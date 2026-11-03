#!/usr/bin/env python3
"""Generation stage: runs INSIDE the ACE-Step venv (on Kaggle, or locally in tests).

Usage: python gen.py --job job.json --out OUTDIR --repo ACE_STEP_REPO
Reads the job file, loads ACE-Step 1.5 once, generates every song in the batch,
writes <id>.<ext> files and results.json to OUTDIR. A failing song never stops
the rest of the batch. Reference audio (timbre cloning) is deliberately not supported.
"""
import argparse, json, os, re, shutil, sys, time, traceback

SETTINGS_DEFAULT = {
    "dit": "acestep-v15-turbo",        # acestep-v15-xl-turbo needs >=12 GB VRAM + offload
    "lm": "acestep-5Hz-lm-1.7B",       # or acestep-5Hz-lm-0.6B / "none" (DiT only)
    "lm_backend": "pt",                # vllm/nano-vllm needs flash-attn: not on a T4
    "format": "mp3",                   # mp3 | wav | flac
    "steps": 8,
    "dtype": "auto",                   # auto|bfloat16|float16. T4 (pre-Ampere): fp16 gives NaN latents -> force bf16
}
SONG_DEFAULT = {
    "caption": "", "lyrics": "", "duration": 60, "seed": -1, "instrumental": False,
    "language": "en", "bpm": None, "keyscale": "", "timesignature": "",
}


def log(*a):
    print("[cap-gen]", *a, flush=True)


def normalize_job(job):
    """Validate + fill defaults. Pure function (unit-tested offline)."""
    if not isinstance(job, dict) or not isinstance(job.get("songs"), list) or not job["songs"]:
        raise ValueError("job needs a non-empty 'songs' list")
    settings = dict(SETTINGS_DEFAULT); settings.update(job.get("settings") or {})
    songs, seen = [], set()
    for i, s in enumerate(job["songs"]):
        song = dict(SONG_DEFAULT); song.update(s)
        song["id"] = str(s.get("id") or f"song{i+1}")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", song["id"]):
            raise ValueError(f"song id {song['id']!r}: use letters, digits, - and _ only (it becomes the file name)")
        if song["id"] in seen:
            raise ValueError(f"duplicate song id {song['id']}")
        seen.add(song["id"])
        if not (song["caption"] or song["lyrics"] or song["instrumental"]):
            raise ValueError(f"{song['id']}: need caption (tags) or lyrics")
        if len(song["lyrics"]) > 4096:
            raise ValueError(f"{song['id']}: lyrics are longer than 4096 characters")
        if len(song["caption"]) > 512:
            raise ValueError(f"{song['id']}: caption (style tags) is longer than 512 characters")
        song["duration"] = float(song["duration"])
        if not 10.0 <= song["duration"] <= 600.0:
            raise ValueError(f"{song['id']}: duration must be between 10 and 600 seconds")
        song["seed"] = int(song["seed"])
        if song["instrumental"]:
            song["lyrics"] = "[Instrumental]"
        songs.append(song)
    return settings, songs


def env_info():
    info = {"python": sys.version.split()[0]}
    try:
        import torch
        info["torch"] = torch.__version__
        info["cuda"] = bool(torch.cuda.is_available())
        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
            info["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1)
    except Exception as e:  # noqa
        info["torch_error"] = str(e)
    return info


def force_bf16():
    """ACE-Step picks fp16 on pre-Ampere GPUs (T4), which produced NaN latents on the first real run.
    Make its capability checks report bf16 (PyTorch emulates it on sm75: slower but numerically safe)."""
    import importlib
    for modname in ("acestep.gpu_config", "acestep.core.generation.handler.memory_utils"):
        m = importlib.import_module(modname)
        m.cuda_supports_bfloat16 = lambda *a, **k: True
    log("forced bfloat16 dtype for pre-Ampere GPU")


def enter_fp32(eng):
    """Last-resort fallback after NaN: run the DiT in float32 and drop the LM to fit 15 GB."""
    dit = eng["dit"]
    try:
        import torch
        dit.dtype = torch.float32
        dit.model = dit.model.to(torch.float32)
        if getattr(dit, "silence_latent", None) is not None:
            dit.silence_latent = dit.silence_latent.to(torch.float32)
        try:
            eng["llm"].llm = None; torch.cuda.empty_cache()
        except Exception:
            pass
    except ImportError:
        dit.dtype = "float32"
    eng["use_lm"] = False; eng["fp32"] = True
    log("fallback: DiT in float32, LM off (thinking=False)")


def load_engine(settings, repo):
    """Import ACE-Step and initialise handlers. Returns an engine dict."""
    sys.path.insert(0, repo)
    if settings.get("dtype", "auto") in ("auto", "bfloat16"):
        try:
            import torch
            if torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] < 8:
                force_bf16()
        except ImportError:
            pass
    from pathlib import Path
    from acestep.handler import AceStepHandler
    from acestep.llm_inference import LLMHandler
    from acestep.inference import GenerationParams, GenerationConfig, generate_music

    ckpt = os.path.join(repo, "checkpoints")
    dit = AceStepHandler()
    t = time.time()
    msg, ok = dit.initialize_service(project_root=repo, config_path=settings["dit"], device="auto",
                                     offload_to_cpu=False)
    if not ok:
        raise RuntimeError(f"DiT init failed: {msg}")
    log(f"DiT {settings['dit']} ready in {time.time()-t:.0f}s")

    llm = LLMHandler()
    use_lm = settings["lm"] and settings["lm"].lower() != "none"
    if use_lm:
        t = time.time()
        try:
            from acestep.model_downloader import ensure_lm_model
            ok_dl, msg_dl = ensure_lm_model(settings["lm"], Path(ckpt))
            if not ok_dl:
                raise RuntimeError(msg_dl)
            msg, ok = llm.initialize(checkpoint_dir=ckpt, lm_model_path=settings["lm"],
                                     backend=settings["lm_backend"], device="auto",
                                     offload_to_cpu=False, dtype=None)
            if not ok:
                raise RuntimeError(msg)
            log(f"LM {settings['lm']} ready in {time.time()-t:.0f}s")
        except Exception as e:  # fall back to DiT-only: still produces music
            log(f"LM init failed ({e}); continuing DiT-only (thinking=False)")
            use_lm = False
    return {"dit": dit, "llm": llm, "use_lm": use_lm, "fp32": False, "GenerationParams": GenerationParams,
            "GenerationConfig": GenerationConfig, "generate_music": generate_music}


def generate_one(eng, settings, song, out_dir):
    r = _generate_one(eng, settings, song, out_dir)
    if r["status"] == "error" and "NaN or Inf" in r.get("error", "") and not eng.get("fp32"):
        enter_fp32(eng)
        r = _generate_one(eng, settings, song, out_dir); r["fallback"] = "float32,no-LM"
    return r


def _generate_one(eng, settings, song, out_dir):
    fmt = settings["format"]
    turbo = "turbo" in settings["dit"]
    params = eng["GenerationParams"](
        task_type="text2music", thinking=bool(eng["use_lm"]),
        caption=song["caption"], lyrics=song["lyrics"], instrumental=bool(song["instrumental"]),
        bpm=song["bpm"], keyscale=song["keyscale"], timesignature=song["timesignature"],
        vocal_language=song["language"] if not song["instrumental"] else "unknown",
        duration=song["duration"], inference_steps=int(settings["steps"]),
        guidance_scale=1.0 if turbo else 7.0, shift=3.0 if turbo else 1.0, seed=song["seed"])
    last_err = None
    for f in ([fmt] if fmt == "wav" else [fmt, "wav"]):
        cfg_kwargs = dict(batch_size=1, audio_format=f, use_random_seed=song["seed"] < 0)
        if f == "mp3": cfg_kwargs["mp3_bitrate"] = "192k"
        if song["seed"] >= 0:
            cfg_kwargs["seeds"] = [song["seed"]]
        config = eng["GenerationConfig"](**cfg_kwargs)
        work = os.path.join(out_dir, "_work", song["id"]); os.makedirs(work, exist_ok=True)
        res = eng["generate_music"](eng["dit"], eng["llm"], params, config, save_dir=work)
        if getattr(res, "success", False) and res.audios and res.audios[0].get("path"):
            src = res.audios[0]["path"]
            dst = os.path.join(out_dir, song["id"] + os.path.splitext(src)[1])
            shutil.copy(src, dst)
            used_seed = (res.audios[0].get("params") or {}).get("seed", song["seed"])
            return {"status": "ok", "file": os.path.basename(dst), "seed": used_seed, "format": f}
        last_err = getattr(res, "error", None) or getattr(res, "status_message", "unknown error")
        log(f"{song['id']}: format {f} failed: {last_err}")
        if not getattr(res, "success", False):
            break   # real generation failure, not a file-format problem: don't repeat it
    return {"status": "error", "error": str(last_err)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args(argv)
    t0 = time.time()
    os.makedirs(a.out, exist_ok=True)
    job = json.load(open(a.job))
    settings, songs = normalize_job(job)
    results = {"run_id": job.get("run_id"), "settings": settings, "env": env_info(), "songs": {},
               "timing": {}}
    eng = None
    try:
        eng = load_engine(settings, a.repo)
        results["timing"]["load_s"] = round(time.time() - t0, 1)
        for s in songs:
            t = time.time(); log(f"generating {s['id']} ({s['duration']:.0f}s, seed {s['seed']})")
            try:
                r = generate_one(eng, settings, s, a.out)
            except Exception as e:
                traceback.print_exc(); r = {"status": "error", "error": repr(e)}
            r["elapsed_s"] = round(time.time() - t, 1); r["duration_req"] = s["duration"]
            results["songs"][s["id"]] = r
            log(f"{s['id']}: {r['status']} in {r['elapsed_s']}s")
    except Exception as e:
        traceback.print_exc(); results["fatal"] = repr(e)
    results["timing"]["total_s"] = round(time.time() - t0, 1)
    shutil.rmtree(os.path.join(a.out, "_work"), ignore_errors=True)
    json.dump(results, open(os.path.join(a.out, "results.json"), "w"), indent=2)
    ok = sum(1 for r in results["songs"].values() if r["status"] == "ok")
    log(f"done: {ok}/{len(songs)} ok in {results['timing']['total_s']}s")
    return 0 if ok == len(songs) else 1


if __name__ == "__main__":
    sys.exit(main())
