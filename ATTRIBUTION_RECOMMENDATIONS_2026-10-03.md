# Attribution — recommended changes (not yet applied)

Source: the partner's validator review of Core Mathematics 2.9 (2026-10-03,
`Editor Review output.docx`). Nothing here is wired into `config/attribution.yaml`
yet: items marked **Mark** need a decision or facts only you (or SeaVuria/ARES)
have. This is a practical review, not legal advice; the reviewer said the same.

## 1. Placement — the repository contradicts itself  (fix: wording only)

The reviewer's finding is accurate against what the repo *says*, not against
what you decided. `config/attribution.yaml` still says the full block goes "at
the TOP of every sub-strand document", while `build_docs.js` (your decision of
2026-10-01, "at the very top it read awkwardly") puts it after the overview in
the Lesson Sequence and at the end of the Summary Table and Final Explanation.

**Recommend:** keep your placement; change the stale YAML comment to say so.
If the reviewer's concern (a reader never sees it) matters to you, add one
line under the title in each document: *"Licensed CC BY-NC 4.0 — full attribution
and licence terms on page N"*. That costs one line and satisfies "visible
immediately" without moving the block. **Mark:** pick one.

## 2. Type size  (mechanical)

Footer is 7 pt (`attribution.js`: `size: 14` half-points), full block 8.5 pt
(`size: 17`), against 9 pt body text. Printed teacher copies are the use case.

**Recommend:** footer 8 pt (`size: 16`), block 9 pt (`size: 18`). Check the
lesson footers still fit on one line.

## 3. Licence summary omits two CC BY-NC 4.0 conditions  (fix the text)

The deed requires that reusers give credit, **link to the licence, and indicate
if changes were made**. Our sentence has only "appropriate credit" and
"non-commercial". Proposed replacement for the last part of the
"Licensing & Copyright" paragraph:

> You are free to copy, redistribute and adapt this material in any medium or
> format, provided you give appropriate credit, provide a link to the licence,
> indicate if changes were made, and do not use the material for commercial
> purposes. The licence text at the link above governs.

Keep the existing KICD and third-party-resource exclusions as they are; the
reviewer called them helpful.

## 4. "United States and Canada (as Afretech Aid)"  (needs facts)

It can be read as claiming Canadian 501(c)(3) status; 501(c)(3) is a US tax
status. State each legal entity once, with its own jurisdiction. Template:

> ARES Education (a US 501(c)(3) organisation and a registered NGO in Kenya,
> No. ______), also operating in Canada as Afretech Aid (______).

**Mark:** supply the exact legal names, jurisdictions and registration numbers.
I have not guessed them.

## 5. "© 2026 SeaVuria and ARES"  (needs agreement between the organisations)

This asserts joint ownership and uses a short name. If both organisations have
agreed to it, keep it but use exact legal names ("© 2026 SeaVuria and ARES
Education"). If not, use a form that matches the real arrangement, e.g.
"© 2026 SeaVuria. Produced with ARES Education." **Mark:** confirm with both.

## 6. AI disclosure vs. copyright  (a legal question)

The AI-assistance sentence is sensible and should stay. The reviewer's point
is that disclosing it does not create copyright in machine-determined text; the
US Copyright Office looks for sufficient human-authored expression, selection,
arrangement or modification. Two practical consequences:
* Word the claim as what is true: "Lesson drafting assisted by AI (Claude,
  Anthropic); sequenced, selected and edited by the educator team" — **only if
  that is accurate**; the pipeline currently has no recorded human edit step.
* Have a short legal/organisational review of the whole block before the next
  distribution, as the reviewer recommends.

## 7. Files that must change together if you accept the above

`config/attribution.yaml` (text + the stale "TOP" comment),
`generators/lib/attribution.js` (sizes), then a full re-render
(`node generators/generate.js --all`) and PDF/index rebuild. Quiz decks and
answer keys read the same config, so they pick it up on the next
`node generators/build_quiz.js`.
