# Kaggle script kernel template. make_song.py fills the three placeholders and pushes the result.
# Stage 1 (this file, Kaggle's system python): install uv and ACE-Step 1.5 at a pinned commit into a venv.
# Stage 2: run the embedded gen.py inside that venv. No token or credential is ever embedded here.
import base64, json, os, shutil, subprocess, sys, time

GEN_B64 = "__GEN_B64__"
JOB_B64 = "__JOB_B64__"
ACE_REF = "__ACE_REF__"          # git ref of ACE-Step-1.5: a commit hash (tested) or "main"
ACE_URL = "https://github.com/ace-step/ACE-Step-1.5"

T0 = time.time()
WORK = "/kaggle/working" if os.path.isdir("/kaggle/working") else os.environ.get("CAP_WORK", "/tmp/cap_work")
OUT = os.path.join(WORK, "out")
TMP = os.environ.get("CAP_TMP", "/tmp/cap_ace")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)


def sh(cmd, **kw):
    print("$", cmd if isinstance(cmd, str) else " ".join(cmd), flush=True)
    return subprocess.run(cmd, shell=isinstance(cmd, str), **kw).returncode


def main():
    timing = {}
    job = json.loads(base64.b64decode(JOB_B64))
    with open(os.path.join(TMP, "job.json"), "w") as f:
        json.dump(job, f)
    with open(os.path.join(TMP, "cap_gen.py"), "wb") as f:
        f.write(base64.b64decode(GEN_B64))
    sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv || true")
    repo = os.path.join(TMP, "ace")
    py = os.environ.get("CAP_PYTHON")           # tests only: use an existing interpreter
    if not os.environ.get("CAP_SKIP_INSTALL"):
        t = time.time()
        if sh([sys.executable, "-m", "pip", "install", "-q", "uv"]) != 0:
            sys.exit("pip install uv failed")
        if not os.path.isdir(repo):
            if sh(["git", "clone", "-q", ACE_URL, repo]) != 0:
                sys.exit("git clone failed (is internet enabled for the kernel?)")
        if ACE_REF != "main" and sh(["git", "-C", repo, "checkout", "-q", ACE_REF]) != 0:
            sys.exit("git checkout of ACE_REF %s failed" % ACE_REF)
        env = dict(os.environ, UV_HTTP_TIMEOUT="600", UV_LINK_MODE="copy")
        rc = sh([sys.executable, "-m", "uv", "sync", "--frozen", "--python", "3.12"], cwd=repo, env=env)
        if rc != 0:
            print("frozen sync failed, retrying with fresh resolution", flush=True)
            rc = sh([sys.executable, "-m", "uv", "sync", "--python", "3.12"], cwd=repo, env=env)
        if rc != 0:
            sys.exit("uv sync failed")
        py = os.path.join(repo, ".venv", "bin", "python")
        timing["install_s"] = round(time.time() - t, 1)
    elif not py:
        py = sys.executable
    commit = "n/a"
    if os.path.isdir(os.path.join(repo, ".git")):
        commit = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip() or "n/a"
    env = dict(os.environ, PYTHONPATH=repo + os.pathsep + os.environ.get("PYTHONPATH", ""),
               CUDA_VISIBLE_DEVICES="0", ACESTEP_DOWNLOAD_SOURCE="huggingface", PYTHONUNBUFFERED="1")
    t = time.time()
    rc = sh([py, os.path.join(TMP, "cap_gen.py"), "--job", os.path.join(TMP, "job.json"),
             "--out", OUT, "--repo", repo], env=env)
    timing["gen_stage_s"] = round(time.time() - t, 1)
    timing["total_s"] = round(time.time() - T0, 1)
    try:  # add bootstrap timing and the ACE-Step commit to results.json
        p = os.path.join(OUT, "results.json")
        r = json.load(open(p)) if os.path.exists(p) else {"run_id": job.get("run_id")}
        r.setdefault("timing", {}).update(timing)
        r["ace_step_commit"] = commit
        with open(p, "w") as f:
            json.dump(r, f, indent=2)
    except Exception as e:
        print("could not enrich results.json:", e)
    shutil.rmtree(os.path.join(OUT, "_work"), ignore_errors=True)
    print("[cap-boot] finished rc=%s timing=%s" % (rc, timing), flush=True)
    sys.exit(rc)


main()
