#!/usr/bin/env python3
"""make_song.py: make songs with ACE-Step 1.5 on the owner's own free Kaggle GPU.

  python3 make_song.py --quota                      show the weekly GPU quota and exit
  python3 make_song.py --jobs JOBS.json --dry-run   build and check the kernel, push nothing
  python3 make_song.py --jobs JOBS.json --out DIR   push, wait, download, verify, copy the audio
  python3 make_song.py --jobs JOBS.json --out DIR --no-wait   push and come back later
  python3 make_song.py --fetch RUN_ID               download the result of an earlier --no-wait run
  python3 make_song.py --list [--refresh]           list runs that are not finished yet

The only resource used is the Kaggle GPU quota. Credentials stay in the Kaggle CLI's own
location (see README.md); this script never reads, prints or stores a token.
Standard library only. Needs the Kaggle CLI (setup.sh installs it into .venv).
"""
import argparse
import base64
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "kernel"))
RUNS = os.path.join(HERE, "runs")
SLUG = "cap-make-song"            # one private kernel per Kaggle account; runs are versions of it
AUDIO_EXT = (".mp3", ".wav", ".flac", ".ogg", ".opus", ".aac")
ACTIVE_KAGGLE = ("QUEUED", "RUNNING", "NEW")
DONE_KAGGLE = ("COMPLETE", "ERROR", "CANCEL_ACKNOWLEDGED", "CANCELACKNOWLEDGED")
# GPU-time model in minutes, from measured Kaggle T4 runs: setup about 4 min, model load about 2.5 min,
# then roughly one minute per minute of audio.
EST_SETUP_MIN = 8
EST_PER_SONG_MIN = 1.0

sys.stdout.reconfigure(line_buffering=True)


def die(msg, code=2):
    print("make_song: %s" % msg, file=sys.stderr)
    sys.exit(code)


def default_ace_ref():
    try:
        with open(os.path.join(HERE, "ACE_STEP_REF")) as f:
            return f.read().strip() or "main"
    except OSError:
        return "main"


# ----------------------------------------------------------------- jobs and kernel
def load_jobs(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        die("cannot read jobs file %s: %s" % (path, e))
    if isinstance(data, list):
        data = {"songs": data}
    return data


def build_job(data, run_id):
    from gen import normalize_job
    job = {"version": 1, "run_id": run_id, "settings": data.get("settings") or {}, "songs": data.get("songs")}
    try:
        _settings, songs = normalize_job(job)
    except ValueError as e:
        die("bad jobs file: %s" % e)
    return job, songs


def build_kernel(run_dir, job, username, ace_ref):
    """Write kernel-metadata.json and script.py. Returns the kernel folder."""
    kdir = os.path.join(run_dir, "kernel")
    os.makedirs(kdir, exist_ok=True)
    with open(os.path.join(HERE, "kernel", "bootstrap.py")) as f:
        tmpl = f.read()
    with open(os.path.join(HERE, "kernel", "gen.py"), "rb") as f:
        gen_b64 = base64.b64encode(f.read()).decode()
    job_b64 = base64.b64encode(json.dumps(job).encode()).decode()
    script = tmpl.replace("__GEN_B64__", gen_b64).replace("__JOB_B64__", job_b64).replace("__ACE_REF__", ace_ref)
    with open(os.path.join(kdir, "script.py"), "w") as f:
        f.write(script)
    # Without enable_gpu and enable_internet Kaggle silently runs on CPU with no network.
    meta = {"id": "%s/%s" % (username, SLUG), "title": "Cap Make Song", "code_file": "script.py",
            "language": "python", "kernel_type": "script", "is_private": "true",
            "enable_gpu": "true", "enable_tpu": "false", "enable_internet": "true",
            "machine_shape": "NvidiaTeslaT4",
            "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}
    with open(os.path.join(kdir, "kernel-metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
    py_compile.compile(os.path.join(kdir, "script.py"), doraise=True)   # syntax check
    return kdir


# ----------------------------------------------------------------- Kaggle CLI helpers
def kaggle_bin():
    local = os.path.join(HERE, ".venv", "bin", "kaggle")
    if os.path.exists(local):
        return local
    return shutil.which("kaggle")


def kg(*args, check=True):
    exe = kaggle_bin()
    if not exe:
        die("the Kaggle CLI is not installed. Run: bash setup.sh", 3)
    r = subprocess.run([exe, "-W", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        die("kaggle %s failed: %s" % (" ".join(args[:2]), (r.stderr or r.stdout).strip()[:600]), 3)
    return r


def kaggle_username():
    """The username is not a secret. Ask the CLI (it knows the auth method); fall back to the env var."""
    if os.environ.get("KAGGLE_USERNAME"):
        return os.environ["KAGGLE_USERNAME"]
    r = kg("config", "view", check=False)
    m = re.search(r"^\s*-?\s*username:\s*(\S+)", r.stdout or "", re.M)
    return m.group(1) if m and m.group(1) != "None" else None


STATUS_RE = re.compile(r'status\s+"?(?:KernelWorkerStatus\.)?([A-Za-z_]+)"?', re.I)


def parse_status(text):
    m = STATUS_RE.search(text or "")
    return m.group(1).upper() if m else None


def quota_rows():
    r = kg("quota", "--format", "json", check=False)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def gpu_numbers():
    """Returns (used_h, remaining_h) or (None, None)."""
    rows = quota_rows() or []
    for row in rows:
        if str(row.get("resource", "")).upper() == "GPU":
            try:
                return float(str(row["used"]).rstrip("h")), float(str(row["remaining"]).rstrip("h"))
            except (KeyError, ValueError):
                pass
    return None, None


# ----------------------------------------------------------------- run state
def state_path(run_dir):
    return os.path.join(run_dir, "state.json")


def save_state(run_dir, **changes):
    p = state_path(run_dir)
    st = {}
    if os.path.exists(p):
        with open(p) as f:
            st = json.load(f)
    st.update(changes)
    st["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(p, "w") as f:
        json.dump(st, f, indent=2)
    return st


def all_runs():
    out = []
    if os.path.isdir(RUNS):
        for name in sorted(os.listdir(RUNS)):
            p = state_path(os.path.join(RUNS, name))
            if os.path.exists(p):
                with open(p) as f:
                    out.append(json.load(f))
    return out


def run_line(st):
    return "%s | %s | %s | %s | %s" % (st["run_id"], st["slug"], st["status"], st.get("started", "?")[:10], st.get("dest", "?"))


def list_runs(refresh):
    """Print one line per run that is not finished: run id | kernel | status | date | output folder."""
    pending = [s for s in all_runs() if s.get("status") in ("pushed", "running")]
    if not pending:
        print("no unfinished runs")
        return 0
    live = None
    if refresh:
        live = parse_status(kg("kernels", "status", pending[-1]["slug"], check=False).stdout)
    for st in pending:
        line = run_line(st)
        if refresh and st is pending[-1] and live:
            line += "  (Kaggle now says: %s)" % live
        print(line)
    if refresh and len(pending) > 1:
        print("note: only the newest run can be checked, because all runs share one kernel name")
    return 0


# ----------------------------------------------------------------- output
def fetch_output(slug, run_dir):
    odir = os.path.join(run_dir, "output")
    shutil.rmtree(odir, ignore_errors=True)
    os.makedirs(odir)
    kg("kernels", "output", slug, "-p", odir, "-o", "-q")
    for rp in (os.path.join(odir, "out", "results.json"), os.path.join(odir, "results.json")):
        if os.path.exists(rp):
            with open(rp) as f:
                return os.path.dirname(rp), json.load(f)
    return odir, None


def deliver(res, srcdir, dest, songs):
    os.makedirs(dest, exist_ok=True)
    delivered = []
    for s in songs:
        r = (res or {}).get("songs", {}).get(s["id"])
        if not r or r.get("status") != "ok":
            print("  %s: FAILED - %s" % (s["id"], (r or {}).get("error", "no result")))
            continue
        src = os.path.join(srcdir, r["file"])
        target = os.path.join(dest, r["file"])
        shutil.copy(src, target)
        delivered.append(target)
        print("  %s: %s  (seed %s, %ss gen)" % (s["id"], target, r.get("seed"), r.get("elapsed_s")))
    return delivered


def finish(run_dir, st, res, srcdir, t0, used0):
    changes = {}
    if t0 is not None:                       # a fresh run: report wall time and the quota it used
        wall_min = (time.time() - t0) / 60
        used1, _ = gpu_numbers()
        delta = None if used0 is None or used1 is None else round(used1 - used0, 2)
        print("wall time %.1f min; GPU quota used by this run: %s" %
              (wall_min, "%.2f h" % delta if delta is not None else "n/a"))
        changes.update(wall_min=round(wall_min, 1), gpu_quota_delta_h=delta)
    delivered = []
    if res:
        print("timing:", res.get("timing"), "| gpu:", (res.get("env") or {}).get("gpu"),
              "| ACE-Step commit:", res.get("ace_step_commit"))
        if res.get("fatal"):
            print("kernel fatal error:", res["fatal"])
        delivered = deliver(res, srcdir, st["dest"], st["songs"])
    ok = res is not None and len(delivered) == len(st["songs"])
    save_state(run_dir, status="fetched" if ok else "failed", delivered=delivered, **changes)
    if not ok:
        print("some takes are missing. Kernel log tail:")
        print(kg("kernels", "logs", st["slug"], check=False).stdout[-2500:])
    return delivered if ok else None


def wait_and_fetch(run_dir, st, poll, t0, used0):
    slug, run_id = st["slug"], st["run_id"]
    seen_active, last, tries = False, None, 0
    time.sleep(15)
    while True:
        status = parse_status(kg("kernels", "status", slug, check=False).stdout)
        if status != last:
            print("[%s] kernel status: %s  (%.1f min)" % (time.strftime("%H:%M:%S"), status, (time.time() - t0) / 60))
            last = status
            save_state(run_dir, status="running" if status in ACTIVE_KAGGLE else st["status"])
        if status in ACTIVE_KAGGLE:
            seen_active = True
        if status in DONE_KAGGLE:
            if not seen_active and time.time() - t0 < 90:   # stale status of the previous version
                time.sleep(20)
                continue
            srcdir, res = fetch_output(slug, run_dir)
            if res and res.get("run_id") == run_id:          # the output must belong to THIS run
                break
            tries += 1
            if tries > 6:
                print("results.json of run %s was not found (found run_id %s)" % (run_id, (res or {}).get("run_id")))
                res = None
                break
            time.sleep(30)
            continue
        time.sleep(poll)
    return finish(run_dir, st, res, srcdir if res else None, t0, used0)


# ----------------------------------------------------------------- commands
def cmd_run(a):
    data = load_jobs(a.jobs)
    run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    job, songs = build_job(data, run_id)
    ace_ref = a.ace_ref or default_ace_ref()
    dest = os.path.abspath(a.out)
    est_min = EST_SETUP_MIN + sum(EST_PER_SONG_MIN * (s["duration"] / 60 + 0.5) for s in songs)
    timeout = a.timeout or int(min(3 * 3600, max(1800, est_min * 60 * 2.5)))
    user = kaggle_username() if not a.dry_run or kaggle_bin() else None
    run_dir = os.path.join(RUNS, run_id)
    os.makedirs(run_dir)
    kdir = build_kernel(run_dir, job, user or "YOUR_KAGGLE_USERNAME", ace_ref)
    slug = "%s/%s" % (user or "YOUR_KAGGLE_USERNAME", SLUG)
    save_state(run_dir, run_id=run_id, slug=slug, status="dry-run" if a.dry_run else "prepared", dest=dest,
               songs=songs, timeout_s=timeout, ace_ref=ace_ref, started=time.strftime("%Y-%m-%d %H:%M:%S"))
    print("run %s: %d song(s), estimated GPU time about %.0f min (hard limit %d min), ACE-Step %s" %
          (run_id, len(songs), est_min, timeout // 60, ace_ref[:12]))
    print("kernel folder: %s" % kdir)
    if a.dry_run:
        print("dry-run: nothing pushed.")
        return 0
    if not user:
        die("no Kaggle login found. Follow the Kaggle steps in README.md, then run: bash doctor.sh", 3)
    # one run at a time: the kernel name is shared, so a second push would replace the first
    for other in all_runs():
        if other["run_id"] != run_id and other.get("status") in ("pushed", "running"):
            live = parse_status(kg("kernels", "status", other["slug"], check=False).stdout)
            if live in ACTIVE_KAGGLE:
                die("run %s is still %s on Kaggle. Fetch or wait for it first (--list --refresh)." % (other["run_id"], live))
    used0, remaining = gpu_numbers()
    if remaining is not None and remaining < est_min / 60:
        die("only %.2f GPU hours left this week, this run needs about %.2f. Not pushing." % (remaining, est_min / 60), 4)
    t0 = time.time()
    r = kg("kernels", "push", "-p", kdir, "--accelerator", "NvidiaTeslaT4", "-t", str(timeout))
    print((r.stdout or "").strip()[:300])
    st = save_state(run_dir, status="pushed")
    if a.no_wait:
        print("pushed. Fetch later with: python3 make_song.py --fetch %s" % run_id)
        print("tracking line: %s" % run_line(st))
        return 0
    out = wait_and_fetch(run_dir, st, a.poll, t0, used0)
    return 0 if out else 1


def cmd_fetch(a):
    rd = a.fetch if os.path.isdir(a.fetch) else os.path.join(RUNS, a.fetch)
    if not os.path.exists(state_path(rd)):
        die("no such run: %s" % a.fetch)
    with open(state_path(rd)) as f:
        st = json.load(f)
    status = parse_status(kg("kernels", "status", st["slug"]).stdout)
    print("kernel status:", status)
    if status in ACTIVE_KAGGLE:
        print("still running. Try again later.")
        return 2
    if status not in DONE_KAGGLE:
        die("unexpected kernel status %s" % status)
    srcdir, res = fetch_output(st["slug"], rd)
    if not res or res.get("run_id") != st["run_id"]:
        die("the kernel output does not belong to run %s (a newer run may have replaced it)" % st["run_id"], 5)
    return 0 if finish(rd, st, res, srcdir, None, None) else 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--jobs", help="jobs JSON: a list of songs, or {\"settings\": {...}, \"songs\": [...]}")
    p.add_argument("--out", default="out", help="folder for the finished audio (default: ./out)")
    p.add_argument("--timeout", type=int, help="kernel run limit in seconds: the hard cap on GPU use")
    p.add_argument("--ace-ref", help="ACE-Step git commit or ref (default: the tested commit in ACE_STEP_REF)")
    p.add_argument("--poll", type=int, default=30, help="seconds between status checks")
    p.add_argument("--no-wait", action="store_true", help="push and return; fetch later with --fetch")
    p.add_argument("--fetch", metavar="RUN_ID", help="download the output of an earlier --no-wait run")
    p.add_argument("--dry-run", action="store_true", help="build and check the kernel, push nothing")
    p.add_argument("--quota", action="store_true", help="show the Kaggle GPU quota and exit")
    p.add_argument("--list", action="store_true", help="list runs that are not finished")
    p.add_argument("--refresh", action="store_true", help="with --list: ask Kaggle for the live status")
    a = p.parse_args(argv)
    if a.quota:
        print(kg("quota").stdout)
        return 0
    if a.list:
        return list_runs(a.refresh)
    if a.fetch:
        return cmd_fetch(a)
    if not a.jobs:
        p.error("give --jobs FILE (see examples/jobs.example.json), or --quota, --list, --fetch")
    return cmd_run(a)


if __name__ == "__main__":
    sys.exit(main())
