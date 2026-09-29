import json, glob, re, csv
from collections import defaultdict

STOP = set("""a an the of and or for to in on with is are be by using how does do what why when
where which their its it this that as from into about over across not no yes vs versus part
1 2 3 4 introduction unit lesson properties intro basic today our does""".split())

def words(s):
    if not s: return set()
    toks = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", s.lower())
    return set(t for t in toks if t not in STOP)

ANSWER_PATTERNS = re.compile(r"answer|topical-test|kcse\s?\d{4}|exam", re.I)

# Vocabulary that is essentially never legitimate outside its home subject.
# Kept deliberately narrow (specific, unambiguous terms only) to minimise
# false positives -- this is a precision-first pass, not a recall-first one.
SUBJECT_VOCAB = {
  "Biology": {"genetics","chromosome","allele","muscle","skeletal","anatomy",
              "digestion","enzyme","hormone","nervous","kidney","liver",
              "protist","organism","photosynthesis","chlorophyll"},
  "Chemistry": {"periodic","valence","mole","molarity","stoichiometry",
                "covalent","ionic-bond","oxidation-state","ph-scale"},
  "Physics": {"voltage","resistor","capacitor","semiconductor","doppler",
              "wavelength","nuclear-decay","radioactivity"},
  "Mathematics": {"logarithm","quadratic","trigonometry","polygon","congruence",
                  "probability-distribution","matrix","vector-space"},
}
# Which subject-folders are allowed to legitimately draw on which vocab
# (General_Science integrates bio/chem/physics by KICD design, so it is
# never "foreign" to those three -- only Math is genuinely separate).
ALLOWED = {
  "Biology": {"Biology"},
  "Chemistry": {"Chemistry"},
  "Physics": {"Physics"},
  "Mathematics": {"Core_Mathematics","Essential_Mathematics","Maths"},
}
def home_folders(vocab_subject):
    if vocab_subject == "Biology": return {"Biology","General_Science"}
    if vocab_subject == "Chemistry": return {"Chemistry","General_Science"}
    if vocab_subject == "Physics": return {"Physics","General_Science"}
    if vocab_subject == "Mathematics": return {"Core_Mathematics","Essential_Mathematics","Maths"}
    return set()

files = sorted(glob.glob("data/outputs/v2/*/*/*_data.json"))
title_count = defaultdict(int)
raw_rows = []
for fp in files:
    subject = fp.split("/")[3]
    with open(fp) as f:
        d = json.load(f)
    substrand = d.get("UNIT", {}).get("substrand") or d.get("META", {}).get("substrand_name") or fp
    for lesson in d.get("LESSONS", []):
        rl = lesson.get("resourceLinks") or {}
        predict = rl.get("predict") or {}
        topic_words = words(substrand) | words(lesson.get("title","")) | words(lesson.get("aresKeywords",""))
        for kind in ("video", "reading"):
            item = predict.get(kind) or {}
            title = item.get("title", "")
            if not title: continue
            title_count[title] += 1
            raw_rows.append((subject, substrand, lesson.get("number"), lesson.get("title"), kind, title, topic_words))

tier1, tier2, tier3 = [], [], []
for subject, substrand, lnum, ltitle, kind, title, topic_words in raw_rows:
    if ANSWER_PATTERNS.search(title):
        tier1.append([subject, substrand, lnum, ltitle, kind, title, "TIER1_ANSWER_KEY", "matches answer/exam pattern"])
        continue
    rwords = words(title)
    overlap = topic_words & rwords
    if overlap:
        continue

    foreign_hits = []
    for vocab_subj, vocab in SUBJECT_VOCAB.items():
        hit = vocab & rwords
        if hit and subject not in home_folders(vocab_subj):
            foreign_hits.append((vocab_subj, hit))
    if foreign_hits:
        tier2.append([subject, substrand, lnum, ltitle, kind, title, "TIER2_WRONG_DOMAIN_VOCAB",
                      "; ".join(f"contains {vocab_subj}-specific term(s) {sorted(h)}" for vocab_subj,h in foreign_hits)
                      + f"  [title used {title_count[title]}x in corpus]"])
    elif title_count[title] >= 6:
        tier3.append([subject, substrand, lnum, ltitle, kind, title, "TIER3_VERY_HIGH_REPEAT",
                      f"generic-looking title reused {title_count[title]}x corpus-wide, no topical overlap here"])

out = "/mnt/user-data/outputs/resource_link_priority_targets.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["subject","substrand","lesson_number","lesson_title","resource_kind","resource_title","tier","reason"])
    for r in tier1: w.writerow(r)
    for r in tier2: w.writerow(r)
    for r in tier3: w.writerow(r)

print(f"TIER 1 (answer key / exam doc surfaced as resource): {len(tier1)}")
print(f"TIER 2 (title contains vocabulary from a genuinely incompatible subject): {len(tier2)}")
print(f"TIER 3 (no domain-vocab hit, but reused 6x+ corpus-wide with zero topical overlap): {len(tier3)}")
print(f"PRIORITY LIST TOTAL: {len(tier1)+len(tier2)+len(tier3)}  (down from 474 originally flagged, 1456 checked)")
print(f"Saved to {out}")
print()
print("=== TIER 2 (wrong-domain vocabulary -- highest confidence after Tier 1) ===")
for r in tier2:
    print(f"[{r[0]}] {r[1]}  L{r[2]}: {r[3]}")
    print(f"    {r[4]}: {r[5]!r}")
    print(f"    {r[7]}")
