#!/usr/bin/env python3
"""
validate_consistency.py — cross-document consistency gate
=========================================================
The three documents of a sub-strand (lesson sequence, Summary Table, Final
Explanation) are rendered from one *_data.json. Nothing used to check that they
AGREE with each other. The partner's validator did, on 2026-10-03, and found a
Summary Table describing different lessons and a Final Explanation whose data
contradicted its own prompt. This is the check that would have caught it.

Run automatically by generators/generate.js after every render; on demand over
the whole corpus. Exit 1 on any hard failure.

HARD FAILURES
  ST-TITLE   Summary Table lesson number/title differs from the lesson's
  ST-TEXT    Summary Table observed/learned/explained differs from the lesson's
             own summaryTablePrompt (it is derived from it; a mismatch means a
             lesson was edited without re-deriving the table)
  ST-COUNT   Summary Table and lesson sequence have different lesson counts
  FE-EMPTY   Final Explanation missing, <3 sections, or a prompt/exemplar empty
  FE-LEAK    scratch work / self-correction text left in the Final Explanation
  FE-TABLE   malformed markdown table (glued '||', missing or repeated separator row)
  FE-ENTITY  a labelled entity in the Final Explanation ("Runner B", "Sample C")
             that no lesson ever mentions: a second, invented dataset
  FE-UNVERIFIED  logs/final_explanation_issues/<module>.json exists and is not
             status=cleared: the reviewer found issues that a human has not yet
             accepted (python3 scripts/rebuild_consistency.py --clear <module> --by NAME)
  DOCS       a docx of the set is missing, or the student Final Explanation
             contains exemplar text (the student/teacher split failed)

WARNINGS
  FE-NUMBERS table cells in the Final Explanation whose numbers appear nowhere
             in the lessons (informational; a fresh worked example is legitimate)

Not machine-checkable here: arithmetic inside a Final Explanation. That is what
the reviewer call in generate_final_explanation() is for.

Usage:
  python3 scripts/validate_consistency.py                  # whole corpus
  python3 scripts/validate_consistency.py path/to/X_data.json [...]
  python3 scripts/validate_consistency.py --quiet
"""
import glob
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "outputs" / "v2"
ISSUES = ROOT / "logs" / "final_explanation_issues"

LEAK = re.compile(r"\[\s*re-?calc|re-calculation|(?:^|[.!?\]\"']\s+)wait[,.!]|let me (?:re|try|check|redo)|"
                  r"\bactually,|\bhmm\b|correction:|on second thought", re.I)
# Labelled characters/objects a dataset is told through ("Runner B", "Sample C").
# Nouns that are also curriculum terms followed by a letter (Group V, Class A
# in a taxonomy, Plant X) are deliberately left out: they are not characters.
ENTITY = re.compile(r"\b(Runner|Sample|Beaker|Team|Car|Cyclist|Object|Trial|Experiment|"
                    r"Test tube|Tube|Solution|Athlete|Bus|Train|Farmer|Shop|Tank|Pipe|Wire|Ball|Block)\s([A-Z])\b")
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])")


_PREFIX_MAP = {}


def module_of_prefix() -> dict:
    """filePrefix -> generators/data module name, scanned from the data modules."""
    if not _PREFIX_MAP:
        for f in (ROOT / "generators" / "data").glob("*_data.js"):
            m = re.search(r"filePrefix:\s*['\"]([^'\"]+)['\"]|\"filePrefix\":\s*\"([^\"]+)\"", f.read_text())
            if m:
                _PREFIX_MAP[m.group(1) or m.group(2)] = f.name.removesuffix("_data.js")
    return _PREFIX_MAP


def text_of(docx: Path) -> str:
    x = zipfile.ZipFile(docx).read("word/document.xml").decode("utf8", "ignore")
    return " ".join(re.findall(r"<w:t[^>]*>([^<]*)", x))


def lesson_blob(d: dict) -> str:
    parts = [json.dumps(d.get("UNIT", {}), ensure_ascii=False)]
    for l in d.get("LESSONS", []):
        parts.append(json.dumps({k: v for k, v in l.items() if k != "resourceLinks"}, ensure_ascii=False))
    return " ".join(parts)


def check(path: Path, quiet: bool):
    fails, warns = [], []
    d = json.loads(path.read_text())
    name = path.name.removesuffix("_data.json")
    where = str(path.relative_to(ROOT))
    L, ST, FE = d.get("LESSONS", []), d.get("SUMMARY_TABLE") or {}, d.get("FINAL_EXPLANATION")

    # Summary Table vs lessons
    rows = ST.get("lessons", [])
    if len(rows) != len(L):
        fails.append(f"ST-COUNT {where}: {len(L)} lessons, Summary Table has {len(rows)}")
    for l, r in zip(L, rows):
        if r.get("number") != l.get("number") or (r.get("title") or "").strip() != (l.get("title") or "").strip():
            fails.append(f"ST-TITLE {where} L{l.get('number')}: {l.get('title')!r} vs {r.get('title')!r}")
            continue
        stp = l.get("summaryTablePrompt") or {}
        for k in ("observed", "learned", "explained"):
            if (r.get(k) or "").strip() != (stp.get(k) or "").strip():
                fails.append(f"ST-TEXT {where} L{l.get('number')}.{k}: differs from the lesson's summaryTablePrompt")
                break

    # Final Explanation
    if not FE or len(FE.get("sections", [])) < 3 or any(
            not (s.get("prompt") or "").strip() or not (s.get("exemplar") or "").strip()
            for s in FE.get("sections", [])):
        fails.append(f"FE-EMPTY {where}: Final Explanation missing, <3 sections, or an empty prompt/exemplar")
    else:
        fe_text = json.dumps(FE, ensure_ascii=False)
        gm = re.search(r"Grade\s+(\d+)", FE.get("subjectLabel", ""))
        mg = str((d.get("META") or {}).get("grade", ""))
        if gm and mg and gm.group(1) != mg:
            fails.append(f"FE-GRADE {where}: label says Grade {gm.group(1)}, sub-strand is Grade {mg}")
        m = LEAK.search(fe_text)
        if m:
            fails.append(f"FE-LEAK {where}: {m.group(0)!r} in the Final Explanation")
        for s in FE["sections"]:
            for field in ("prompt", "exemplar"):
                # Each contiguous run of pipe rows is one table: exactly one
                # separator row, and no glued '||'.
                blocks, cur = [], []
                for ln in s[field].split("\n"):
                    if ln.strip().startswith("|"):
                        cur.append(ln.strip())
                    elif cur:
                        blocks.append(cur)
                        cur = []
                if cur:
                    blocks.append(cur)
                for blk in blocks:
                    if len(blk) < 2:      # a lone line starting with | is maths (|a| = 5), not a table
                        continue
                    seps = [ln for ln in blk if re.fullmatch(r"\|[\s:\-|]+\|?", ln)]
                    if "||" in "\n".join(blk).replace("|\n|", "") or len(seps) != 1:
                        fails.append(f"FE-TABLE {where} {s['title'][:40]!r} {field}: malformed table "
                                     f"({len(seps)} separator rows, {len(blk)} rows)")
                        break
        blob = lesson_blob(d)
        ents = {"".join(e) if isinstance(e, tuple) else e for e in
                (f"{a} {b}" for a, b in ENTITY.findall(fe_text))}
        for e in sorted(ents):
            if e not in blob:
                fails.append(f"FE-ENTITY {where}: {e!r} appears in the Final Explanation but in no lesson")
        lesson_nums = set(NUM.findall(blob))
        for s in FE["sections"]:
            for ln in s["prompt"].split("\n"):
                if ln.strip().startswith("|") and not re.fullmatch(r"\|[\s:\-|]+\|?", ln.strip()):
                    nums = [n for n in NUM.findall(ln) if len(n) >= 2]
                    if nums and not any(n in lesson_nums for n in nums):
                        warns.append(f"FE-NUMBERS {where}: table row {ln.strip()[:60]!r} shares no number with the lessons")
                        break

    # Issue logs are keyed by data-module name (bio_1_1); map this file to it.
    modname = module_of_prefix().get((d.get("META") or {}).get("filePrefix", name), name)
    flag = next((p_ for p_ in (ISSUES / f"{modname}.json", ISSUES / f"{name}.json") if p_.exists()), None)
    if flag is not None and json.loads(flag.read_text()).get("status") != "cleared":
        fails.append(f"FE-UNVERIFIED {where}: reviewer found unresolved contradictions "
                     f"(logs/final_explanation_issues/{modname}.json)")

    # The document set on disk
    base = path.parent
    prefix = (d.get("META") or {}).get("filePrefix", name)
    expected = [f"{prefix}_CBE_LessonSequence.docx", f"{prefix}_SummaryTable.docx",
                f"{prefix}_FinalExplanation.docx", f"{prefix}_FinalExplanation_TeacherKey.docx"]
    for e in expected:
        if not (base / e).exists():
            fails.append(f"DOCS {where}: missing {e}")
    stu = base / f"{prefix}_FinalExplanation.docx"
    if stu.exists() and FE and FE.get("sections"):
        t = re.sub(r"\s+", " ", text_of(stu))
        for s in FE["sections"]:
            ex = re.sub(r"\s+", " ", (s.get("exemplar") or "")).strip()
            if len(ex) > 60 and ex[:60] in t and ex[:60] not in re.sub(r"\s+", " ", s.get("prompt") or ""):
                fails.append(f"DOCS {where}: student Final Explanation contains exemplar text ({s['title'][:40]!r})")
                break
    return fails, warns


def main(argv):
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    files = [Path(a).resolve() for a in args] if args else \
        sorted(Path(p) for p in glob.glob(str(OUT / "**" / "*_data.json"), recursive=True)
               if "/PDF/" not in p)
    allf, allw = [], []
    for f in files:
        fl, wl = check(f, quiet)
        allf += fl
        allw += wl
    kinds = {}
    for x in allf:
        kinds[x.split()[0]] = kinds.get(x.split()[0], 0) + 1
    print(f"validate_consistency: {len(files)} file(s)")
    print("  hard failures: " + ("none" if not allf else "  ".join(f"{k}={v}" for k, v in sorted(kinds.items()))))
    print(f"  warnings: {len(allw)}")
    for w in allw[: (5 if quiet else 40)]:
        print(f"  WARN {w}")
    for x in allf[:150]:
        print(f"  FAIL {x}")
    if len(allf) > 150:
        print(f"  ... {len(allf) - 150} more failures")
    return 1 if allf else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
