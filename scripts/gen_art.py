#!/usr/bin/env python3
"""Generate illustration candidates locally (Z-Image-Turbo, Apache-2.0) in one fixed house style.

Usage (from repo root, system python3; no venv activation needed):
    python3 scripts/gen_art.py --id amina_finger --prompt "a teenage girl looking at her bandaged finger" \
        [--n 4] [--size 1536x864|1024x1024] [--seed 123] [--out data/presentations_art/candidates] [--steps 9]

Writes <out>/<id>/cand_<k>.png and <out>/<id>/meta.json (full prompt, model + revision, per-candidate seed,
settings, timestamp). Candidate k uses seed (base+k-1), so each image is reproducible.
Exit codes: 0 ok, 2 setup/GPU/model unavailable or bad arguments.
Setup lives in /home/markk/imggen (venv, weights, notes in README.txt). Prompt tips: describe what IS in the
scene; the model does not obey negations ("no people" can add people). Scene text should avoid words to be written.
"""
import argparse, datetime, json, os, sys

IMGGEN = "/home/markk/imggen"
VENV_PY = IMGGEN + "/venv/bin/python"
MODEL_DIR = IMGGEN + "/models/Z-Image-Turbo"
MODEL_NAME = "Tongyi-MAI/Z-Image-Turbo"
STYLE_VERSION = "2026-10-22-v4"
# {scene} is replaced by --prompt. Z-Image-Turbo runs at guidance 0, so there is no negative prompt: every
# exclusion has to live in this positive text (and works only partly: see imggen/README.txt).
STYLE_PRESET = (
    "Flat vector educational illustration for a children's science textbook, clean smooth outlines, "
    "bright friendly colour palette with cyan, lime green, magenta, orange and red accents plus warm browns and greens, "
    "simple plain soft off-white background, uncluttered, no text, no letters, no numbers, no logos, no watermark, "
    "not photorealistic, child-friendly.{people} Scene: {scene}"
)
# Added only when the scene mentions people: putting it in every prompt made the model invent children in
# kitchens, labs and gardens. Tested and dropped: spelling out 'teenagers about 16, tall' made single-person
# scenes into groups of extra people. Say 'a single ...' in the scene if you want exactly one person.
PEOPLE_CLAUSE = (
    " People are friendly stylised cartoon Kenyan characters with dark brown skin and short black hair, hair braids "
    "or hair buns, wearing bright clothes."
)
PEOPLE_RE = r"\b(girl|boy|student|learner|teacher|person|people|child|children|man|woman|farmer|mother|father|family|friend|friends|teenager|teenage|classmates?|scientist|figure)s?\b"
NEGATIVE_PROMPT = None  # not supported by this distilled model at guidance 0
SIZES = {"1536x864": (1536, 864), "1024x1024": (1024, 1024)}


def die(msg, code=2):
    print("gen_art: " + msg, file=sys.stderr)
    sys.exit(code)


def parse():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True, help="slug; becomes the folder name")
    ap.add_argument("--prompt", required=True, help="scene description (the style preset is prepended)")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--size", default="1536x864", help="1536x864 or 1024x1024 (any WxH multiple of 16 also works)")
    ap.add_argument("--seed", type=int, default=None, help="base seed (default: random, recorded in meta.json)")
    ap.add_argument("--out", default="data/presentations_art/candidates")
    ap.add_argument("--people", dest="people", action="store_true", default=None, help="force the people-style clause (default: auto, if the scene mentions people)")
    ap.add_argument("--no-people", dest="people", action="store_false", help="never add the people-style clause")
    ap.add_argument("--steps", type=int, default=9, help="denoising steps (Turbo is tuned for 9)")
    return ap.parse_args()


def main():
    a = parse()
    if not a.id.replace("_", "").replace("-", "").isalnum():
        die("--id must be letters, digits, - or _")
    if a.size in SIZES:
        w, h = SIZES[a.size]
    else:
        try:
            w, h = (int(x) for x in a.size.lower().split("x"))
            assert w % 16 == 0 and h % 16 == 0 and 256 <= w <= 2048 and 256 <= h <= 2048
        except Exception:
            die("bad --size %r" % a.size)
    if a.n < 1:
        die("--n must be >= 1")
    # Re-exec under the imggen venv (heavy deps live only there).
    if os.path.realpath(sys.prefix) != os.path.realpath(IMGGEN + "/venv"):
        if not os.path.exists(VENV_PY):
            die("venv python missing: %s. See %s/README.txt to rebuild it." % (VENV_PY, IMGGEN))
        os.execv(VENV_PY, [VENV_PY] + sys.argv)
    if not os.path.isdir(MODEL_DIR):
        die("model weights missing: " + MODEL_DIR)
    os.environ["HF_HUB_OFFLINE"] = "1"
    try:
        import torch, diffusers
    except Exception as e:
        die("cannot import torch/diffusers in the imggen venv: %s" % e)
    if not torch.cuda.is_available():
        die("no usable CUDA GPU (torch.cuda.is_available() is False). Check nvidia-smi.")
    free = torch.cuda.mem_get_info()[0] / 1e9
    try:   # unified memory: CUDA 'free' leaves out reclaimable file cache (model files just read), which the kernel gives back on demand
        avail = int([l for l in open('/proc/meminfo') if l.startswith('MemAvailable')][0].split()[1]) / 1e6
    except Exception:
        avail = 0
    free = max(free, avail - 8)    # keep 8 GB headroom for the system
    if free < 28:
        die("only %.0f GB memory free; the model needs about 28 GB. Stop something (e.g. vlm-qa/stop_server.sh) and retry." % free)
    try:
        pipe = diffusers.ZImagePipeline.from_pretrained(MODEL_DIR, torch_dtype=torch.bfloat16, local_files_only=True).to("cuda")
    except Exception as e:
        die("could not load model from %s: %s" % (MODEL_DIR, e))

    import random, time
    base = a.seed if a.seed is not None else random.randrange(0, 2**31 - a.n)
    import re
    people = a.people if a.people is not None else bool(re.search(PEOPLE_RE, a.prompt, re.I))
    full = STYLE_PRESET.replace("{people}", PEOPLE_CLAUSE if people else "").replace("{scene}", a.prompt.strip())
    d = os.path.join(a.out, a.id)
    os.makedirs(d, exist_ok=True)
    cands = []
    t_all = time.time()
    for k in range(a.n):
        seed = base + k
        t = time.time()
        try:
            img = pipe(full, height=h, width=w, num_inference_steps=a.steps, guidance_scale=0.0,
                       generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        except Exception as e:
            die("generation failed on candidate %d: %s" % (k + 1, e))
        fn = "cand_%d.png" % (k + 1)
        img.save(os.path.join(d, fn))
        cands.append({"file": fn, "seed": seed, "seconds": round(time.time() - t, 1)})
        print("%s/%s  seed %d  %.1fs" % (d, fn, seed, time.time() - t), flush=True)
    rev = ""
    try:
        rev = open(IMGGEN + "/MODEL_REVISION").read().strip()
    except OSError:
        pass
    meta = {
        "id": a.id, "scene": a.prompt.strip(), "style_version": STYLE_VERSION, "prompt": full,
        "negative_prompt": NEGATIVE_PROMPT, "model": MODEL_NAME, "model_revision": rev, "licence": "Apache-2.0",
        "settings": {"width": w, "height": h, "steps": a.steps, "guidance_scale": 0.0, "dtype": "bfloat16",
                     "base_seed": base, "people_clause": people, "torch": torch.__version__, "diffusers": diffusers.__version__},
        "candidates": cands, "peak_gpu_gb": round(torch.cuda.max_memory_allocated() / 1e9, 1),
        "total_seconds": round(time.time() - t_all, 1),
        "created": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    old = os.path.join(d, "meta.json")
    if os.path.exists(old):  # keep a regeneration from silently erasing a previous choice record
        try:
            meta["previous"] = {k: v for k, v in json.load(open(old)).items() if k in ("created", "chosen", "base_seed")}
        except Exception:
            pass
    with open(old, "w") as f:
        json.dump(meta, f, indent=2)
    print("wrote %s (peak GPU %.1f GB)" % (old, meta["peak_gpu_gb"]))


if __name__ == "__main__":
    main()
