'use strict';
// Parametric figure generators (code-drawn, editable PowerPoint shapes, no photos).
// Unlike the fixed templates in diagrams.js, a figure is built from a small JSON spec the deck author supplies:
//   geometry | grid | circuit | atoms | flow     (see FAMILY_DOCS for the spec each takes)
// The generator owns the drawing rules and checks the spec for science/maths errors (a label that contradicts
// the drawing, a voltmeter in series, electrons that do not add up). Errors go back to the authoring repair loop.
// A figure is built once into a list of primitives in a frame {w,h} (units); drawFigure() scales it into a box.
//
// Primitives (frame units, y down):
//   {t:'line',x1,y1,x2,y2,color,w,dash,arrow}   {t:'ell',cx,cy,rx,ry,fill,line,w}   {t:'rect',x,y,w,h,fill,line,w,r}
//   {t:'text',x,y,text,pt,bold,color,align,wu}  text box centred on (x,y) (align l/r anchors that edge at x), width wu units

const { widthIn, heightIn } = require('./measure');

const INK = '1A1A1A', GREY = '8A8A8A', LIGHT = 'D9D9D9';
const PALETTE = ['1F77B4', 'D62728', '2CA02C', 'FF7F0E', '9467BD', '17A2B8'];
const COLOURS = { blue: '1F77B4', red: 'D62728', green: '2CA02C', orange: 'FF7F0E', purple: '9467BD', black: INK, grey: GREY };
const col = (c, i = 0) => COLOURS[c] || PALETTE[i % PALETTE.length];

const L = (x1, y1, x2, y2, o = {}) => ({ t: 'line', x1, y1, x2, y2, color: o.color || INK, w: o.w || 1.5, dash: o.dash, arrow: o.arrow });
const E = (cx, cy, rx, ry, o = {}) => ({ t: 'ell', cx, cy, rx, ry, fill: o.fill, line: o.line === undefined ? INK : o.line, w: o.w || 1.5 });
const R = (x, y, w, h, o = {}) => ({ t: 'rect', x, y, w, h, fill: o.fill, line: o.line === undefined ? INK : o.line, w_: o.w || 1.5, r: o.r });
const T = (x, y, text, o = {}) => ({ t: 'text', x, y, text: String(text), pt: o.pt || 16, bold: !!o.bold, color: o.color || INK, align: o.align || 'c', wu: o.wu, italic: !!o.italic, tick: !!o.tick });
const polyline = (pts, o = {}) => { const out = []; for (let i = 1; i < pts.length; i++) out.push(L(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1], o)); return out; };
const arc = (cx, cy, r, a0, a1, o = {}) => { // angles in radians, screen coordinates (y down); a1 > a0 draws the short way given
  const n = Math.max(6, Math.round(Math.abs(a1 - a0) / 0.2)), pts = [];
  for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * i / n; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return polyline(pts, o);
};
const isNum = v => typeof v === 'number' && isFinite(v);
const isPt = p => Array.isArray(p) && p.length === 2 && isNum(p[0]) && isNum(p[1]);
const bbox = pts => ({ x0: Math.min(...pts.map(p => p[0])), x1: Math.max(...pts.map(p => p[0])), y0: Math.min(...pts.map(p => p[1])), y1: Math.max(...pts.map(p => p[1])) });

// ---------------------------------------------------------------- geometry
// spec: {points:{A:[x,y],...}, lines:[{a,b,label,dash,tick,color}], fill:[[names]], circles:[{c,r,label}],
//        angles:[{at,from,to,label,right}], point_labels:true, scale:'exact'|'not_to_scale'}
// Coordinates are maths coordinates (y up). 'exact' means labelled lengths and angles are checked against the drawing.
function buildGeometry(sp) {
  const errors = [], pts = sp.points || {};
  const names = Object.keys(pts);
  if (!names.length) return { errors: ['geometry: no points'] };
  for (const n of names) if (!isPt(pts[n])) errors.push(`geometry: point ${n} must be [x, y]`);
  if (errors.length) return { errors };
  const ref = (n, where) => { if (!pts[n]) { errors.push(`geometry: ${where} uses unknown point '${n}'`); return false; } return true; };
  const circles = (sp.circles || []).map(c => ({ ...c, cc: typeof c.c === 'string' ? pts[c.c] : c.c })), exact = sp.scale === 'exact';
  circles.forEach(c => { if (!isPt(c.cc) || !isNum(c.r) || c.r <= 0) errors.push('geometry: each circle needs c (point name or [x,y]) and r > 0'); });
  if (errors.length) return { errors };
  // frame: bounding box of points and circles, scaled so the larger side is 84 units
  const all = names.map(n => pts[n]);
  circles.forEach(c => all.push([c.cc[0] - c.r, c.cc[1] - c.r], [c.cc[0] + c.r, c.cc[1] + c.r]));
  const bb = bbox(all), sw = Math.max(bb.x1 - bb.x0, 1e-9), sh = Math.max(bb.y1 - bb.y0, 1e-9), k = 84 / Math.max(sw, sh), M = 14;
  const W = sw * k + 2 * M, H = sh * k + 2 * M;
  const P = p => [M + (p[0] - bb.x0) * k, M + (bb.y1 - p[1]) * k];
  const cen = P([all.reduce((a, p) => a + p[0], 0) / all.length, all.reduce((a, p) => a + p[1], 0) / all.length]);
  const out = [];
  for (const poly of sp.fill || []) { // light fill drawn as a fan of triangles is not possible; use outline plus translucent look via lines only
    poly.forEach(n => ref(n, 'fill'));
  }
  const lineLen = {};
  for (const ln of sp.lines || []) {
    if (!ref(ln.a, 'line') || !ref(ln.b, 'line')) continue;
    const a = P(pts[ln.a]), b = P(pts[ln.b]);
    out.push(L(a[0], a[1], b[0], b[1], { color: col(ln.color), w: 2.25, dash: ln.dash ? 'dash' : undefined }));
    const len = Math.hypot(pts[ln.b][0] - pts[ln.a][0], pts[ln.b][1] - pts[ln.a][1]);
    if (ln.tick) { // equal-length ticks
      const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, ux = (b[0] - a[0]) / d, uy = (b[1] - a[1]) / d;
      for (let i = 0; i < ln.tick; i++) { const o = (i - (ln.tick - 1) / 2) * 2.2; out.push(L(mx + ux * o - uy * 2.2, my + uy * o + ux * 2.2, mx + ux * o + uy * 2.2, my + uy * o - ux * 2.2, { w: 1.5 })); }
    }
    if (ln.label) {
      const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
      let nx = -(b[1] - a[1]) / d, ny = (b[0] - a[0]) / d;
      if ((mx + nx - cen[0]) ** 2 + (my + ny - cen[1]) ** 2 < (mx - nx - cen[0]) ** 2 + (my - ny - cen[1]) ** 2) { nx = -nx; ny = -ny; }
      out.push(T(mx + nx * 6.5, my + ny * 5, ln.label, { pt: 16, bold: true, wu: 22 }));
      const m = /^\s*(\d+(?:\.\d+)?)\s*([a-zA-Zµ]+)\s*$/.exec(ln.label);
      if (m) (lineLen[m[2]] = lineLen[m[2]] || []).push({ v: +m[1], d: len, n: ln.a + ln.b });
    }
  }
  // labelled lengths must match the drawing when scale is exact
  if (exact) for (const [u, arr] of Object.entries(lineLen)) for (let i = 1; i < arr.length; i++) {
    const r = (arr[i].d / arr[0].d) / (arr[i].v / arr[0].v);
    if (r < 0.92 || r > 1.08) errors.push(`geometry: ${arr[i].n} is labelled ${arr[i].v} ${u} and ${arr[0].n} ${arr[0].v} ${u}, but the drawing has a different ratio; fix the coordinates or set scale 'not_to_scale'`);
  }
  for (const c of circles) {
    const p = P(c.cc);
    out.push(E(p[0], p[1], c.r * k, c.r * k, { line: INK, w: 2.25 }));
    if (typeof c.c === 'string') out.push(E(p[0], p[1], 0.9, 0.9, { fill: INK, line: INK, w: 0.5 }));
    if (c.label) out.push(T(p[0] + c.r * k * 0.5, p[1] - 4, c.label, { pt: 16, bold: true, wu: 22 }));
  }
  for (const an of sp.angles || []) {
    if (!ref(an.at, 'angle') || !ref(an.from, 'angle') || !ref(an.to, 'angle')) continue;
    const v = P(pts[an.at]), f = P(pts[an.from]), t = P(pts[an.to]);
    let a0 = Math.atan2(f[1] - v[1], f[0] - v[0]), a1 = Math.atan2(t[1] - v[1], t[0] - v[0]);
    let d = a1 - a0; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
    const shortest = Math.min(Math.hypot(f[0] - v[0], f[1] - v[1]), Math.hypot(t[0] - v[0], t[1] - v[1]));
    const r = Math.min(8, shortest * 0.35);
    if (an.right) {
      const ux = Math.cos(a0) * r * 0.9, uy = Math.sin(a0) * r * 0.9, wx = Math.cos(a1) * r * 0.9, wy = Math.sin(a1) * r * 0.9;
      out.push(...polyline([[v[0] + ux, v[1] + uy], [v[0] + ux + wx, v[1] + uy + wy], [v[0] + wx, v[1] + wy]], { w: 1.5 }));
      if (exact && Math.abs(Math.abs(d) - Math.PI / 2) > 0.06) errors.push(`geometry: angle at ${an.at} is marked as a right angle but the drawing measures ${(Math.abs(d) * 180 / Math.PI).toFixed(0)} degrees`);
    } else {
      out.push(...arc(v[0], v[1], r, a0, a0 + d, { w: 1.5 }));
      const mid = a0 + d / 2;
      if (an.label) out.push(T(v[0] + Math.cos(mid) * (r + 6.5), v[1] + Math.sin(mid) * (r + 5.5), an.label, { pt: 16, bold: true, wu: 14 }));
      const m = /(\d+(?:\.\d+)?)\s*°/.exec(an.label || '');
      if (exact && m && Math.abs(Math.abs(d) * 180 / Math.PI - +m[1]) > 4) errors.push(`geometry: angle at ${an.at} is labelled ${m[1]}° but the drawing measures ${(Math.abs(d) * 180 / Math.PI).toFixed(0)}°; fix the coordinates or set scale 'not_to_scale'`);
    }
    if (an.right && an.label) out.push(T(v[0] + (Math.cos(a0) + Math.cos(a1)) * (r + 4), v[1] + (Math.sin(a0) + Math.sin(a1)) * (r + 4), an.label, { pt: 16, bold: true, wu: 14 }));
  }
  if (sp.point_labels !== false) for (const n of names) {
    const p = P(pts[n]); let dx = p[0] - cen[0], dy = p[1] - cen[1]; const d = Math.hypot(dx, dy) || 1;
    out.push(E(p[0], p[1], 0.9, 0.9, { fill: INK, line: INK, w: 0.5 }));
    out.push(T(p[0] + dx / d * 5, p[1] + dy / d * 4.5, n, { pt: 18, bold: true, wu: 10 }));
  }
  let H2 = H;
  if (!exact) { out.push(T(W / 2, H + 3, 'Not drawn to scale', { pt: 14, italic: true, color: GREY, wu: 50 })); H2 = H + 7; }
  return { w: W, h: H2, shapes: out, errors, notes: exact ? 'drawn to scale' : 'not to scale' };
}

// ---------------------------------------------------------------- coordinate grid
// spec: {x:[min,max], y:[min,max], step, grid:true, shapes:[{pts:[[x,y]..], labels:[..], color, closed}],
//        lines:[{m,c,label,color}|{x:3,label}|{y:2,label}|{p:[x,y],q:[x,y],label}], points:[{at,label}],
//        vectors:[{from,to,label,color}]}
function buildGrid(sp) {
  const errors = [];
  const [x0, x1] = sp.x || [], [y0, y1] = sp.y || [];
  if (![x0, x1, y0, y1].every(isNum) || x1 <= x0 || y1 <= y0) return { errors: ['grid: x and y must be [min, max] with max > min'] };
  const xr = x1 - x0, yr = y1 - y0;
  if (xr > 40 || yr > 40) errors.push('grid: window larger than 40 units');
  const step = sp.step || 1, u = 80 / Math.max(xr, yr), M = 12;
  const W = xr * u + 2 * M, H = yr * u + 2 * M;
  const X = x => M + (x - x0) * u, Y = y => M + (y1 - y) * u;
  const out = [];
  if (sp.grid !== false) {
    for (let x = Math.ceil(x0 / step) * step; x <= x1 + 1e-9; x += step) out.push(L(X(x), Y(y0), X(x), Y(y1), { color: LIGHT, w: 0.5 }));
    for (let y = Math.ceil(y0 / step) * step; y <= y1 + 1e-9; y += step) out.push(L(X(x0), Y(y), X(x1), Y(y), { color: LIGHT, w: 0.5 }));
  }
  const ax = x0 <= 0 && x1 >= 0 ? 0 : x0, ay = y0 <= 0 && y1 >= 0 ? 0 : y0;
  out.push(L(X(x0), Y(ay), X(x1) + 4, Y(ay), { w: 1.75, arrow: 'end' }), L(X(ax), Y(y0), X(ax), Y(y1) - 4, { w: 1.75, arrow: 'end' }));
  const every = sp.labels_every || step;
  for (let x = Math.ceil(x0 / every) * every; x <= x1 + 1e-9; x += every) if (Math.abs(x - ax) > 1e-9) { out.push(L(X(x), Y(ay) - 0.9, X(x), Y(ay) + 0.9, { w: 1 })); out.push(T(X(x), Y(ay) + 4.2, +x.toFixed(6), { pt: 14, wu: 8, tick: true })); }
  for (let y = Math.ceil(y0 / every) * every; y <= y1 + 1e-9; y += every) if (Math.abs(y - ay) > 1e-9) { out.push(L(X(ax) - 0.9, Y(y), X(ax) + 0.9, Y(y), { w: 1 })); out.push(T(X(ax) - 4.2, Y(y), +y.toFixed(6), { pt: 14, align: 'r', wu: 8, tick: true })); }
  out.push(T(X(x1) + 5, Y(ay) - 3.5, sp.x_label || 'x', { pt: 16, italic: true, wu: 8 }), T(X(ax) + 5, Y(y1) - 3, sp.y_label || 'y', { pt: 16, italic: true, wu: 8 }));
  if (ax === 0 && ay === 0) out.push(T(X(0) - 3, Y(0) + 4.2, '0', { pt: 14, wu: 6 }));
  const inside = (x, y) => x >= x0 - 1e-9 && x <= x1 + 1e-9 && y >= y0 - 1e-9 && y <= y1 + 1e-9;
  (sp.shapes || []).forEach((s, i) => {
    const c = col(s.color, i), ps = s.pts || [];
    if (ps.length < 2 || !ps.every(isPt)) { errors.push('grid: each shape needs pts as [[x, y], ...]'); return; }
    ps.forEach(p => { if (!inside(p[0], p[1])) errors.push(`grid: point (${p[0]}, ${p[1]}) is outside the grid window`); });
    const q = s.closed === false ? ps : ps.concat([ps[0]]);
    out.push(...polyline(q.map(p => [X(p[0]), Y(p[1])]), { color: c, w: 2.5 }));
    const gc = [ps.reduce((a, p) => a + p[0], 0) / ps.length, ps.reduce((a, p) => a + p[1], 0) / ps.length];
    ps.forEach((p, j) => {
      out.push(E(X(p[0]), Y(p[1]), 0.9, 0.9, { fill: c, line: c, w: 0.5 }));
      const lab = (s.labels || [])[j]; if (!lab) return;
      const dx = p[0] - gc[0], dy = p[1] - gc[1], d = Math.hypot(dx, dy) || 1;
      out.push(T(X(p[0]) + dx / d * 5.5, Y(p[1]) - dy / d * 4.5, lab, { pt: 16, bold: true, color: c, wu: 10 }));
    });
  });
  (sp.lines || []).forEach((ln, i) => {
    const c = col(ln.color, i + 1); let a, b;
    if (isNum(ln.m)) { const cc = ln.c || 0; a = [x0, ln.m * x0 + cc]; b = [x1, ln.m * x1 + cc]; }
    else if (isNum(ln.x)) { a = [ln.x, y0]; b = [ln.x, y1]; }
    else if (isNum(ln.y)) { a = [x0, ln.y]; b = [x1, ln.y]; }
    else if (isPt(ln.p) && isPt(ln.q)) { a = ln.p; b = ln.q; if (ln.extend) { const dx = b[0] - a[0], dy = b[1] - a[1]; const t = 100; a = [a[0] - dx * t, a[1] - dy * t]; b = [b[0] + dx * t, b[1] + dy * t]; } }
    else { errors.push('grid: each line needs m (and c), x, y, or p and q'); return; }
    // clip to window (Liang-Barsky)
    let t0 = 0, t1 = 1; const dx = b[0] - a[0], dy = b[1] - a[1];
    for (const [p, q] of [[-dx, a[0] - x0], [dx, x1 - a[0]], [-dy, a[1] - y0], [dy, y1 - a[1]]]) {
      if (p === 0) { if (q < 0) { t0 = 1; t1 = 0; } } else { const r = q / p; if (p < 0) t0 = Math.max(t0, r); else t1 = Math.min(t1, r); }
    }
    if (t0 >= t1) { errors.push('grid: a line lies outside the grid window'); return; }
    const A = [a[0] + dx * t0, a[1] + dy * t0], B = [a[0] + dx * t1, a[1] + dy * t1];
    out.push(L(X(A[0]), Y(A[1]), X(B[0]), Y(B[1]), { color: c, w: 2.5, dash: ln.dash ? 'dash' : undefined }));
    if (ln.label) out.push(T(X(B[0]) - 3, Y(B[1]) - 5, ln.label, { pt: 16, bold: true, color: c, align: 'r', wu: 30 }));
  });
  (sp.points || []).forEach((pt, i) => {
    if (!isPt(pt.at)) { errors.push('grid: each point needs at: [x, y]'); return; }
    if (!inside(pt.at[0], pt.at[1])) errors.push(`grid: point (${pt.at[0]}, ${pt.at[1]}) is outside the grid window`);
    const c = col(pt.color, i);
    out.push(E(X(pt.at[0]), Y(pt.at[1]), 1.2, 1.2, { fill: c, line: c, w: 0.5 }));
    if (pt.label) out.push(T(X(pt.at[0]) + 3, Y(pt.at[1]) - 4.5, pt.label, { pt: 16, bold: true, color: c, align: 'l', wu: 26 }));
  });
  (sp.vectors || []).forEach((v, i) => {
    if (!isPt(v.from) || !isPt(v.to)) { errors.push('grid: each vector needs from and to as [x, y]'); return; }
    const c = col(v.color, i + 2);
    out.push(L(X(v.from[0]), Y(v.from[1]), X(v.to[0]), Y(v.to[1]), { color: c, w: 2.5, arrow: 'end', dash: v.dash ? 'dash' : undefined }));
    if (v.label) out.push(T((X(v.from[0]) + X(v.to[0])) / 2 + 2, (Y(v.from[1]) + Y(v.to[1])) / 2 - 5, v.label, { pt: 16, bold: true, color: c, wu: 24 }));
  });
  return { w: W + 4, h: H, shapes: out, errors, notes: 'grid drawn to scale' };
}

// ---------------------------------------------------------------- circuit
// spec: {source:{type:'cell'|'battery',label}, series:[comp], parallel:[[comp],[comp]], bottom:[comp]}
// comp: {type, label}. series sits on the top wire left to right, then the parallel branches (each a vertical column).
const COMP = {
  cell: 4, battery: 6, bulb: 7, resistor: 10, variable_resistor: 10, switch_open: 9, switch_closed: 9,
  ammeter: 8, voltmeter: 8, fuse: 9, diode: 7, led: 7,
};
// draw component centred at (cx,cy), local axis u along the wire. horiz => u is x; else u is y.
function symbol(type, cx, cy, horiz, flip) {
  const o = [], P = (u, v) => horiz ? [cx + u * (flip ? -1 : 1), cy + v] : [cx + v, cy + u * (flip ? -1 : 1)];
  const ln = (u1, v1, u2, v2, w = 2, color = INK) => { const a = P(u1, v1), b = P(u2, v2); o.push(L(a[0], a[1], b[0], b[1], { w, color })); };
  const rect = (u1, v1, u2, v2) => { ln(u1, v1, u2, v1); ln(u2, v1, u2, v2); ln(u2, v2, u1, v2); ln(u1, v2, u1, v1); };
  switch (type) {
    case 'cell': ln(-1, -4.5, -1, 4.5, 2); ln(1, -2.5, 1, 2.5, 4.5); break;
    case 'battery': ln(-2.5, -4.5, -2.5, 4.5, 2); ln(-0.5, -2.5, -0.5, 2.5, 4.5); ln(1.5, -4.5, 1.5, 4.5, 2); ln(3.5, -2.5, 3.5, 2.5, 4.5); break;
    case 'bulb': { const c = P(0, 0); o.push(E(c[0], c[1], 3.4, 3.4, { w: 2 })); ln(-2.4, -2.4, 2.4, 2.4); ln(-2.4, 2.4, 2.4, -2.4); break; }
    case 'resistor': rect(-4.5, -2, 4.5, 2); break;
    case 'variable_resistor': rect(-4.5, -2, 4.5, 2); { const a = P(-4, 4.5), b = P(4, -4.5); o.push(L(a[0], a[1], b[0], b[1], { w: 1.75, arrow: 'end' })); } break;
    case 'fuse': rect(-4, -1.8, 4, 1.8); ln(-4, 0, 4, 0, 1.25); break;
    case 'switch_open': { const a = P(-4, 0), b = P(4, 0); o.push(E(a[0], a[1], 0.9, 0.9, { fill: INK })); o.push(E(b[0], b[1], 0.9, 0.9, { fill: INK })); ln(-4, 0, 3, -4.5, 2); break; }
    case 'switch_closed': { const a = P(-4, 0), b = P(4, 0); o.push(E(a[0], a[1], 0.9, 0.9, { fill: INK })); o.push(E(b[0], b[1], 0.9, 0.9, { fill: INK })); ln(-4, 0, 4, 0, 2); break; }
    case 'ammeter': case 'voltmeter': { const c = P(0, 0); o.push(E(c[0], c[1], 3.6, 3.6, { w: 2 })); o.push(T(c[0], c[1], type === 'ammeter' ? 'A' : 'V', { pt: 18, bold: true, wu: 6 })); break; }
    case 'diode': case 'led': ln(-3, -3.2, -3, 3.2); ln(-3, -3.2, 3, 0); ln(-3, 3.2, 3, 0); ln(3, -3.2, 3, 3.2);
      if (type === 'led') { const a = P(0, -4), b = P(2.2, -7); o.push(L(a[0], a[1], b[0], b[1], { w: 1.5, arrow: 'end' })); const c = P(2, -3.5), d = P(4.2, -6.5); o.push(L(c[0], c[1], d[0], d[1], { w: 1.5, arrow: 'end' })); } break;
    default: break;
  }
  return o;
}
function wireWithGaps(x1, y1, x2, y2, gaps, horiz) { // gaps: [{c, hl}] positions along the wire axis
  const out = [], a = horiz ? x1 : y1, b = horiz ? x2 : y2, dir = b >= a ? 1 : -1;
  const gs = gaps.slice().sort((p, q) => dir * (p.c - q.c)); let cur = a;
  const seg = (s, e) => { if (dir * (e - s) > 0.01) out.push(horiz ? L(s, y1, e, y1, { w: 2 }) : L(x1, s, x1, e, { w: 2 })); };
  for (const g of gs) { seg(cur, g.c - dir * g.hl); cur = g.c + dir * g.hl; }
  seg(cur, b); return out;
}
function buildCircuit(sp) {
  const errors = [], out = [];
  const series = sp.series || [], branches = sp.parallel || [], bottom = sp.bottom || [];
  const src = sp.source || { type: 'cell' };
  const bad = c => !c || !COMP[c.type] ? (errors.push(`circuit: unknown component type '${c && c.type}' (allowed: ${Object.keys(COMP).join(', ')})`), true) : false;
  [src, ...series, ...bottom, ...branches.flat()].forEach(bad);
  if (!['cell', 'battery'].includes(src.type)) errors.push('circuit: source must be a cell or a battery');
  series.concat(bottom).forEach(c => { if (c.type === 'voltmeter') errors.push('circuit: a voltmeter must be connected in parallel (put it in a parallel branch), not in series'); });
  branches.forEach(br => { if (br.length === 1 && br[0].type === 'ammeter' && branches.length > 1) errors.push('circuit: an ammeter alone in a parallel branch short-circuits the other branches; put it in series'); });
  if (errors.length) return { errors };
  const nB = branches.length, topN = series.length;
  const bw = 22;
  const rightX = nB ? Math.max(70, 28 + topN * 17) + (nB - 1) * bw + 10 : Math.max(70, 28 + topN * 17 + 12);
  const junctionX = nB ? rightX - (nB - 1) * bw - 10 : rightX;
  const left = 14, topY = 16, botY = 16 + (nB && branches.some(b => b.length > 1) ? 46 : 40);
  const W = rightX + 22, H = botY + 20;
  // left edge: source in the middle
  const midY = (topY + botY) / 2;
  const srcHl = COMP[src.type] / 2 + 1;
  out.push(...wireWithGaps(left, topY, left, botY, [{ c: midY, hl: srcHl }], false));
  out.push(...symbol(src.type, left, midY, false, true));
  out.push(T(left - 7, midY, src.label || '', { pt: 16, bold: true, align: 'r', wu: 18 }));
  // top wire with series components
  const gapsTop = series.map((c, i) => ({ c: left + 14 + i * 17, hl: COMP[c.type] / 2 + 1, comp: c }));
  out.push(...wireWithGaps(left, topY, junctionX, topY, gapsTop, true));
  gapsTop.forEach(g => { out.push(...symbol(g.comp.type, g.c, topY, true)); if (g.comp.label) out.push(T(g.c, topY - 8.5, g.comp.label, { pt: 16, bold: true, wu: 22 })); });
  // bottom wire (optionally with components)
  const gapsBot = bottom.map((c, i) => ({ c: left + 14 + i * 17, hl: COMP[c.type] / 2 + 1, comp: c }));
  out.push(...wireWithGaps(left, botY, nB ? rightX : rightX, botY, gapsBot, true));
  gapsBot.forEach(g => { out.push(...symbol(g.comp.type, g.c, botY, true)); if (g.comp.label) out.push(T(g.c, botY + 8.5, g.comp.label, { pt: 16, bold: true, wu: 22 })); });
  if (!nB) { out.push(L(rightX, topY, rightX, botY, { w: 2 })); }
  else {
    branches.forEach((br, i) => {
      const x = junctionX + i * bw + (nB === 1 ? 0 : 0);
      const gs = br.map((c, j) => ({ c: topY + (botY - topY) * (j + 1) / (br.length + 1), hl: COMP[c.type] / 2 + 1, comp: c }));
      out.push(...wireWithGaps(x, topY, x, botY, gs, false));
      gs.forEach(g => { out.push(...symbol(g.comp.type, x, g.c, false)); if (g.comp.label) out.push(T(x + 6, g.c, g.comp.label, { pt: 16, bold: true, align: 'l', wu: 24 })); });
      if (i > 0) { out.push(L(x - bw, topY, x, topY, { w: 2 }), L(x - bw, botY, x, botY, { w: 2 })); }
      if (nB > 1) { out.push(E(x, topY, 0.8, 0.8, { fill: INK, line: INK, w: 0.5 }), E(x, botY, 0.8, 0.8, { fill: INK, line: INK, w: 0.5 })); }
    });
    const last = junctionX + (nB - 1) * bw;
    out.push(L(last, topY, rightX, topY, { w: 2 }), L(last, botY, rightX, botY, { w: 2 }), L(rightX, topY, rightX, botY, { w: 2 }));
    out.push(T(0, 0, '', { pt: 1 }));
  }
  return { w: W, h: H, shapes: out.filter(s => !(s.t === 'text' && s.text === '')), errors, notes: 'circuit symbols' };
}

// ---------------------------------------------------------------- atoms and ions (Bohr diagrams)
const SYM = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'];
const CAP = [2, 8, 8, 18];
// spec: {atoms:[{symbol, protons, neutrons, shells:[2,8,1], charge, show_counts, label, outer_only}]}
function buildAtoms(sp) {
  const errors = [], atoms = sp.atoms || [];
  if (!atoms.length || atoms.length > 4) return { errors: ['atoms: give 1 to 4 atoms or ions'] };
  const radii = at => 15 + 8 * ((at.shells || []).length - 1);
  atoms.forEach((a, i) => {
    const tag = `atom ${i + 1} (${a.symbol || '?'})`;
    if (!Array.isArray(a.shells) || !a.shells.length || a.shells.length > 4 || !a.shells.every(n => Number.isInteger(n) && n >= 0)) { errors.push(`atoms: ${tag} needs shells as electrons per shell, e.g. [2, 8, 1] (max 4 shells)`); return; }
    const z = SYM.indexOf(a.symbol) + 1, charge = a.charge || 0, tot = a.shells.reduce((s, n) => s + n, 0);
    if (z === 0) errors.push(`atoms: ${tag}: symbol not in the first 36 elements`);
    if (z && a.protons !== undefined && a.protons !== null && a.protons !== z) errors.push(`atoms: ${tag}: ${a.symbol} has ${z} protons, not ${a.protons}`);
    if (z && tot !== z - charge) errors.push(`atoms: ${tag}: ${a.shells.join(', ')} is ${tot} electrons but ${a.symbol}${charge ? ` with charge ${charge > 0 ? '+' : ''}${charge}` : ''} needs ${z - charge}`);
    a.shells.forEach((n, s) => { if (n > CAP[s]) errors.push(`atoms: ${tag}: shell ${s + 1} holds at most ${CAP[s]} electrons, not ${n}`); });
    if (z && z <= 20) a.shells.forEach((n, s) => { if (s < a.shells.length - 1 && n < Math.min(CAP[s], 8)) errors.push(`atoms: ${tag}: shell ${s + 1} must be full before shell ${s + 2} (${a.shells.join(', ')})`); });
  });
  if (errors.length) return { errors };
  const out = [], rmax = Math.max(...atoms.map(radii)), D = 2 * (rmax + 6), gap = 8;
  let x = 0;
  atoms.forEach(a => {
    const cx = x + D / 2, cy = rmax + 8, r0 = radii(a), z = SYM.indexOf(a.symbol) + 1;
    const ion = !!a.charge;
    if (a.outer_only) { // outer shell only: dots around the symbol (Lewis style)
      out.push(T(cx, cy, a.symbol, { pt: 28, bold: true, wu: 14 }));
      const n = a.shells[a.shells.length - 1], pos = [[0, -9, 3, 0], [0, 9, -3, 0], [9, 0, 0, -3], [-9, 0, 0, 3]];
      for (let i = 0; i < n; i++) { const p = pos[i % 4], s = i < 4 ? 1 : -1; out.push(E(cx + p[0] + (p[2] ? s * p[2] : 0), cy + p[1] + (p[3] ? s * p[3] : 0), 0.95, 0.95, { fill: INK, line: INK, w: 0.5 })); }
    } else {
      a.shells.forEach((n, s) => {
        const r = 15 + 8 * s; out.push(E(cx, cy, r, r, { line: '7F7F7F', w: 1.5 }));
        for (let i = 0; i < n; i++) { const ang = -Math.PI / 2 + (2 * Math.PI * i) / n + s * 0.5; out.push(E(cx + r * Math.cos(ang), cy + r * Math.sin(ang), 1.5, 1.5, { fill: '1F77B4', line: '1F77B4', w: 0.5 })); }
      });
      out.push(E(cx, cy, 8.5, 8.5, { fill: 'FDE9C9', line: 'C77700', w: 2 }));
      const counts = a.show_counts !== false;
      out.push(T(cx, cy, counts ? `${z}p\n${a.neutrons !== undefined && a.neutrons !== null ? a.neutrons + 'n' : ''}`.trim() : a.symbol, { pt: counts ? 13 : 16, bold: true, wu: 16 }));
    }
    let ly = cy + rmax + 7;
    const nm = (ion && a.charge ? `${a.symbol}${Math.abs(a.charge) > 1 ? Math.abs(a.charge) : ''}${a.charge > 0 ? '+' : '−'}` : a.symbol) + (a.label ? ` ${a.label}` : '');
    out.push(T(cx, ly + 3, nm, { pt: 18, bold: true, wu: D + 4 }));
    if (ion && !a.outer_only) { // square brackets with the charge at the top right
      const bx = r0 + 6, by = r0 + 6;
      for (const sd of [1, -1]) out.push(L(cx + sd * bx, cy - by, cx + sd * bx, cy + by, { w: 2 }), L(cx + sd * bx, cy - by, cx + sd * (bx - 3), cy - by, { w: 2 }), L(cx + sd * bx, cy + by, cx + sd * (bx - 3), cy + by, { w: 2 }));
      out.push(T(cx + bx + 2, cy - by - 2, `${Math.abs(a.charge) > 1 ? Math.abs(a.charge) : ''}${a.charge > 0 ? '+' : '−'}`, { pt: 18, bold: true, align: 'l', wu: 8 }));
    }
    x += D + gap;
  });
  return { w: x - gap, h: 2 * (rmax + 8) + 14, shapes: out, errors, notes: 'electron arrangement checked against proton number' };
}

// ---------------------------------------------------------------- flow / cycle
// spec: {kind:'flow'|'cycle', nodes:[{text}], arrow_labels:[...], per_row:4}
function buildFlow(sp) {
  const errors = [], nodes = sp.nodes || [], n = nodes.length;
  if (n < 2 || n > 10) return { errors: ['flow: give 2 to 10 nodes'] };
  nodes.forEach(nd => { if (!nd.text || nd.text.length > 60) errors.push(`flow: node text is empty or longer than 60 characters ('${String(nd.text).slice(0, 30)}...')`); });
  if (errors.length) return { errors };
  const out = [], al = sp.arrow_labels || [], nodeShapes = [];
  const box = (cx, cy, w, h, nd, i) => { const c = PALETTE[i % PALETTE.length]; out.push(R(cx - w / 2, cy - h / 2, w, h, { fill: tintOf(c), line: c, w: 2, r: 3 })); out.push(T(cx, cy, nd.text, { pt: 16, bold: true, wu: w - 2, box: [w - 2, h - 1] })); nodeShapes.push({ cx, cy, w, h }); };
  const clip = (a, b) => { // point on edge of box a towards b
    const dx = b.cx - a.cx, dy = b.cy - a.cy; const t = Math.min(dx ? (a.w / 2 + 1) / Math.abs(dx) : 1e9, dy ? (a.h / 2 + 1) / Math.abs(dy) : 1e9); return [a.cx + dx * t, a.cy + dy * t];
  };
  const link = (i, j) => {
    const a = nodeShapes[i], b = nodeShapes[j], p = clip(a, b), q = clip(b, a);
    out.push(L(p[0], p[1], q[0], q[1], { w: 2.5, arrow: 'end' }));
    if (al[i]) { const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2; out.push(T(mx, my - 4.2, al[i], { pt: 14, italic: true, wu: 22 })); }
  };
  let W, H;
  if (sp.kind === 'cycle') {
    const rx = 38, ry = 26, bw = 26, bh = 11; W = 2 * rx + bw + 6; H = 2 * ry + bh + 6;
    nodes.forEach((nd, i) => { const a = -Math.PI / 2 + 2 * Math.PI * i / n; box(W / 2 + rx * Math.cos(a), H / 2 + ry * Math.sin(a), bw, bh, nd, i); });
    for (let i = 0; i < n; i++) link(i, (i + 1) % n);
  } else {
    const per = Math.max(2, Math.min(sp.per_row || 4, 5)), rows = Math.ceil(n / per), bw = 24, bh = 12, gx = 12, gy = 14;
    W = Math.min(per, n) * bw + (Math.min(per, n) - 1) * gx + 4; H = rows * bh + (rows - 1) * gy + 4;
    nodes.forEach((nd, i) => { const r = Math.floor(i / per), c = i % per, cc = r % 2 ? per - 1 - c : c; box(2 + bw / 2 + cc * (bw + gx), 2 + bh / 2 + r * (bh + gy), bw, bh, nd, i); });
    for (let i = 0; i < n - 1; i++) link(i, i + 1);
  }
  return { w: W, h: H, shapes: out, errors, notes: sp.kind === 'cycle' ? 'cycle' : 'flow' };
}
function tintOf(hex) { const c = [0, 2, 4].map(i => parseInt(hex.slice(i, i + 2), 16)); return c.map(v => Math.round(v + (255 - v) * 0.85).toString(16).padStart(2, '0')).join('').toUpperCase(); }


// ---------------------------------------------------------------- apparatus
// spec: {parts:[{id,type,x,size,liquid,colour,stopper,on,in,inverted,reading,holds,flame}], links:[{from,to}], labels:[{on,text,side,at}]}
// Fixed, correctly drawn bench parts placed by position. The generator owns the drawing and checks the setup.
const LQ = { blue: 'BFDFF5', red: 'F4B6B6', green: 'BFE5BF', orange: 'F9D3A8', purple: 'D8C7EA', clear: 'EAF4FB' };
const APP_TYPES = ['beaker', 'conical_flask', 'test_tube', 'measuring_cylinder', 'bunsen', 'tripod', 'gas_jar', 'trough', 'balance', 'thermometer', 'funnel', 'dish', 'stand'];
const CONTAINERS = ['beaker', 'conical_flask', 'test_tube', 'measuring_cylinder', 'gas_jar', 'trough', 'dish'];
const SIZE = { small: 0.8, m: 1, l: 1.25 };
const BENCH = 62;

function liquidRects(cx, by, h, hw, level, color, out) {
  const top = h * 0.92 * level;
  for (let d = 0; d < top; d += 0.8) { const w = hw(d + 0.4), hh = Math.min(0.95, top - d + 0.15); out.push(R(cx - w, by - d - hh, 2 * w, hh, { fill: color, line: null })); }
  return by - top;
}

function drawPart(pt, cx, by, u, out) { // returns geometry: {bb, top, surface, support, hw0}
  const g = { bb: null, top: [cx, by], surface: null, support: null }, lc = LQ[pt.colour] || LQ.blue, lvl = pt.liquid || 0;
  const wall = (x1, y1, x2, y2) => out.push(L(x1, y1, x2, y2, { w: 2 }));
  switch (pt.type) {
    case 'beaker': { const w = 7 * u, h = 18 * u; if (lvl) g.surface = liquidRects(cx, by, h, () => w, lvl, lc, out);
      wall(cx - w, by - h, cx - w, by); wall(cx + w, by - h, cx + w, by); wall(cx - w, by, cx + w, by); if (g.surface) out.push(L(cx - w, g.surface, cx + w, g.surface, { w: 1, color: GREY }));
      g.bb = { x0: cx - w, x1: cx + w, y0: by - h, y1: by }; g.top = [cx, by - h]; g.mouth = by - h; g.hw0 = w; break; }
    case 'conical_flask': { const h = 20 * u, nh = 2.6 * u, bw = 8 * u, k = h * 0.55, hw = d => d <= k ? bw - (bw - nh) * d / k : nh;
      if (lvl) g.surface = liquidRects(cx, by, h, hw, lvl, lc, out);
      wall(cx - bw, by, cx + bw, by); wall(cx - bw, by, cx - nh, by - k); wall(cx + bw, by, cx + nh, by - k); wall(cx - nh, by - k, cx - nh, by - h); wall(cx + nh, by - k, cx + nh, by - h);
      let top = by - h; if (pt.stopper) { out.push(R(cx - nh - 0.7, by - h - 3, 2 * nh + 1.4, 3, { fill: '8A8A8A', line: INK, w: 1.5 })); top = by - h - 3; }
      g.bb = { x0: cx - bw, x1: cx + bw, y0: top, y1: by }; g.top = [cx, top]; g.mouth = by - h; g.hw0 = nh; g.sealed = !!pt.stopper; break; }
    case 'test_tube': { const hw = 2.6 * u, h = 20 * u; if (lvl) { g.surface = liquidRects(cx, by - hw, h - hw, () => hw, lvl, lc, out); out.push(E(cx, by - hw, hw, hw, { fill: lc, line: null })); }
      wall(cx - hw, by - h, cx - hw, by - hw); wall(cx + hw, by - h, cx + hw, by - hw); out.push(...arc(cx, by - hw, hw, 0, Math.PI, { w: 2 }));
      let top = by - h; if (pt.stopper) { out.push(R(cx - hw - 0.5, top - 3, 2 * hw + 1, 3, { fill: '8A8A8A', line: INK, w: 1.5 })); top -= 3; }
      g.bb = { x0: cx - hw - 0.5, x1: cx + hw + 0.5, y0: top, y1: by }; g.top = [cx, top]; g.mouth = by - h; g.hw0 = hw; g.sealed = !!pt.stopper; break; }
    case 'measuring_cylinder': { const hw = 2.8 * u, h = 26 * u; if (lvl) g.surface = liquidRects(cx, by, h, () => hw, lvl, lc, out);
      wall(cx - hw, by - h, cx - hw, by); wall(cx + hw, by - h, cx + hw, by); out.push(R(cx - hw - 1.5, by - 1.2, 2 * hw + 3, 1.2, { fill: 'D9D9D9', line: INK, w: 1.5 }));
      for (let i = 1; i <= 9; i++) out.push(L(cx - hw, by - h * i / 10, cx - hw + (i % 5 ? 1.4 : 2.4), by - h * i / 10, { w: 1 }));
      g.bb = { x0: cx - hw - 1.5, x1: cx + hw + 1.5, y0: by - h, y1: by }; g.top = [cx, by - h]; g.mouth = by - h; g.hw0 = hw; break; }
    case 'bunsen': { const w = 2.2 * u, h = 8.5 * u; out.push(R(cx - 4.5 * u, by - 1.6, 9 * u, 1.6, { fill: '595959', line: INK, w: 1.5 })); out.push(R(cx - w, by - h, 2 * w, h - 1.6, { fill: 'A6A6A6', line: INK, w: 1.5 }));
      if (pt.flame !== false) { out.push(E(cx, by - h - 3.2 * u, 1.5 * u, 3.4 * u, { fill: 'FFB000', line: null })); out.push(E(cx, by - h - 2.2 * u, 0.8 * u, 2.2 * u, { fill: '2F80ED', line: null })); }
      g.bb = { x0: cx - 4.5 * u, x1: cx + 4.5 * u, y0: by - h - (pt.flame !== false ? 6.6 * u : 0), y1: by }; g.top = [cx, g.bb.y0]; g.heat = true; break; }
    case 'tripod': { const h = 19 * u, w = 8 * u; out.push(L(cx - w, by - h, cx - w - 2, by, { w: 2.5 })); out.push(L(cx + w, by - h, cx + w + 2, by, { w: 2.5 })); out.push(R(cx - w - 1, by - h - 1.2, 2 * w + 2, 1.2, { fill: 'D9D9D9', line: INK, w: 1.5 }));
      g.bb = { x0: cx - w - 2, x1: cx + w + 2, y0: by - h - 1.2, y1: by }; g.support = by - h - 1.2; g.top = [cx, g.support]; break; }
    case 'gas_jar': { const hw = 4 * u, h = 22 * u; if (lvl) { if (pt.inverted) { const top = by - h; for (let d = 0; d < h * lvl; d += 0.8) out.push(R(cx - hw, by - d - 0.95 - (h - h * lvl) * 0 , 2 * hw, 0.95, { fill: lc, line: null })); g.surface = by - h * lvl; } else g.surface = liquidRects(cx, by, h, () => hw, lvl, lc, out); }
      wall(cx - hw, by - h, cx - hw, by); wall(cx + hw, by - h, cx + hw, by); if (pt.inverted) wall(cx - hw, by - h, cx + hw, by - h); else wall(cx - hw, by, cx + hw, by);
      g.bb = { x0: cx - hw, x1: cx + hw, y0: by - h, y1: by }; g.top = [cx, by - h]; g.mouth = pt.inverted ? by : by - h; g.hw0 = hw; g.inverted = !!pt.inverted; break; }
    case 'trough': { const hw = 15 * u, h = 8 * u; g.surface = liquidRects(cx, by, h, () => hw, lvl || 0.7, lc, out); wall(cx - hw, by - h, cx - hw, by); wall(cx + hw, by - h, cx + hw, by); wall(cx - hw, by, cx + hw, by);
      const sy = by - h * 0.55; out.push(R(cx - hw * 0.35, sy, hw * 0.7, 1.1, { fill: 'D9D9D9', line: INK, w: 1.5 })); g.bb = { x0: cx - hw, x1: cx + hw, y0: by - h, y1: by }; g.top = [cx, by - h]; g.shelf = sy; g.support = sy; g.rim = by - h; g.hw0 = hw; break; }
    case 'balance': { const w = 10 * u; out.push(R(cx - w, by - 5, 2 * w, 5, { fill: 'D9D9D9', line: INK, w: 2, r: 1 })); out.push(R(cx - 4 * u, by - 4.2, 8 * u, 3, { fill: '203040', line: INK, w: 1 }));
      if (pt.reading) out.push(T(cx, by - 2.7, pt.reading, { pt: 12, bold: true, color: 'A8FFB0', wu: 8 * u })); out.push(R(cx - 6 * u, by - 6.2, 12 * u, 1.2, { fill: 'A6A6A6', line: INK, w: 1.5 }));
      g.bb = { x0: cx - w, x1: cx + w, y0: by - 6.2, y1: by }; g.support = by - 6.2; g.top = [cx, g.support]; break; }
    case 'dish': { const hw = 6 * u, h = 3.5 * u; out.push(...arc(cx, by - h, hw, 0, Math.PI, { w: 2 })); out.push(L(cx - hw, by - h, cx + hw, by - h, { w: 2 })); if (lvl) out.push(R(cx - hw * 0.7, by - h - 0.9, hw * 1.4, 0.9, { fill: lc, line: null }));
      g.bb = { x0: cx - hw, x1: cx + hw, y0: by - h, y1: by }; g.top = [cx, by - h]; g.mouth = by - h; g.hw0 = hw; break; }
    case 'funnel': { const hw = 6 * u, h = 8 * u; out.push(L(cx - hw, by - h - 5, cx - 0.9, by - 5, { w: 2 })); out.push(L(cx + hw, by - h - 5, cx + 0.9, by - 5, { w: 2 })); out.push(L(cx - 0.9, by - 5, cx - 0.9, by, { w: 2 })); out.push(L(cx + 0.9, by - 5, cx + 0.9, by, { w: 2 }));
      out.push(L(cx - hw, by - h - 5, cx + hw, by - h - 5, { w: 2 })); if (pt.paper) out.push(L(cx - hw * 0.8, by - h - 4.2, cx, by - 5.5, { w: 1, color: GREY, dash: 'dash' }), L(cx + hw * 0.8, by - h - 4.2, cx, by - 5.5, { w: 1, color: GREY, dash: 'dash' }));
      g.bb = { x0: cx - hw, x1: cx + hw, y0: by - h - 5, y1: by }; g.top = [cx, by - h - 5]; break; }
    case 'stand': { const h = 40 * u; out.push(L(cx, by, cx, by - h, { w: 3 })); out.push(R(cx - 6 * u, by - 1.6, 12 * u, 1.6, { fill: '595959', line: INK, w: 1.5 })); g.bb = { x0: cx - 6 * u, x1: cx + 6 * u, y0: by - h, y1: by }; g.top = [cx, by - h]; break; }
  }
  return g;
}

function buildApparatus(sp) {
  const errors = [], parts = sp.parts || [], out = [], geo = {}, byId = {}, W = 100, H = 70;
  if (!parts.length || parts.length > 10) return { errors: ['apparatus: give 1 to 10 parts'] };
  parts.forEach(p => { if (!p.id || byId[p.id]) errors.push(`apparatus: part id '${p.id}' is missing or repeated`); byId[p.id] = p;
    if (!APP_TYPES.includes(p.type)) errors.push(`apparatus: unknown part type '${p.type}' (use ${APP_TYPES.join(', ')})`);
    if (p.liquid !== undefined && (!isNum(p.liquid) || p.liquid < 0 || p.liquid > 1)) errors.push(`apparatus: ${p.id} liquid must be between 0 and 1`);
    if (p.liquid && !CONTAINERS.includes(p.type)) errors.push(`apparatus: ${p.id} (${p.type}) cannot hold a liquid`);
    if (p.stopper && !['conical_flask', 'test_tube'].includes(p.type)) errors.push(`apparatus: ${p.id} (${p.type}) cannot take a stopper`); });
  if (errors.length) return { errors };
  out.push(L(6, BENCH, 94, BENCH, { w: 3, color: '595959' }));
  // draw in two passes: parts that sit on the bench first, then parts that rest on another part
  const order = [...parts.filter(p => !p.on && !p.in), ...parts.filter(p => p.on), ...parts.filter(p => p.in)];
  for (const p of order) {
    const u = SIZE[p.size] || 1; let cx = p.x, by = BENCH;
    if (p.on) { const h = geo[p.on]; if (!h) { errors.push(`apparatus: ${p.id} is on '${p.on}', which is not drawn before it (check the id)`); continue; }
      if (h.support === null || h.support === undefined) { errors.push(`apparatus: ${p.id} cannot rest on ${p.on} (${byId[p.on].type}); use a tripod, trough or balance`); continue; } by = h.support; cx = byId[p.on].x + (p.dx || 0); if (p.x !== undefined && Math.abs(p.x - byId[p.on].x) > 0.01) errors.push(`apparatus: ${p.id} is on ${p.on}, so its x must equal ${byId[p.on].x} (or omit x)`); }
    if (p.type === 'thermometer') {
      const h = geo[p.in]; if (!h || !(byId[p.in] && CONTAINERS.includes(byId[p.in].type))) { errors.push(`apparatus: thermometer ${p.id} must be 'in' a container part`); continue; }
      const cont = byId[p.in]; if (!cont.liquid) errors.push(`apparatus: thermometer ${p.id} is in ${p.in}, which has no liquid`);
      const x = h.bb.x0 + (h.bb.x1 - h.bb.x0) * 0.62, y0 = h.bb.y0 - 9, y1 = h.bb.y1 - 2.5;
      out.push(R(x - 0.7, y0, 1.4, y1 - y0, { fill: 'FFFFFF', line: INK, w: 1.2 })); out.push(E(x, y1 + 0.6, 1.5, 1.5, { fill: 'D62728', line: INK, w: 1 })); out.push(R(x - 0.35, y1 - (y1 - y0) * 0.35, 0.7, (y1 - y0) * 0.35, { fill: 'D62728', line: null }));
      geo[p.id] = { bb: { x0: x - 1.5, x1: x + 1.5, y0, y1 }, top: [x, y0], attached: true }; continue; }
    if (p.type === 'funnel') { if (!p.on && !p.in) { errors.push(`apparatus: funnel ${p.id} must be placed 'in' a beaker or flask`); continue; } }
    const h = p.in && p.type === 'funnel' ? (() => { const c = geo[p.in]; if (!c) return null; return c; })() : null;
    if (p.type === 'funnel' && p.in) { const c = geo[p.in]; if (!c) { errors.push(`apparatus: funnel ${p.id} is in '${p.in}', which is not drawn`); continue; }
      const g = drawPart(p, byId[p.in].x, c.mouth + 5, u, out); g.attached = true; geo[p.id] = g; continue; }
    if (p.type === 'gas_jar' && p.inverted && p.on) { geo[p.id] = drawPart(p, cx, by, u, out); continue; }
    geo[p.id] = drawPart(p, cx, by, u, out);
  }
  if (errors.length) return { errors };
  // stands hold a part with a clamp arm
  parts.filter(p => p.type === 'stand' && p.holds).forEach(p => { const h = geo[p.holds]; if (!h) { errors.push(`apparatus: stand ${p.id} holds '${p.holds}', which is not drawn`); return; }
    const y = h.bb.y0 + (h.bb.y1 - h.bb.y0) * 0.3, gx = geo[p.id].bb; const sx = byId[p.id].x; const tx = sx < (h.bb.x0 + h.bb.x1) / 2 ? h.bb.x0 : h.bb.x1;
    out.push(L(sx, y, tx, y, { w: 3, color: '595959' })); });
  // layout checks
  const free = parts.filter(p => !p.on && !p.in && p.type !== 'stand');
  parts.forEach(p => { const g = geo[p.id]; if (!g || !g.bb) return; if (g.bb.x0 < 16 || g.bb.x1 > 84) errors.push(`apparatus: ${p.id} is outside the drawing area (keep x between about 22 and 78 so labels fit at the sides)`); if (g.bb.y0 < 2) errors.push(`apparatus: ${p.id} is too tall for the frame; use size small or remove a part`); });
  for (let i = 0; i < free.length; i++) for (let j = i + 1; j < free.length; j++) { const a = geo[free[i].id].bb, b = geo[free[j].id].bb;
    const bunsenUnder = (free[i].type === 'bunsen' && free[j].type === 'tripod') || (free[j].type === 'bunsen' && free[i].type === 'tripod');
    if (!bunsenUnder && a.x0 < b.x1 + 1 && b.x0 < a.x1 + 1) errors.push(`apparatus: ${free[i].id} and ${free[j].id} overlap (move one along the bench; x differs by at least the width of the parts)`); }
  // science checks
  parts.forEach(p => {
    if (p.type === 'bunsen') { const above = parts.find(q => q.on && byId[q.on] && byId[q.on].type === 'tripod' && Math.abs(byId[q.on].x - p.x) < 8);
      if (!above) { if (p.flame !== false) errors.push(`apparatus: bunsen ${p.id} heats nothing; put a tripod above it at the same x and the vessel on the tripod`); }
      else if (above.stopper && !(sp.links || []).some(l => l.from === above.id)) errors.push(`apparatus: ${above.id} is sealed with a stopper over a flame and has no delivery tube; a closed vessel must not be heated (remove the stopper or add a link)`);
      if (above && ['test_tube', 'measuring_cylinder', 'gas_jar'].includes(above.type)) errors.push(`apparatus: ${above.id} (${above.type}) is not heated on a tripod; use a beaker, flask or dish`); }
    if (p.type === 'measuring_cylinder' && p.on && byId[p.on].type === 'tripod') errors.push(`apparatus: a measuring cylinder is never heated`);
  });
  (sp.links || []).forEach(l => { const a = byId[l.from], b = byId[l.to];
    if (!a || !b) { errors.push(`apparatus: link ${l.from} -> ${l.to} names a part that does not exist`); return; }
    if (!a.stopper) errors.push(`apparatus: link from ${l.from}: a delivery tube needs a stopper on ${l.from} (set stopper true)`);
    if (!CONTAINERS.includes(b.type)) errors.push(`apparatus: a delivery tube must end in a container, not ${b.type}`);
    const ga = geo[l.from], gb = geo[l.to]; if (!ga || !gb) return;
    const x1 = ga.top[0], y1 = ga.top[1] + 1.5, x2 = gb.top[0], topY = Math.min(ga.bb.y0, gb.bb.y0) - 6;
    if (b.type === 'trough') { // over the rim, under the water, then up into the jar standing on the shelf (or just under the water)
      const jar = parts.find(q => q.on === l.to && q.type === 'gas_jar'), gj = jar && geo[jar.id], xr = gb.bb.x0 + 2.5, yw = gb.bb.y1 - 2.2;
      const pts = [[x1, y1], [x1, topY], [xr, topY], [xr, yw], [gj ? gj.top[0] : x2, yw]]; if (gj) pts.push([gj.top[0], gb.shelf - 6]);
      out.push(...polyline(pts, { w: 2.5, color: '595959' })); return; }
    let endY = gb.inverted ? gb.bb.y1 - 2 : (gb.surface || gb.bb.y1 - 4) + (b.liquid ? 3 : -1);
    const pts = [[x1, y1], [x1, topY], [x2, topY], [x2, endY]]; out.push(...polyline(pts, { w: 2.5, color: '595959' })); });
  // labels: leader lines to the left or right column, spaced so they never overlap
  const labs = (sp.labels || []).map(l => { const g = geo[l.on], p = byId[l.on]; if (!g || !g.bb) { errors.push(`apparatus: label '${l.text}' is on '${l.on}', which does not exist`); return null; }
    if (!l.text || l.text.length > 28) errors.push(`apparatus: label '${l.text}' must be 1 to 28 characters`);
    let ay = g.bb.y0 + (g.bb.y1 - g.bb.y0) * 0.45; if (l.at === 'liquid') { if (!g.surface) errors.push(`apparatus: label '${l.text}' points at the liquid of ${l.on}, which has none`); else ay = g.surface; } else if (l.at === 'top') ay = g.bb.y0 + 1; else if (l.at === 'base') ay = g.bb.y1 - 2;
    const side = l.side === 'left' ? 'left' : l.side === 'right' ? 'right' : ((g.bb.x0 + g.bb.x1) / 2 < 50 ? 'left' : 'right');
    return { text: l.text, side, ay, ax: side === 'left' ? g.bb.x0 : g.bb.x1, ly: ay }; }).filter(Boolean);
  for (const side of ['left', 'right']) { const col = labs.filter(l => l.side === side).sort((a, b) => a.ay - b.ay); let last = -99;
    col.forEach(l => { l.ly = Math.max(l.ay, last + 6.5); last = l.ly; }); const over = last - 66; if (over > 0) col.forEach(l => { l.ly -= over; });
    col.forEach(l => { const lx = side === 'left' ? 17 : 83; out.push(L(l.ax, l.ay, lx, l.ly, { w: 1, color: GREY })); out.push(T(side === 'left' ? 15.5 : 84.5, l.ly, l.text, { pt: 16, bold: true, align: side === 'left' ? 'r' : 'l', wu: 24 })); }); }
  return { w: W, h: 66, shapes: out, errors, notes: 'apparatus' };
}

// ---------------------------------------------------------------- public API
const FAMILIES = { geometry: buildGeometry, grid: buildGrid, circuit: buildCircuit, atoms: buildAtoms, flow: buildFlow, apparatus: buildApparatus };

const FAMILY_DOCS = {
  geometry: 'Lines, polygons, circles and marked angles from coordinates. spec: {"points":{"A":[0,0],"B":[6,0],"C":[2,4]},"lines":[{"a":"A","b":"B","label":"6 cm","tick":0,"dash":false}],"circles":[{"c":"O","r":3,"label":""}],"angles":[{"at":"B","from":"A","to":"C","label":"40°","right":false}],"point_labels":true,"scale":"exact"}. Coordinates are maths coordinates (y up). scale "exact" => labelled lengths and angles are checked against the coordinates (build fails if they disagree); "not_to_scale" => a caption says so. Use exact only when you give coordinates that really satisfy the labels. Do NOT label an answer students must find.',
  grid: 'Cartesian grid with plotted shapes, lines, points and vectors (transformations, graphs of lines, coordinates). spec: {"x":[-6,6],"y":[-6,6],"step":1,"shapes":[{"pts":[[1,1],[3,1],[3,2]],"labels":["A","B","C"],"color":"blue"}],"lines":[{"m":2,"c":1,"label":"y = 2x + 1"},{"x":3},{"y":2},{"p":[0,0],"q":[2,3]}],"points":[{"at":[2,3],"label":"P"}],"vectors":[{"from":[0,0],"to":[3,2],"label":"a"}]}. Colours: blue, red, green, orange, purple. Everything must lie inside the window. Never draw the image shape students must find.',
  circuit: 'Circuit diagram in standard symbols. spec: {"source":{"type":"cell|battery","label":"6 V"},"series":[{"type":"switch_closed","label":"S"},{"type":"ammeter","label":""}],"parallel":[[{"type":"bulb","label":"L1"}],[{"type":"resistor","label":"R"}]],"bottom":[]}. Types: cell, battery, bulb, resistor, variable_resistor, switch_open, switch_closed, ammeter, voltmeter, fuse, diode, led. Series parts go along the top wire; each parallel entry is one branch (a vertical column of parts). Ammeters go in series, voltmeters in a parallel branch (checked).',
  atoms: 'Bohr diagrams of atoms and ions (shells with electrons). spec: {"atoms":[{"symbol":"Na","protons":11,"neutrons":12,"shells":[2,8,1],"charge":0,"show_counts":true,"label":"atom","outer_only":false}]}. 1-4 atoms side by side (e.g. Na and Na+). Electron counts are checked against the element and charge (first 36 elements). outer_only draws dots for the outer shell only. Omit neutrons if the lesson does not give them. Do not draw an atom students are asked to draw.',
  apparatus: 'Laboratory bench setups from fixed, correctly drawn parts. spec: {"parts":[{"id":"b1","type":"beaker","x":50,"size":"m","liquid":0.6,"colour":"blue"}],"links":[{"from":"f1","to":"t1"}],"labels":[{"on":"b1","text":"water","side":"right","at":"liquid"}]}. Part types: beaker, conical_flask, test_tube, measuring_cylinder, bunsen, tripod, gas_jar, trough, balance, thermometer, funnel, dish, stand. x is the position along the bench, 22 to 78 (parts at different x must not overlap: beakers and flasks are about 15 wide, a trough 30). liquid 0 to 1 (fraction full); colour blue, red, green, orange, purple or clear. A part resting on another gives on:"id" (a vessel on a tripod; a tripod, trough and balance can carry things); a bunsen sits at the same x under its tripod. A thermometer or funnel gives in:"id" (a container). stopper:true seals a flask or test tube; a delivery tube is a link from a stoppered vessel to a container. inverted:true on a gas_jar on a trough. stand with holds:"id" clamps a part. Labels: side left or right, at liquid, top or base. The build checks: overlaps, a closed vessel over a flame, a flame heating nothing, a thermometer in no liquid, a tube with no stopper. Do not label what students must identify or predict.',
  flow: 'Boxes joined by arrows: a process flow or a cycle. spec: {"kind":"flow|cycle","nodes":[{"text":"Light is absorbed"},{"text":"..."}],"arrow_labels":["","..."],"per_row":4}. 2-10 nodes, each text up to 60 characters. flow runs left to right and wraps in a snake; cycle places nodes in a ring, last arrow returning to the first. arrow_labels[i] labels the arrow leaving node i. Use for sequences, cycles, food chains, processes.',
};

function buildFigure(json) {
  let sp;
  try { sp = typeof json === 'string' ? JSON.parse(json) : json; } catch (e) { return { errors: ['figure: not valid JSON (' + e.message + ')'] }; }
  if (!sp || !FAMILIES[sp.family]) return { errors: [`figure: family must be one of ${Object.keys(FAMILIES).join(', ')}`] };
  try { const r = FAMILIES[sp.family](sp.spec || {}); r.family = sp.family; return r; } catch (e) { return { errors: [`figure ${sp.family}: could not be built (${e.message})`] }; }
}

// Draw a built figure into box {x,y,w,h} inches. Returns {errors, warnings}.
function drawFigure(pptx, slide, boxIn, fig, opts = {}) {
  const rep = { errors: [], warnings: [] };
  const s = Math.min(boxIn.w / fig.w, boxIn.h / fig.h);
  const ox = boxIn.x + (boxIn.w - fig.w * s) / 2, oy = boxIn.y + (boxIn.h - fig.h * s) / 2;
  const X = v => ox + v * s, Y = v => oy + v * s;
  const font = opts.font || 'Calibri', texts = [];
  for (const sh of fig.shapes) {
    if (sh.t === 'line') {
      const x1 = X(sh.x1), y1 = Y(sh.y1), x2 = X(sh.x2), y2 = Y(sh.y2);
      const line = { color: sh.color, width: sh.w, dashType: sh.dash };
      if (sh.arrow) line.endArrowType = 'triangle';
      slide.addShape(pptx.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipV: (x2 - x1) * (y2 - y1) < 0, flipH: false, line, ...(x2 < x1 && y2 === y1 ? { flipH: true } : {}), ...(y2 < y1 && x2 === x1 ? { flipV: true } : {}) });
    } else if (sh.t === 'ell') {
      slide.addShape(pptx.ShapeType.ellipse, { x: X(sh.cx - sh.rx), y: Y(sh.cy - sh.ry), w: sh.rx * 2 * s, h: sh.ry * 2 * s, line: sh.line ? { color: sh.line, width: sh.w } : { type: 'none' }, fill: sh.fill ? { color: sh.fill } : { type: 'none' } });
    } else if (sh.t === 'rect') {
      const o = { x: X(sh.x), y: Y(sh.y), w: sh.w * s, h: sh.h * s, line: sh.line ? { color: sh.line, width: sh.w_ } : { type: 'none' }, fill: sh.fill ? { color: sh.fill } : { type: 'none' } };
      if (sh.r) { o.rectRadius = Math.min(sh.w, sh.h) * s * 0.18; slide.addShape(pptx.ShapeType.roundRect, o); } else slide.addShape(pptx.ShapeType.rect, o);
    } else if (sh.t === 'text') {
      let pt = sh.pt, wIn = (sh.wu || 20) * s;
      const lines = sh.text.split('\n').length;
      if (sh.box) { // text inside a node box: shrink to fit, never below 12 pt
        const bw = sh.box[0] * s, bh = sh.box[1] * s;
        while (pt > 12 && heightIn(sh.text, pt, bw - 0.1, true) > bh - 0.06) pt -= 1;
        if (heightIn(sh.text, pt, bw - 0.1, true) > bh - 0.06) rep.errors.push(`figure: box text '${sh.text.slice(0, 30)}' does not fit at 12 pt; shorten it`);
        wIn = bw;
      } else wIn = Math.max(wIn, widthIn(sh.text.replace(/\n.*/s, ''), pt, sh.bold) + 0.12);
      const hIn = sh.box ? sh.box[1] * s : Math.max(0.34, lines * pt * 1.2 / 72 + 0.04);
      const x = sh.align === 'l' ? X(sh.x) : sh.align === 'r' ? X(sh.x) - wIn : X(sh.x) - wIn / 2;
      const y = Y(sh.y) - hIn / 2;
      if (!sh.tick) texts.push({ x, y, w: wIn, h: hIn, t: sh.text });
      slide.addText(sh.text, { x, y, w: wIn, h: hIn, fontFace: font, fontSize: pt, bold: sh.bold, italic: sh.italic, color: sh.color, align: sh.align === 'l' ? 'left' : sh.align === 'r' ? 'right' : 'center', valign: 'middle', margin: 0, fit: 'none' });
    }
  }
  // overlapping labels are a legibility fault
  const tight = 0.04;
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    const aw = Math.min(a.w, widthIn(a.t.split('\n')[0], 16, true) + 0.1), bw = Math.min(b.w, widthIn(b.t.split('\n')[0], 16, true) + 0.1);
    const acx = a.x + a.w / 2, bcx = b.x + b.w / 2;
    if (Math.abs(acx - bcx) < (aw + bw) / 2 - tight && Math.abs((a.y + a.h / 2) - (b.y + b.h / 2)) < Math.min(a.h, b.h) - tight) rep.warnings.push(`figure: labels '${a.t.slice(0, 20)}' and '${b.t.slice(0, 20)}' overlap`);
  }
  rep.scale = s;
  return rep;
}

module.exports = { buildFigure, drawFigure, FAMILIES, FAMILY_DOCS };
