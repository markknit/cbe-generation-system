#!/usr/bin/env python3
"""
make_tracked_docx.py — turn (original.docx, revised.docx) into ONE docx with real Word tracked changes
=====================================================================================================
Both inputs are rendered by the same generator, so their paragraph structure lines up. Paragraphs are
aligned (difflib), then compared word by word:  words only in the original become <w:del>, words only in
the revised become <w:ins>, so Word's Review pane shows who changed what and a teacher can accept or reject
each change.  Accept All = the revised document; Reject All = the original (both are verified here).

  python3 scripts/make_tracked_docx.py ORIGINAL.docx REVISED.docx OUT.docx [--author NAME] [--verify]
"""
import argparse
import copy
import datetime
import difflib
import re
import sys
import zipfile
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % W_NS
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
TOKEN = re.compile(r"\s+|\w+|[^\w\s]", re.U)


def q(tag):
    return W + tag


class Ids:
    def __init__(self, author, date):
        self.n = 9000
        self.author, self.date = author, date

    def attrs(self, el):
        self.n += 1
        el.set(q("id"), str(self.n))
        el.set(q("author"), self.author)
        el.set(q("date"), self.date)
        return el


def run_text(r):
    out = []
    for c in r:
        if c.tag == q("t"):
            out.append(c.text or "")
        elif c.tag == q("tab"):
            out.append("\t")
        elif c.tag == q("br"):
            out.append("\n")
    return "".join(out)


def para_text(p):
    return "".join(run_text(r) for r in p.iter(q("r")) if not any(a.tag in (q("del"),) for a in r.iterancestors()))


def simple(p):
    """A paragraph whose only content children are plain runs (so it can be re-flowed safely)."""
    return all(c.tag in (q("pPr"), q("r")) for c in p)


def chars(p):
    out = []
    for r in p.findall(q("r")):
        rpr = r.find(q("rPr"))
        for ch in run_text(r):
            out.append((ch, rpr))
    return out


def make_run(text, rpr, deleted=False):
    r = etree.Element(q("r"))
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    parts = re.split(r"(\t|\n)", text)
    for part in parts:
        if part == "\t":
            etree.SubElement(r, q("tab"))
        elif part == "\n":
            etree.SubElement(r, q("br"))
        elif part:
            t = etree.SubElement(r, q("delText" if deleted else "t"))
            t.text = part
            t.set(XML_SPACE, "preserve")
    return r


def runs_from(chs, deleted=False):
    """Group consecutive chars with the same rPr into runs."""
    out, cur, key = [], [], None
    for ch, rpr in chs:
        k = etree.tostring(rpr) if rpr is not None else b""
        if cur and k != key:
            out.append(make_run("".join(c for c, _ in cur), cur[0][1], deleted)); cur = []
        key = k
        cur.append((ch, rpr))
    if cur:
        out.append(make_run("".join(c for c, _ in cur), cur[0][1], deleted))
    return out


def wrap(kind, runs, ids):
    el = ids.attrs(etree.Element(q(kind)))
    for r in runs:
        el.append(r)
    return el


def mark_para(p, kind, ids):
    ppr = p.find(q("pPr"))
    if ppr is None:
        ppr = etree.Element(q("pPr"))
        p.insert(0, ppr)
    rpr = ppr.find(q("rPr"))
    if rpr is None:
        rpr = etree.SubElement(ppr, q("rPr"))
    rpr.insert(0, ids.attrs(etree.Element(q(kind))))


def whole_inserted(p, ids):
    runs = [c for c in p if c.tag == q("r")]
    others = [c for c in p if c.tag not in (q("pPr"), q("r"))]
    for r in runs:
        idx = p.index(r)
        p.remove(r)
        p.insert(idx, wrap("ins", [r], ids))
    for o in others:      # hyperlinks etc.: wrap their runs
        for r in list(o.iter(q("r"))):
            par = r.getparent()
            i = par.index(r)
            par.remove(r)
            par.insert(i, wrap("ins", [r], ids))
    mark_para(p, "ins", ids)


def deleted_clone(old_p, ids):
    p = copy.deepcopy(old_p)
    for r in list(p.iter(q("r"))):
        for t in r.findall(q("t")):
            t.tag = q("delText")
            t.set(XML_SPACE, "preserve")
        par = r.getparent()
        i = par.index(r)
        par.remove(r)
        par.insert(i, wrap("del", [r], ids))
    mark_para(p, "del", ids)
    return p


def merge_ops(ops, otok):
    """Absorb short unchanged gaps (<= 2 words) between two changes, so edits read as phrases, not confetti."""
    out = []
    for op in ops:
        out.append(list(op))
    merged = []
    for k, op in enumerate(out):
        tag, i1, i2, j1, j2 = op
        gap = tag == "equal" and 0 < k < len(out) - 1 and sum(1 for t in otok[i1:i2] if t.strip()) <= 2
        if gap:
            op = ["replace", i1, i2, j1, j2]
        if merged and merged[-1][0] != "equal" and op[0] != "equal":
            m = merged[-1]
            merged[-1] = ["replace", m[1], op[2], m[3], op[4]]
        else:
            merged.append(op)
    return [tuple(m) for m in merged]


def word_diff(old_p, new_p, ids):
    """Rewrite new_p's content as tracked word-level changes against old_p. Returns False if not possible."""
    if not (simple(old_p) and simple(new_p)):
        return False
    oc, nc = chars(old_p), chars(new_p)
    ot, nt = "".join(c for c, _ in oc), "".join(c for c, _ in nc)
    otok, ntok = TOKEN.findall(ot), TOKEN.findall(nt)
    # token -> char offsets
    def offs(toks):
        o, pos = [], 0
        for t in toks:
            o.append(pos); pos += len(t)
        o.append(pos)
        return o
    oo, no = offs(otok), offs(ntok)
    sm = difflib.SequenceMatcher(None, otok, ntok, autojunk=False)
    ops = merge_ops(sm.get_opcodes(), otok)
    if sm.ratio() < 0.5:                       # mostly rewritten: show one deletion + one insertion
        ops = [("replace", 0, len(otok), 0, len(ntok))]
    content = []
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            content += runs_from(nc[no[j1]:no[j2]])
            continue
        if i2 > i1:
            content.append(wrap("del", runs_from(oc[oo[i1]:oo[i2]], deleted=True), ids))
        if j2 > j1:
            content.append(wrap("ins", runs_from(nc[no[j1]:no[j2]]), ids))
    for r in new_p.findall(q("r")):
        new_p.remove(r)
    for c in content:
        new_p.append(c)
    return True


def ratio(a, b):
    if not a and not b:
        return 1.0
    s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    if s.real_quick_ratio() < 0.45 or s.quick_ratio() < 0.45:
        return 0.0
    return s.ratio()


def build(orig_xml, new_xml, ids):
    ot, nt = etree.fromstring(orig_xml), etree.fromstring(new_xml)
    op, np_ = list(ot.iter(q("p"))), list(nt.iter(q("p")))
    otxt, ntxt = [para_text(p) for p in op], [para_text(p) for p in np_]
    sm = difflib.SequenceMatcher(None, otxt, ntxt, autojunk=False)
    stats = {"changed": 0, "inserted": 0, "deleted": 0, "fallback": 0}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        i = i1
        pending_del = []
        pairs = []          # (old_idx or None, new_idx or None) in order
        for j in range(j1, j2):
            best, bi = 0.0, None
            for k in range(i, i2):
                r_ = ratio(otxt[k], ntxt[j])
                if r_ > best:
                    best, bi = r_, k
            if bi is not None and best >= 0.5:
                for k in range(i, bi):
                    pairs.append((k, None))
                pairs.append((bi, j))
                i = bi + 1
            else:
                pairs.append((None, j))
        for k in range(i, i2):
            pairs.append((k, None))
        # emit: walk pairs; deleted paragraphs go before the next new paragraph (or after the last one)
        for idx, (o_i, n_j) in enumerate(pairs):
            if o_i is not None and n_j is not None:
                if otxt[o_i] == ntxt[n_j]:
                    continue
                if word_diff(op[o_i], np_[n_j], ids):
                    stats["changed"] += 1
                else:
                    stats["fallback"] += 1
                    pending_del.append(op[o_i])
                    whole_inserted(np_[n_j], ids)
            elif n_j is not None:
                if ntxt[n_j].strip() or True:
                    whole_inserted(np_[n_j], ids)
                    stats["inserted"] += 1
            else:
                pending_del.append(op[o_i])
                stats["deleted"] += 1
            # flush deletions before the next new paragraph in this block
            nxt = next((nj for _, nj in pairs[idx + 1:] if nj is not None), None)
            if pending_del and (nxt is not None or idx == len(pairs) - 1):
                anchor_j = nxt if nxt is not None else None
                tail = None        # keeps several trailing deletions in their original order
                for d in pending_del:
                    dc = deleted_clone(d, ids)
                    if anchor_j is not None:
                        np_[anchor_j].addprevious(dc)
                    else:
                        if tail is None:
                            last = next((nj for _, nj in reversed(pairs) if nj is not None), None)
                            if last is not None:
                                np_[last].addnext(dc)
                            else:
                                np_[min(j1, len(np_) - 1)].addprevious(dc)
                        else:
                            tail.addnext(dc)
                        tail = dc
                pending_del = []
    return etree.tostring(nt, xml_declaration=True, encoding="UTF-8", standalone=True), stats


# ---------- verification ----------
def paragraphs_view(xml, mode):
    """mode 'accept': deletions removed, insertions kept. 'reject': insertions removed, deletions kept."""
    root = etree.fromstring(xml)
    out = []
    for p in root.iter(q("p")):
        ppr = p.find(q("pPr"))
        mark = None
        if ppr is not None and ppr.find(q("rPr")) is not None:
            for k in ("ins", "del"):
                if ppr.find(q("rPr")).find(q(k)) is not None:
                    mark = k
        if (mode == "accept" and mark == "del") or (mode == "reject" and mark == "ins"):
            continue
        text = []
        for r in p.iter(q("r")):
            anc = {a.tag for a in r.iterancestors()}
            if mode == "accept" and q("del") in anc:
                continue
            if mode == "reject" and q("ins") in anc:
                continue
            for c in r:
                if c.tag in (q("t"), q("delText")):
                    text.append(c.text or "")
                elif c.tag == q("tab"):
                    text.append("\t")
                elif c.tag == q("br"):
                    text.append("\n")
        out.append("".join(text))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original"); ap.add_argument("revised"); ap.add_argument("out")
    ap.add_argument("--author", default="Claude (AI) - proposed")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    zo, zn = zipfile.ZipFile(a.original), zipfile.ZipFile(a.revised)
    orig_xml, new_xml = zo.read("word/document.xml"), zn.read("word/document.xml")
    out_xml, stats = build(orig_xml, new_xml, Ids(a.author, date))
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zn.infolist():
            zout.writestr(item, out_xml if item.filename == "word/document.xml" else zn.read(item.filename))
    print(f"{a.out}: {stats}")
    if a.verify:
        ok = True
        want_new = [para_text(p) for p in etree.fromstring(new_xml).iter(q("p"))]
        want_old = [para_text(p) for p in etree.fromstring(orig_xml).iter(q("p"))]
        got_new, got_old = paragraphs_view(out_xml, "accept"), paragraphs_view(out_xml, "reject")
        if got_new != want_new:
            ok = False; print("  VERIFY FAIL: Accept All != revised document")
        if got_old != want_old:
            ok = False; print("  VERIFY FAIL: Reject All != original document")
        print("  verify:", "Accept All = revised, Reject All = original" if ok else "FAILED")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
