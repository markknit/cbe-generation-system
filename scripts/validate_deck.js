#!/usr/bin/env node
'use strict';
/**
 * validate_deck.js — independent validator for one lesson deck. It re-reads the finished .pptx (it does not
 * trust the builder) plus the authored spec and the lesson data, and checks the Manual's section 13
 * self-check as modified by docs/presentations/OVERRIDES.md. Exit 1 if any ERROR; warnings are reported.
 *
 *   node scripts/validate_deck.js <deck.pptx> <spec.json> <data.json> <lessonNo> [--manifest out.json] [--golden golden.json] [--json]
 *
 * Link-gate (scripts/check_resource_links.py) is run separately on the lesson data JSON by the pipeline.
 */
const fs = require('fs');
const JSZip = require('jszip');
const { CFG, PHASE_ORDER } = require('../generators/presentations/lib/theme');
const { deckAttribution, footerText } = require('../generators/presentations/lib/attr');
const { resourceIndex } = require('../generators/presentations/lib/resources');
const { lessonLength } = require('../generators/presentations/build_deck');
const { drivingQuestion } = require('../generators/presentations/lib/unit');
const { iconPath, unknownIconPrefixes } = require('../generators/presentations/lib/icons');
const { artPath } = require('../generators/presentations/lib/art');

const NOTE_ORDER = ['PHASE', 'TIME', 'DO', 'SAY', 'WAIT TIME', 'LOOK FOR', 'IF…', 'WHY THIS WORKS', 'ANSWER KEY', 'SCIENCE NOTE FOR YOU', 'RESOURCE LINKS', 'TEACHER REFLECTION'];
const US_SPELL = /\b(color|colors|colored|specialization|specialized|aluminum|center|centers|meter(?!s? reading)|liter|fiber|organize[sd]?|analyze[sd]?|behavior|favorite|neighbor|gray|recognize[sd]?|summarize[sd]?|catalog)\b/i;
const LABEL_RE = /^(TIME:|DO$|SAY$|WAIT TIME$|LOOK FOR$|IF…$|WHY THIS WORKS$|ANSWER KEY$|SCIENCE NOTE FOR YOU$|RESOURCE LINKS|TEACHER REFLECTION$|[A-Z][A-Z ]+ PHASE \(|DRIVING QUESTION BOARD \()/;

const dec = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&');
const texts = xml => [...xml.matchAll(/<a:t>([^<]*)<\/a:t>/g)].map(m => dec(m[1]));
const paraTexts = xml => [...xml.matchAll(/<a:p>([\s\S]*?)<\/a:p>/g)].map(m => texts(m[1]).join(''));

async function readDeck(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const pres = await zip.file('ppt/presentation.xml').async('string');
  const rels = await zip.file('ppt/_rels/presentation.xml.rels').async('string');
  const relTarget = {};
  for (const m of rels.matchAll(/<Relationship [^>]*>/g)) { const id = /Id="([^"]+)"/.exec(m[0]), t = /Target="([^"]+)"/.exec(m[0]); if (id && t) relTarget[id[1]] = t[1]; }
  const order = [...pres.matchAll(/<p:sldId [^>]*r:id="([^"]+)"/g)].map(m => relTarget[m[1]]);
  const slides = [];
  for (const t of order) {
    const sp = 'ppt/' + t.replace(/^\.?\//, '');
    const xml = await zip.file(sp).async('string');
    const relP = sp.replace('slides/', 'slides/_rels/') + '.rels';
    const rel = zip.file(relP) ? await zip.file(relP).async('string') : '';
    const ext = {}, notesRel = [];
    for (const m of rel.matchAll(/<Relationship [^>]*>/g)) {
      const id = /Id="([^"]+)"/.exec(m[0])[1], tg = /Target="([^"]+)"/.exec(m[0])[1];
      if (/TargetMode="External"/.test(m[0])) ext[id] = dec(tg); if (/notesSlide/.test(m[0])) notesRel.push(tg);
    }
    const links = [...xml.matchAll(/<a:hlinkClick[^>]*r:id="([^"]+)"/g)].map(m => ext[m[1]]).filter(Boolean);
    let notesXml = '';
    if (notesRel.length) notesXml = await zip.file('ppt/' + notesRel[0].replace(/^\.\.\//, '')).async('string');
    const bodyM = /<p:ph[^>]*type="body"[^>]*\/>[\s\S]*?<p:txBody>([\s\S]*?)<\/p:txBody>/.exec(notesXml);
    const notes = bodyM ? paraTexts(bodyM[1]) : [];
    const alts = [...xml.matchAll(/<p:cNvPr [^>]*descr="([^"]*)"/g)].map(m => dec(m[1]));
    const sizes = [...xml.matchAll(/<a:rPr[^>]*\bsz="(\d+)"[^>]*>/g)].map(m => +m[1] / 100);
    const fonts = new Set([...xml.matchAll(/typeface="([^"]+)"/g)].map(m => m[1]));
    slides.push({ path: sp, xml, hidden: /<p:sld [^>]*show="0"/.test(xml), text: texts(xml), notes, links, alts, sizes, fonts });
  }
  return slides;
}

async function validate({ deck, specP, dataP, lessonNo, opts = {} }) {
  const issues = [];
  const E = (id, slide, msg) => issues.push({ severity: 'ERROR', id, slide, msg });
  const W = (id, slide, msg) => issues.push({ severity: 'warn', id, slide, msg });
  const spec = JSON.parse(fs.readFileSync(specP, 'utf8')), data = JSON.parse(fs.readFileSync(dataP, 'utf8'));
  const lesson = data.LESSONS.find(l => l.number === lessonNo), len = lessonLength(lesson), meta = data.META;
  const slides = await readDeck(deck);
  const attr = deckAttribution(), res = resourceIndex(lesson), urls = new Set(res.map(r => r.url));
  const kindOf = (s, i) => {
    const t = s.text.join(' ');
    if (i === 0) return 'title'; if (/How these lessons work/.test(t)) return 'how'; if (/at a glance/.test(t)) return 'glance'; if (/ARES resources for Lesson/.test(t)) return 'resources';
    if (/Where we are in the unit/.test(t)) return 'unitmap'; if (/By the end of this lesson/.test(t)) return 'goals';
    if (/SAFETY FIRST/.test(t)) return 'safety'; if (/^Summary Table: Lesson/.test(s.text.find(x => /Summary Table: Lesson/.test(x)) || '') && i === slides.length - 1) return 'summary';
    return 'phase';
  };
  const kinds = slides.map(kindOf);

  // --- S1: order and hidden flags (Manual s5)
  const expectHead = ['title', 'how', 'glance', ...(res.length ? ['resources'] : []), 'unitmap', 'goals'];
  expectHead.forEach((k, i) => { if (kinds[i] !== k) E('S1', i + 1, `slide ${i + 1} should be '${k}', found '${kinds[i]}'`); });
  if (kinds[kinds.length - 1] !== 'summary') E('S1', slides.length, 'last slide must be the Summary Table');
  const hasSafety = kinds[expectHead.length] === 'safety';
  if (spec.is_practical && !hasSafety) E('S12', 6, 'practical lesson without a Safety slide (Manual s9)');
  if (!spec.is_practical && hasSafety) W('S12', 6, 'Safety slide on a lesson not flagged as a practical');
  slides.forEach((s, i) => { const want = kinds[i] === 'how' || kinds[i] === 'glance' || kinds[i] === 'resources'; if (s.hidden !== want) E('S1', i + 1, `slide ${i + 1} (${kinds[i]}) hidden=${s.hidden}, expected ${want}`); });
  const firstPhase = kinds.indexOf('phase');
  const phaseSeq = slides.map((s, i) => (kinds[i] === 'phase' ? PHASE_ORDER.find(k => s.text.includes(CFG.phases[k].label.toUpperCase())) : null));
  let last = -1;
  slides.forEach((s, i) => { if (kinds[i] !== 'phase') return; const k = phaseSeq[i]; if (!k) { E('S6', i + 1, 'phase slide without a recognised phase pill'); return; } const idx = PHASE_ORDER.indexOf(k); if (idx < last) E('S6', i + 1, `phase '${k}' appears after a later phase (SoW order is Predict, Observe, Explain, Driving Question Board, Model Building)`); last = Math.max(last, idx); });
  for (const k of PHASE_ORDER) if (!phaseSeq.includes(k)) E('S6', 0, `no slide for phase '${k}' (Manual s13: DQB and Model Building must be in the lesson)`);

  // --- S2/S3: notes on every slide, fixed label order; checks carry LOOK FOR and IF…
  slides.forEach((s, i) => {
    if (!s.notes.length || !s.notes.join('').trim()) { E('S2', i + 1, 'no speaker notes'); return; }
    const labs = [];
    s.notes.forEach(l => { const m = LABEL_RE.exec(l); if (!m) return; const t = m[1]; labs.push(/PHASE \(|^DRIVING QUESTION BOARD \(/.test(t) ? 'PHASE' : t.replace(':', '').replace(/ \(.*/, '')); });
    const idxs = labs.map(l => NOTE_ORDER.findIndex(n => l.startsWith(n))).filter(x => x >= 0);
    for (let k = 1; k < idxs.length; k++) if (idxs[k] < idxs[k - 1]) { E('S2', i + 1, `notes labels out of order: ${labs.join(' > ')}`); break; }
    const slideText = s.text.join(' ');
    if (!['title', 'how', 'glance', 'resources'].includes(kinds[i]) && !labs.includes('TIME')) E('S2', i + 1, 'notes have no TIME line');
    if (/CHECK FOR UNDERSTANDING/.test(slideText) && kinds[i] === 'phase') { if (!labs.includes('LOOK FOR')) E('S3', i + 1, 'check for understanding without LOOK FOR'); if (!labs.includes('IF…')) E('S3', i + 1, 'check for understanding without IF…'); }
  });

  // --- phase-total headers and minutes (Manual s13 first two ticks)
  const specSlides = spec.slides, byPhase = {};
  specSlides.forEach(sl => { byPhase[sl.phase] = (byPhase[sl.phase] || 0) + sl.minutes; });
  const total = spec.unit_map_minutes + spec.goals_minutes + (spec.safety.rules.length ? spec.safety.minutes : 0) + specSlides.reduce((a, s) => a + s.minutes, 0) + spec.summary.minutes;
  if (total !== len) E('S4', 0, `slide TIME lines add up to ${total} minutes; lesson is ${len}`);
  const gl = {}; spec.glance.rows.forEach(r => { gl[r.group] = (gl[r.group] || 0) + r.minutes; });
  for (const k of PHASE_ORDER) if ((gl[k] || 0) !== (byPhase[k] || 0)) E('S4', 0, `glance says ${gl[k] || 0} min for ${k}, slides say ${byPhase[k] || 0}`);
  const openMin = spec.unit_map_minutes + spec.goals_minutes + (spec.safety.rules.length ? spec.safety.minutes : 0);
  if ((gl.opening || 0) !== openMin) E('S4', 0, `glance says ${gl.opening || 0} min for opening, slides say ${openMin}`);
  if ((gl.summary || 0) !== spec.summary.minutes) E('S4', 0, `glance says ${gl.summary || 0} min for summary, slides say ${spec.summary.minutes}`);
  const timers = specSlides.forEach((sl, i) => { for (const t of sl.timers) { const m = /^(\d+):(\d\d)$/.exec(t.time); if (!m) E('S4', 0, `timer '${t.time}' on '${sl.title}' is not m:ss`); else if (+m[1] > sl.minutes) W('S4', 0, `timer ${t.time} on '${sl.title}' exceeds the slide time (${sl.minutes} min)`); } });
  for (const k of PHASE_ORDER) { const want = new RegExp(`^${CFG.phases[k].label.toUpperCase()}${k === 'dqb' ? '' : ' PHASE'} \\(${byPhase[k]} minutes? total\\)$`); const hit = slides.some(s => s.notes.some(l => want.test(l))); if (byPhase[k] !== undefined && !hit) E('S4', 0, `no notes line 'PHASE (${byPhase[k]} minutes total)' for ${k}`); }

  // --- student tasks have an ANSWER KEY (spec-level)
  specSlides.forEach(sl => { if (sl.student_task && !(sl.notes.answer_key || []).filter(x => x.trim()).length) E('S5', 0, `student task slide '${sl.title}' has no ANSWER KEY`); });
  specSlides.forEach(sl => { if (sl.check_for_understanding && (!sl.notes.look_for.length || !sl.notes.if_then.length)) E('S3', 0, `'${sl.title}': check needs look_for and if_then`); });
  if (spec.goals.length > 3 || !spec.goals.length) E('S7', 5, `goals: ${spec.goals.length} (1-3 allowed)`);
  if (spec.safety.rules.length > 5) E('S7', 6, 'more than five safety rules');
  if (spec.key_words.length > 6) W('S7', 5, 'more than six key words');

  // --- footer + logos on every slide; text from attribution.yaml
  slides.forEach((s, i) => {
    const full = i === 0 || i === slides.length - 1, want = footerText(attr, meta, lessonNo, full);
    if (!s.text.some(t => t.trim() === want)) E('S8', i + 1, `footer text missing or not equal to attribution output${full ? ' (full lesson_footer expected on title and last slide)' : ''}`);
    if (!s.alts.includes('SeaVuria logo') || !s.alts.includes('ARES Education logo')) E('S8', i + 1, 'both logos (by alt text) must be on every slide');
  });
  // --- fonts (Calibri only) and text size floor
  slides.forEach((s, i) => {
    for (const f of s.fonts) if (!/^(Calibri|\+mn-lt|\+mj-lt)$/.test(f)) E('S9', i + 1, `font '${f}' (Calibri only, Manual s4)`);
    if (s.hidden) return;
    const small = s.sizes.filter(p => p < 10); if (small.length) E('S9', i + 1, `text below 10pt: ${[...new Set(small)].join(',')}`);
    const mid = s.sizes.filter(p => p >= 10 && p < 14 && p !== 10 && p !== 11 && p !== 12); if (mid.length && kinds[i] === 'phase') W('S9', i + 1, `small text sizes: ${[...new Set(mid)].join(',')}`);
  });
  // --- phase colour on the pill
  slides.forEach((s, i) => {
    if (kinds[i] !== 'phase') return; const k = phaseSeq[i]; if (!k) return;
    const label = CFG.phases[k].label.toUpperCase(), at = s.xml.indexOf(`<a:t>${label}</a:t>`);
    if (at < 0) return;
    const before = s.xml.slice(0, at), spStart = before.lastIndexOf('<p:sp>'), prev = before.slice(before.lastIndexOf('<p:sp>', spStart - 1), spStart);
    if (!prev.includes(CFG.phases[k].hex)) E('S10', i + 1, `phase pill colour is not ${CFG.phases[k].hex} (${k})`);
  });
  // --- links (Overrides 2/3): only ares.local links of this lesson's resourceLinks; icon alt text; URL also in notes
  slides.forEach((s, i) => {
    for (const u of s.links) {
      if (!urls.has(u)) E('L1', i + 1, `hyperlink not in this lesson's resourceLinks: ${u}`);
      if (!/^http:\/\/ares\.local/.test(u)) E('L1', i + 1, `non-ares.local link: ${u}`);
      if (!s.notes.some(l => l.includes(u))) E('L2', i + 1, `link URL not repeated in the notes (printed copies keep it): ${u}`);
    }
    const pics = (s.xml.match(/<p:pic>[\s\S]*?<\/p:pic>/g) || []);
    for (const p of pics) if (/hlinkClick/.test(p) && !/descr="[^"]+"/.test(p)) E('L3', i + 1, 'linked icon without alt text');
    const all = s.text.join(' ') + ' ' + s.notes.join(' ');
    if (/REPLACE-WITH|ares\.edu|\bTODO\b|\bFILL\b/.test(all) || /lorem ipsum/i.test(all)) E('L4', i + 1, 'placeholder or dead host in text');
  });
  spec.glance.resource_notes.forEach(r => { if (r.match === 'use_later' && !/after|in lesson|later|revision|once|when/i.test(r.note)) W('L6', 3, `use_later note for ${r.key} does not say when to use it`); });
  const noteKeys = new Set(spec.glance.resource_notes.map(r => r.key));
  const knownKeys = new Set(res.flatMap(r => [r.key, ...r.also]));
  res.forEach(r => { if (!noteKeys.has(r.key)) E('L5', 3, `resource ${r.key} has no match note on the glance slide (Manual s10)`); });
  for (const k of noteKeys) if (!knownKeys.has(k)) E('L5', 3, `match note for unknown resource key '${k}' (never invent resources)`);
  specSlides.forEach(sl => (sl.resources || []).forEach(k => { const n = spec.glance.resource_notes.find(r => r.key === k || (res.find(x => x.key === k) || { also: [] }).key === r.key); if (!knownKeys.has(k)) E('L5', 0, `slide '${sl.title}' uses unknown resource key '${k}'`); if (n && n.match === 'do_not_use') E('L5', 0, `slide '${sl.title}' shows a DO NOT USE resource`); }));
  // --- visuals: icon names exist, illustrations exist and are limited, hero present
  { let ill = 0;
    specSlides.forEach(sl => sl.blocks.forEach(b => {
      for (const it of (b.items || [])) { const u = b.type === 'illustration' ? null : unknownIconPrefixes(it); if (u) E('V1', 0, `unknown icon '${u}' on slide '${sl.title}'`); }
      if (b.type === 'illustration') { ill++; if (!artPath(b.items[0])) E('V2', 0, `illustration '${b.items[0]}' on '${sl.title}' has not been generated`); if (!(b.text || '').trim()) E('V2', 0, `illustration '${b.items[0]}' has no alt text`); if ((b.items || []).length < 2) E('V2', 0, `illustration on '${sl.title}' needs [art_id, prompt]`); }
      if (b.type === 'tiles' && (b.items.length < 2 || b.items.length > 8)) W('V3', 0, `tiles on '${sl.title}': ${b.items.length} items`);
    }));
    if (ill > 6) W('V3', 0, `${ill} illustrations (max 6)`);
    const h = spec.hero || {}; if (!h.art_id || !artPath(h.art_id)) E('V2', 1, `hero illustration '${h.art_id}' has not been generated`); if (!iconPath(h.icon || '')) W('V1', 1, `hero.icon '${h.icon}' is not a known icon`); }
  // --- wording
  slides.forEach((s, i) => {
    if (s.hidden) return;
    const vis = s.text.join(' ');
    if (/\bDQB\b/.test(vis)) E('W1', i + 1, "'DQB' on a slide: write 'Driving Question Board' in full (Manual s4)");
    const m = US_SPELL.exec(vis + ' ' + s.notes.join(' ')); if (m) W('W2', i + 1, `US spelling '${m[1]}' (British spelling, Manual s11)`);
    if (/\bForm [1-4]\b/.test(vis + s.notes.join(' '))) E('W3', i + 1, "'Form N' (use Grade 10, Manual s11)");
  });
  // --- title slide: five phases, one-line, lesson N of M, minutes; unit map has the driving question
  const t0 = slides[0].text.join(' ');
  for (const k of PHASE_ORDER) if (!t0.includes(CFG.phases[k].label)) E('S11', 1, `title slide missing phase '${CFG.phases[k].label}'`);
  if (!t0.includes(`LESSON ${lessonNo} OF ${data.LESSONS.length}`) || !t0.includes(`${len} MINUTES`)) E('S11', 1, 'title slide kicker must show Lesson N OF M and minutes');
  if (spec.lesson_title_short && !lesson.title.includes(spec.lesson_title_short.replace(/\?$/, ''))) W('S11', 1, 'short title is not a part of the SoW lesson title');
  { const mt = spec.unit_map_titles || [], words = t => new Set(String(t).toLowerCase().match(/[a-z0-9]+/g) || []);
    if (mt.length !== data.LESSONS.length) E('S11', 4, `unit map needs ${data.LESSONS.length} short titles, spec has ${mt.length}`);
    else mt.forEach((t, i) => { const w = words(data.LESSONS[i].title); const extra = [...words(t)].filter(x => !w.has(x)); if (extra.length) E('S11', 4, `unit map title ${i + 1} '${t}' uses words not in the SoW title: ${extra.join(', ')}`); }); }
  if (!slides[kinds.indexOf('unitmap')].text.join(' ').includes(drivingQuestion(data.UNIT))) E('S11', kinds.indexOf('unitmap') + 1, 'unit map must show the unit driving question');
  if (!spec.build_log) E('B1', 0, 'no build log');

  // --- manifest / golden (structure only, not wording)
  const manifest = {
    lesson: lessonNo, lessonMinutes: len, slideCount: slides.length,
    slides: slides.map((s, i) => ({
      n: i + 1, kind: kinds[i], phase: phaseSeq[i] || null, hidden: s.hidden, cfu: /CHECK FOR UNDERSTANDING/.test(s.text.join(' ')),
      noteLabels: s.notes.filter(l => LABEL_RE.test(l)).map(l => l.replace(/:.*/, '').replace(/ \(.*/, '')), links: s.links.length,
      footer: s.text.find(t => t.includes('CC BY-NC') || t.includes('Creative Commons')) || '', logos: s.alts.filter(a => /logo$/.test(a)).sort(),
    })),
  };
  if (opts.golden) {
    const g = JSON.parse(fs.readFileSync(opts.golden, 'utf8'));
    const drift = [];
    for (const key of ['kind', 'hidden', 'logos']) manifest.slides.forEach((s, i) => { const gs = g.slides[i]; if (gs && JSON.stringify(gs[key]) !== JSON.stringify(s[key])) drift.push(`slide ${i + 1} ${key}: golden ${JSON.stringify(gs[key])}, now ${JSON.stringify(s[key])}`); });
    for (const i of [0, 1, 2, 3, 4]) { const a = manifest.slides[i], b = g.slides[i]; if (a && b && JSON.stringify(a.noteLabels) !== JSON.stringify(b.noteLabels)) drift.push(`fixed slide ${i + 1} note labels changed`); }
    drift.forEach(d => W('G1', 0, 'golden drift: ' + d));
  }
  if (opts.manifest) fs.writeFileSync(opts.manifest, JSON.stringify(manifest, null, 1));
  return { issues, manifest };
}

if (require.main === module) {
  const a = process.argv.slice(2); const flag = n => { const i = a.indexOf(n); return i >= 0 ? a[i + 1] : undefined; };
  const [deck, specP, dataP, no] = a; if (!no) { console.error('usage: validate_deck.js <deck.pptx> <spec.json> <data.json> <lessonNo> [--manifest f] [--golden f] [--json]'); process.exit(2); }
  validate({ deck, specP, dataP, lessonNo: +no, opts: { manifest: flag('--manifest'), golden: flag('--golden') } }).then(({ issues }) => {
    const errs = issues.filter(i => i.severity === 'ERROR');
    if (a.includes('--json')) console.log(JSON.stringify(issues, null, 1)); else {
      issues.forEach(i => console.log(`${i.severity === 'ERROR' ? 'ERROR' : 'warn '} ${i.id} slide ${i.slide || '-'}: ${i.msg}`));
      console.log(`${errs.length} error(s), ${issues.length - errs.length} warning(s)`);
    }
    process.exit(errs.length ? 1 : 0);
  }).catch(e => { console.error(e.stack || e.message); process.exit(2); });
}
module.exports = { validate };
