#!/usr/bin/env python3
"""
validate_quiz.py — contract + quality gate for Quick Check quizzes
===================================================================
Runs inside src/generate_quiz.py (every lesson is validated before it is
saved) and on demand over any set of <prefix>_quiz.json files. Rules come from
config/quiz_generation.yaml. Handoff §3b.

HARD FAILURES (exit 1):
  count outside 5..10; not exactly 4 choices; duplicate choices; correctIndex
  out of range; invalid phase; empty prompt/placement/rationale; banned choice
  phrase ("all of the above" ...); a rationale naming an answer letter;
  arithmetic `check` that does not evaluate to a number in the correct choice;
  placement with zero overlap with the lesson plan; corpus answer-letter share
  outside the configured range (once enough questions exist).
WARNINGS: weak placement overlap; possibly not self-contained wording; a
  numeric check that matches a distractor as well; lesson missing from quiz.

Usage:
  python3 scripts/validate_quiz.py                     # all *_quiz.json under data/outputs/v2
  python3 scripts/validate_quiz.py path/X_quiz.json ... | dir ...
"""
import ast
import glob
import json
import math
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "config", "quiz_generation.yaml")
LETTERS = "ABCD"
STOP = set("""the and for with from into that this what when where which who why how does are was were
its their your you can all not also about between through than then them they there these those
have has had been being will would should could may might must very more most some such only
each other after before during while lesson students student teacher class part step""".split())


def load_config(path=CONFIG):
    import yaml
    with open(path) as f:
        cfg = yaml.safe_load(f)
    cfg["_banned_choice"] = [p.lower() for p in cfg["banned_choice_phrases"]]
    cfg["_banned_rationale"] = re.compile("|".join(cfg["banned_rationale_patterns"]))
    cfg["_not_self_contained"] = re.compile("|".join(cfg["not_self_contained_patterns"]), re.I)
    return cfg


# ── arithmetic check ─────────────────────────────────────────────────────────

_FUNCS = {
    "sqrt": math.sqrt, "log10": math.log10, "log": math.log, "ln": math.log, "exp": math.exp,
    "abs": abs, "round": round,
    # Degrees, as taught in the Kenyan syllabus.
    "sin": lambda d: math.sin(math.radians(d)), "cos": lambda d: math.cos(math.radians(d)),
    "tan": lambda d: math.tan(math.radians(d)),
    "asin": lambda x: math.degrees(math.asin(x)), "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
}
_CONSTS = {"pi": math.pi, "e": math.e}


def safe_eval(expr: str) -> float:
    """Evaluate a pure arithmetic expression (numbers, + - * / ** %, whitelisted functions)."""
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Name) and n.id in _CONSTS:
            return _CONSTS[n.id]
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div): return a / b
            if isinstance(n.op, ast.Pow): return a ** b
            if isinstance(n.op, ast.Mod): return a % b
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in _FUNCS and not n.keywords:
            return _FUNCS[n.func.id](*[ev(a) for a in n.args])
        raise ValueError(f"unsupported expression element: {ast.dump(n)[:60]}")
    return float(ev(ast.parse(expr.replace("^", "**").replace("×", "*").replace("÷", "/"), mode="eval")))


_NUM = re.compile(r"[-\u2212]?\d{1,3}(?:[ ,\u00a0\u2009]\d{3})+(?:\.\d+)?|[-\u2212]?\d+(?:\.\d+)?")


def numbers_in(text: str) -> list[tuple[float, int]]:
    """Numbers in text, each with the count of decimals shown ("2.8" -> (2.8, 1))."""
    out = []
    for m in _NUM.finditer(text or ""):
        raw = re.sub(r"[ ,\u00a0\u2009]", "", m.group()).replace("\u2212", "-")
        try:
            out.append((float(raw), len(raw.split(".")[1]) if "." in raw else 0))
        except ValueError:
            pass
    return out


def close(val: float, shown: tuple[float, int], strict: bool = False) -> bool:
    """True if `val` rounds to the number as shown, or (unless strict) is within 1% of it."""
    n, decimals = shown
    if abs(val - n) <= 0.5 * 10 ** -decimals + 1e-9:
        return True
    return not strict and math.isclose(val, n, rel_tol=0.01, abs_tol=1e-9)


# ── per-lesson validation ────────────────────────────────────────────────────

def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z\-']{2,}", (text or "").lower()) if w not in STOP}


def lesson_text(lesson: dict) -> str:
    parts = [lesson.get("title", ""), lesson.get("overview", "")]
    for f in lesson.get("framework", []):
        parts += [f.get("learnerExperience", ""), f.get("teacherMoves", ""),
                  f.get("sensemakingStrategy", ""), f.get("formativeAssessment", "")]
    return " ".join(parts)


def validate_lesson_quiz(quiz: list, lesson: dict | None, cfg: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one lesson's quiz array."""
    errs, warns = [], []
    if not (cfg["questions_min"] <= len(quiz) <= cfg["questions_max"]):
        errs.append(f"{len(quiz)} questions (need {cfg['questions_min']}-{cfg['questions_max']})")
    elif len(quiz) > cfg.get("questions_typical_max", cfg["questions_max"]):
        warns.append(f"{len(quiz)} questions (normal is {cfg['questions_min']}-{cfg['questions_typical_max']};"
                     " fine only for a content-heavy lesson)")
    ltext_words = content_words(lesson_text(lesson)) if lesson else None
    for i, q in enumerate(quiz, 1):
        tag = f"Q{i}"
        ch = q.get("choices") or []
        if len(ch) != cfg["choices"]:
            errs.append(f"{tag}: {len(ch)} choices")
        # Case/whitespace/trailing-punctuation only: maths choices differ by
        # symbols ("sin θ / cos θ" vs "sin θ × cos θ"), which must survive.
        norm = [re.sub(r"\s+", " ", str(c)).strip().rstrip(".").lower() for c in ch]
        if len(set(norm)) != len(norm):
            errs.append(f"{tag}: duplicate choices")
        if any(not c for c in norm):
            errs.append(f"{tag}: empty choice")
        ci = q.get("correctIndex")
        if not isinstance(ci, int) or not (0 <= ci < len(ch)):
            errs.append(f"{tag}: correctIndex {ci!r} out of range")
            continue
        if q.get("phase") not in cfg["phases"]:
            errs.append(f"{tag}: invalid phase {q.get('phase')!r}")
        for field in ("prompt", "placement", "rationale"):
            if not str(q.get(field, "")).strip():
                errs.append(f"{tag}: empty {field}")
        for c in norm:
            for b in cfg["_banned_choice"]:
                if c == b or c.startswith(b + " ") or c.endswith(" " + b):
                    errs.append(f"{tag}: banned choice phrase {b!r}")
        if cfg["_banned_rationale"].search(q.get("rationale", "")):
            errs.append(f"{tag}: rationale names an answer letter (choices are shuffled)")
        if cfg["_not_self_contained"].search(q.get("prompt", "")):
            warns.append(f"{tag}: prompt may depend on something not shown: {q['prompt'][:70]!r}")
        chk = q.get("check")
        if chk:
            try:
                val = safe_eval(chk)
            except Exception as e:
                errs.append(f"{tag}: check {chk!r} does not evaluate ({e})")
            else:
                if not any(close(val, n) for n in numbers_in(ch[ci])):
                    errs.append(f"{tag}: check {chk!r} = {val:.6g}, not found in correct choice {ch[ci]!r}")
                elif any(close(val, n, strict=True) for j, c in enumerate(ch) if j != ci for n in numbers_in(c)):
                    warns.append(f"{tag}: check value {val:.6g} also appears in a distractor")
        if ltext_words is not None:
            pw = content_words(q.get("placement", ""))
            if pw:
                share = len(pw & ltext_words) / len(pw)
                if share == 0 and q.get("phase") != "end":
                    errs.append(f"{tag}: placement {q['placement']!r} matches nothing in the lesson plan")
                elif share < cfg["placement_min_overlap"]:  # includes end-of-lesson with no overlap
                    warns.append(f"{tag}: placement weakly matches lesson plan ({share:.0%}): {q['placement']!r}")
    return errs, warns


def letter_distribution(files: list[str]) -> Counter:
    c = Counter()
    for f in files:
        for L in json.load(open(f)).get("lessons", []):
            for q in L.get("quiz", []):
                if isinstance(q.get("correctIndex"), int) and 0 <= q["correctIndex"] < 4:
                    c[LETTERS[q["correctIndex"]]] += 1
    return c


def find_quiz_files(args):
    targets = args or [os.path.join(ROOT, "data", "outputs", "v2")]
    out = []
    for t in targets:
        out += glob.glob(os.path.join(t, "**", "*_quiz.json"), recursive=True) if os.path.isdir(t) else [t]
    return sorted(set(out))


def main(argv):
    cfg = load_config()
    files = find_quiz_files([a for a in argv if not a.startswith("--")])
    if not files:
        print("validate_quiz: no *_quiz.json found")
        return 1
    n_err = n_warn = n_q = n_lessons = 0
    for f in files:
        d = json.load(open(f))
        data_path = re.sub(r"_quiz[^/]*\.json$", "_data.json", f)
        lessons = {L["number"]: L for L in json.load(open(data_path))["LESSONS"]} if os.path.exists(data_path) else {}
        rel = os.path.relpath(f, ROOT)
        seen = set()
        for L in d.get("lessons", []):
            seen.add(L["number"])
            n_lessons += 1
            n_q += len(L.get("quiz", []))
            errs, warns = validate_lesson_quiz(L.get("quiz", []), lessons.get(L["number"]), cfg)
            for e in errs:
                print(f"  FAIL {rel} L{L['number']} {e}")
            for w in warns:
                print(f"  WARN {rel} L{L['number']} {w}")
            n_err += len(errs)
            n_warn += len(warns)
        missing = sorted(set(lessons) - seen)
        if missing:
            print(f"  WARN {rel}: no quiz for lessons {missing}")
            n_warn += 1
    dist = letter_distribution(files)
    total = sum(dist.values())
    shares = {k: dist[k] / total for k in LETTERS} if total else {}
    print(f"validate_quiz: {len(files)} file(s), {n_lessons} lessons, {n_q} questions")
    print("  answer letters: " + "  ".join(f"{k}={dist[k]} ({shares.get(k, 0):.0%})" for k in LETTERS))
    if total >= cfg["letter_check_min_questions"]:
        skew = [k for k in LETTERS if not (cfg["letter_share_min"] <= shares[k] <= cfg["letter_share_max"])]
        if skew:
            print(f"  FAIL answer-letter share outside {cfg['letter_share_min']:.0%}-{cfg['letter_share_max']:.0%}: {skew}")
            n_err += 1
    print(f"  {n_err} failure(s), {n_warn} warning(s)")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
