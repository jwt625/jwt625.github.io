// Functional schematic generated from PIC_DATA. Devices are placed by role (one template per TX chain / RX unit);
// each wire is linked to the traced waveguide components found between its two devices in the connection graph.
window.buildSchematic = function (DATA) {
  const NS = 'http://www.w3.org/2000/svg';
  const byId = Object.fromEntries(DATA.components.map(c => [c.id, c]));
  const has = id => !!(id && byId[id]);
  const pick = (...ids) => ids.find(has) || null;
  const items = [];
  const mk = (tag, a) => { const n = document.createElementNS(NS, tag); for (const k in a) n.setAttribute(k, a[k]); return n; };

  // undirected adjacency for route lookup
  const adj = {};
  DATA.connections.forEach(({ from, to }) => { (adj[from] = adj[from] || []).push(to); (adj[to] = adj[to] || []).push(from); });
  function wgPath(a, b) {
    if (!has(a) || !has(b)) return [];
    const prev = { [a]: null }, q = [a];
    while (q.length) {
      const n = q.shift();
      for (const m of adj[n] || []) {
        if (m in prev) continue;
        prev[m] = n;
        if (m === b) { const out = []; let p = prev[b]; while (p && p !== a) { out.unshift(p); p = prev[p]; } return out; }
        if (has(m) && byId[m].cat === 'wg') q.push(m);
      }
    }
    return [];
  }

  // ---------- items ----------
  function device(kind, comp, x, y, w, h, label, opt = {}) {
    if (!comp) return;
    const it = { comps: [comp], anchor: [x + w / 2, y + h / 2] };
    it.draw = (g, col) => {
      const s = { stroke: col, 'stroke-width': 1.3, fill: col, 'fill-opacity': 0.13 };
      const sl = { stroke: col, 'stroke-width': 1, fill: 'none' };
      const cx = x + w / 2, cy = y + h / 2;
      switch (kind) {
        case 'dbr': g.appendChild(mk('rect', { x, y, width: w, height: h, ...s }));
          for (let yy = y + 4; yy < y + h - 1; yy += 4) g.appendChild(mk('line', { x1: x + 3, y1: yy, x2: x + w - 3, y2: yy, ...sl, opacity: 0.7 })); break;
        case 'split': g.appendChild(mk('polygon', { points: `${x},${cy - 4} ${x + w},${y} ${x + w},${y + h} ${x},${cy + 4}`, ...s })); break;
        case 'comb': g.appendChild(mk('polygon', { points: `${x},${y} ${x + w},${cy - 4} ${x + w},${cy + 4} ${x},${y + h}`, ...s })); break;
        case 'soa': g.appendChild(mk('polygon', { points: `${x},${y} ${x + w},${cy} ${x},${y + h}`, ...s })); break;
        case 'pd': g.appendChild(mk('polygon', { points: `${x},${y} ${x + w - 3},${cy} ${x},${y + h}`, ...s }));
          g.appendChild(mk('line', { x1: x + w - 2, y1: y, x2: x + w - 2, y2: y + h, stroke: col, 'stroke-width': 1.6 })); break;
        case 'term': g.appendChild(mk('path', { d: `M${x},${cy} a${w / 2},${h / 2} 0 1 1 ${w / 2},${h / 2}`, ...sl, 'stroke-width': 1.3 })); break;
        case 'port': g.appendChild(mk('polygon', { points: opt.left ? `${x + w},${cy - 2} ${x},${y} ${x},${y + h} ${x + w},${cy + 2}` : `${x},${cy - 2} ${x + w},${y} ${x + w},${y + h} ${x},${cy + 2}`, ...s }));
          g.appendChild(mk('line', { x1: opt.left ? x : x + w, y1: y - 6, x2: opt.left ? x : x + w, y2: y + h + 6, stroke: col, 'stroke-width': 2 })); break;
        case 'ph': g.appendChild(mk('rect', { x, y, width: w, height: h, ...s }));
          { let d = `M${x + 3},${cy}`; for (let xx = x + 3, i = 0; xx < x + w - 4; xx += 5, i++) d += ` L${xx + 2.5},${cy + (i % 2 ? 3 : -3)}`; g.appendChild(mk('path', { d, ...sl })); } break;
        case 'mod': g.appendChild(mk('rect', { x, y, width: w, height: h, ...s }));
          g.appendChild(mk('line', { x1: x + 4, y1: y + 2.5, x2: x + w - 4, y2: y + 2.5, stroke: col, 'stroke-width': 1.6 }));
          g.appendChild(mk('line', { x1: x + 4, y1: y + h - 2.5, x2: x + w - 4, y2: y + h - 2.5, stroke: col, 'stroke-width': 1.6 })); break;
        case 'group': g.appendChild(mk('rect', { x, y, width: w, height: h, fill: 'none', stroke: col, 'stroke-width': 0.8, 'stroke-dasharray': '3 2', opacity: 0.8 })); break;
        default: g.appendChild(mk('rect', { x, y, width: w, height: h, ...s }));
      }
      if (label) {
        const t = mk('text', { x: cx, y: cy + 3.5, 'font-size': opt.fs || 9, fill: '#c9ced6', 'text-anchor': 'middle', 'pointer-events': 'none' });
        t.textContent = label; g.appendChild(t);
      }
    };
    // group frames are hit on their border only, so the PDs inside stay hoverable
    it.hit = () => kind === 'group'
      ? mk('rect', { x, y, width: w, height: h, fill: 'none', stroke: 'transparent', 'stroke-width': 5, 'pointer-events': 'stroke' })
      : mk('rect', { x: x - 2, y: y - 2, width: w + 4, height: h + 4, fill: 'transparent', 'pointer-events': 'all' });
    it.highlight = (g, col) => g.appendChild(mk('rect', { x: x - 3, y: y - 3, width: w + 6, height: h + 6, fill: col, 'fill-opacity': 0.18, stroke: col, 'stroke-width': 2.2 }));
    items.push(it);
  }
  function wire(pts, a, b) {
    const comps = wgPath(a, b);
    const m = Math.floor((pts.length - 1) / 2), n = Math.ceil((pts.length - 1) / 2);
    const it = { comps, wire: true, anchor: [(pts[m][0] + pts[n][0]) / 2, (pts[m][1] + pts[n][1]) / 2] };
    const P = pts.map(p => p.join(',')).join(' ');
    it.draw = (g, col) => g.appendChild(mk('polyline', { points: P, fill: 'none', stroke: comps.length ? col : '#56606e', 'stroke-width': 1.3, opacity: 0.75, 'stroke-linejoin': 'round' }));
    it.hit = () => mk('polyline', { points: P, fill: 'none', stroke: 'transparent', 'stroke-width': 8, 'pointer-events': 'stroke' });
    it.highlight = (g, col) => {
      g.appendChild(mk('polyline', { points: P, fill: 'none', stroke: col, 'stroke-width': 6, opacity: 0.3, 'stroke-linejoin': 'round' }));
      g.appendChild(mk('polyline', { points: P, fill: 'none', stroke: col, 'stroke-width': 2.2, 'stroke-linejoin': 'round' }));
    };
    items.unshift(it); // wires below devices
  }
  function text(x, y, s, o = {}) {
    items.push({ comps: [], draw: g => { const t = mk('text', { x, y, 'font-size': o.fs || 10, fill: o.c || '#8a929e', 'text-anchor': o.a || 'start', 'font-weight': o.b ? 600 : 400 }); t.textContent = s; g.appendChild(t); } });
  }
  function line(pts, o = {}) {
    items.push({ comps: [], draw: g => g.appendChild(mk('polyline', { points: pts.map(p => p.join(',')).join(' '), fill: 'none', stroke: o.c || '#2a2f38', 'stroke-width': o.w || 1 })) });
  }

  // ---------- laser column (vertical, between rows centered at oy+105 and oy+345) ----------
  function laser(ox, oy, L) {
    const x = ox + 12, w = 24;
    device('dbr', L.top, x, oy + 130, w, 46, '');
    device('box', L.gain, x, oy + 180, w, 66, 'G');
    device('box', L.phase, x, oy + 250, w, 18, 'φ', { fs: 10 });
    device('dbr', L.bot, x, oy + 272, w, 46, '');
    text(x - 6, oy + 214, 'DBR laser', { fs: 8, a: 'end', c: '#6b7380' });
  }

  // ---------- TX IQ chain (row centered at oy+105) ----------
  function txChain(ox, oy, P, fromTop, laserId) {
    const c = oy + 105, ci = oy + 60, cq = oy + 150, X = v => ox + v;
    text(X(70), oy + 18, P.title, { b: true, c: '#c9ced6' });
    wire(fromTop ? [[X(24), oy + 130], [X(24), c], [X(70), c]] : [[X(24), oy + 78], [X(24), c], [X(70), c]], laserId, P.split1);
    device('split', P.split1, X(70), c - 50, 26, 100, '');
    if (P.term1) device('term', P.term1, X(58), c + 10, 8, 8, '');
    wire([[X(96), ci], [X(130), ci]], P.split1, P.spl_i);
    wire([[X(96), cq], [X(130), cq]], P.split1, P.spl_q);
    device('split', P.spl_i, X(130), oy + 32, 22, 56, '');
    device('split', P.spl_q, X(130), oy + 122, 22, 56, '');
    [['I1', oy + 38, 'i'], ['I2', oy + 82, 'i'], ['Q1', oy + 128, 'q'], ['Q2', oy + 172, 'q']].forEach(([a, y, g]) => {
      const A = P.arms[a], s2 = g === 'i' ? P.spl_i : P.spl_q, cb = g === 'i' ? P.comb_i : P.comb_q;
      wire([[X(152), y], [X(175), y]], s2, A.mod);
      device('mod', A.mod, X(175), y - 8, 118, 16, a + ' RF', { fs: 8.5 });
      wire([[X(293), y], [X(310), y]], A.mod, A.amp);
      device('box', A.amp, X(310), y - 7, 26, 14, a + 'A', { fs: 7.5 });
      wire([[X(336), y], [X(350), y]], A.amp, A.ph);
      device('ph', A.ph, X(350), y - 7, 80, 14, '');
      text(X(390), y - 9, a + 'P', { fs: 7.5, a: 'middle' });
      wire([[X(430), y], [X(447), y]], A.ph, cb);
    });
    device('comb', P.comb_i, X(447), oy + 32, 24, 56, '');
    device('comb', P.comb_q, X(447), oy + 122, 24, 56, '');
    [[P.comb_i, P.tap_i, P.pd_im, P.term_im, ci, -1, P.mon_i], [P.comb_q, P.tap_q, P.pd_qm, P.term_qm, cq, 1, P.mon_q]].forEach(([cb, tp, pd, tm, y, dir, lab]) => {
      wire([[X(471), y], [X(492), y]], cb, tp);
      device('box', tp, X(492), y - 4, 16, 8, '');
      wire([[X(500), y + 4 * dir], [X(500), y + 24 * dir], [X(522), y + 24 * dir]], tp, pd);
      device('pd', pd, X(522), y + 24 * dir - 7, 14, 14, '');
      text(X(529), y + 24 * dir + (dir > 0 ? 18 : -10), lab, { fs: 7.5, a: 'middle' });
      if (tm) { wire([[X(536), y + 24 * dir], [X(546), y + 24 * dir]], pd, tm); device('term', tm, X(546), y + 24 * dir - 4, 8, 8, ''); }
      wire([[X(508), y], [X(560), y], [X(560), c + 12 * dir], [X(578), c + 12 * dir]], tp, P.comb_iq);
    });
    device('comb', P.comb_iq, X(578), c - 18, 24, 36, '');
    wire([[X(602), c], [X(622), c]], P.comb_iq, P.tap_c);
    device('box', P.tap_c, X(622), c - 4, 16, 8, '');
    wire([[X(630), c - 4], [X(630), c - 28], [X(648), c - 28]], P.tap_c, P.pd_cpd);
    device('pd', P.pd_cpd, X(648), c - 35, 14, 14, '');
    text(X(655), c - 40, P.mon_c, { fs: 7.5, a: 'middle' });
    if (P.term_cpd) { wire([[X(662), c - 28], [X(672), c - 28]], P.pd_cpd, P.term_cpd); device('term', P.term_cpd, X(672), c - 32, 8, 8, ''); }
    wire([[X(638), c], [X(665), c]], P.tap_c, P.soa);
    device('soa', P.soa, X(665), c - 12, 30, 24, '');
    text(X(680), c + 24, 'SOA', { fs: 7.5, a: 'middle' });
    wire([[X(695), c], [X(722), c]], P.soa, P.port);
    device('port', P.port, X(722), c - 8, 26, 16, '');
    text(X(752), c + 3.5, P.portLabel, { fs: 9.5, c: '#e0e4ea', b: true });
  }
  function txIds(pre, pol) {
    const g = (...s) => pick(...s.map(x => `${pre}_${pol}_${x}`));
    const arm = a => ({ mod: g(`mod_${a}`, `mod_${a.toLowerCase()}`), amp: g(`amp_${a}`, `amp_${a.toLowerCase()}`), ph: g(`ph_${a}`, `ph_${a.toLowerCase()}`) });
    return { split1: g('mmi1', 'split1'), term1: g('term_mmi1'), spl_i: g('spl_i', 'split2_i'), spl_q: g('spl_q', 'split2_q'),
      arms: { I1: arm('I1'), I2: arm('I2'), Q1: arm('Q1'), Q2: arm('Q2') },
      comb_i: g('comb_i'), comb_q: g('comb_q'), tap_i: g('tap_i'), tap_q: g('tap_q'), pd_im: g('pd_im'), pd_qm: g('pd_qm'),
      term_im: g('term_im'), term_qm: g('term_qm'), comb_iq: g('comb_iq'), tap_c: g('tap_c', 'tap_cpd'), pd_cpd: g('pd_cpd'), term_cpd: g('term_cpd'),
      soa: g('soa'), port: g('port') };
  }
  function txUnit(ox, oy, n, L) {
    text(ox, oy - 22, `TX unit ${n}: laser ${n} → TE${n} / TM${n} IQ modulators`, { fs: 11, b: true, c: '#e0e4ea' });
    laser(ox, oy, L);
    txChain(ox, oy, Object.assign(txIds(`tx${n}`, 'te'), { title: `TE${n}`, portLabel: `TE${n}`, mon_i: 'TEIM', mon_q: 'TEQM', mon_c: 'TECPD' }), true, L.top);
    txChain(ox, oy + 240, Object.assign(txIds(`tx${n}`, 'tm'), { title: `TM${n}`, portLabel: `TM${n}`, mon_i: 'TMIM', mon_q: 'TMQM', mon_c: 'TMCPD' }), false, L.bot);
  }

  // ---------- RX row: splitter output -> hybrid <- signal port; hybrid -> 2 balanced PD pairs + 3 dummy ports ----------
  // flip: LO enters on the lower hybrid input and the signal port sits above (keeps the upward WLL branch uncrossed)
  function rxRow(ox, oy, B, splitId, loLabel, portLabel, title, flip) {
    const c = oy + 105, X = v => ox + v, sgn = flip ? -1 : 1;
    text(X(70), oy + 8, title, { b: true, c: '#c9ced6' });
    wire([[X(96), c - 14 * sgn], [X(330), c - 14 * sgn]], splitId, B.hyb);
    text(X(215), c - 14 * sgn - 4, loLabel, { fs: 7.5, a: 'middle' });
    device('port', B.port, X(196), c + 40 * sgn - 8, 26, 16, '', { left: true });
    text(X(192), c + 40 * sgn + 4, portLabel, { fs: 9.5, c: '#e0e4ea', b: true, a: 'end' });
    wire([[X(222), c + 40 * sgn], [X(300), c + 40 * sgn], [X(300), c + 14 * sgn], [X(330), c + 14 * sgn]], B.port, B.hyb);
    text(X(262), c + 40 * sgn + (flip ? -5 : 12), 'signal', { fs: 7.5, a: 'middle' });
    device('box', B.hyb, X(330), c - 58, 52, 116, '90°', { fs: 11 });
    device('group', B.bpd_o, X(440), c - 56, 34, 44, '');
    device('group', B.bpd_v, X(440), c + 12, 34, 44, '');
    text(X(480), c - 30, 'BPD', { fs: 7.5 });
    text(X(480), c + 38, 'BPD', { fs: 7.5 });
    [[B.pd_o1, c - 46], [B.pd_o2, c - 22], [B.pd_v1, c + 22], [B.pd_v2, c + 46]].forEach(([pd, y]) => {
      wire([[X(382), y], [X(450), y]], B.hyb, pd); device('pd', pd, X(450), y - 7, 14, 14, '');
    });
    [[B.d1, c - 34], [B.d2, c], [B.d3, c + 34]].forEach(([d, y]) => { if (d) { wire([[X(382), y], [X(398), y]], B.hyb, d); device('term', d, X(398), y - 4, 8, 8, ''); } });
    text(X(410), c + 3, 'dummy', { fs: 7, c: '#6b7380' });
  }
  function rxIds(b) {
    const g = s => pick(`rxsig_${b}_${s}`);
    return { port: g('port'), hyb: g('hyb'), d1: g('dummy1'), d2: g('dummy2'), d3: g('dummy3'), bpd_o: g('bpd_o'), bpd_v: g('bpd_v'),
      pd_o1: g('pd_o1'), pd_o2: g('pd_o2'), pd_v1: g('pd_v1'), pd_v2: g('pd_v2') };
  }
  function rxUnit(ox, oy, n, topB, botB, topPort, botPort, flipTop) {
    const p = `rxlo_l${n}_`, L = { top: pick(p + 'mir_top'), gain: pick(p + 'gain'), phase: pick(p + 'phase'), bot: pick(p + 'mir_bot') };
    text(ox, oy - 22, `RX unit ${n}: LO laser ${n} → ${topB.toUpperCase()} / ${botB.toUpperCase()} coherent receivers`, { fs: 11, b: true, c: '#e0e4ea' });
    laser(ox, oy, L);
    const ts = pick(p + 'top_split'), bs = pick(p + 'bot_split'), c1 = oy + 105, c2 = oy + 345;
    wire([[ox + 24, oy + 130], [ox + 24, c1], [ox + 70, c1]], L.top, ts);
    device('split', ts, ox + 70, c1 - 22, 26, 44, '');
    rxRow(ox, oy, rxIds(topB), ts, `LO${n}`, topPort, `${topB.toUpperCase()} receiver`, flipTop);
    wire([[ox + 24, oy + 318], [ox + 24, c2], [ox + 70, c2]], L.bot, bs);
    device('split', bs, ox + 70, c2 - 22, 26, 44, '');
    rxRow(ox, oy + 240, rxIds(botB), bs, `LO${n}`, botPort, `${botB.toUpperCase()} receiver`, false);
    // monitor PD on the bottom-end splitter
    const mpd = pick(p + 'mpd'), mt = pick(p + 'mpd_term');
    wire([[ox + 96, c2 + 14], [ox + 118, c2 + 14], [ox + 118, c2 + 72], [ox + 140, c2 + 72]], bs, mpd);
    device('pd', mpd, ox + 140, c2 + 65, 14, 14, '');
    text(ox + 147, c2 + 92, 'MPD', { fs: 7.5, a: 'middle' });
    if (mt) { wire([[ox + 154, c2 + 72], [ox + 164, c2 + 72]], mpd, mt); device('term', mt, ox + 164, c2 + 68, 8, 8, ''); }
    return { ts, c: c1 };
  }

  // ---------- layout ----------
  txUnit(0, 0, 1, { top: pick('tx1_dbr_n'), gain: pick('tx1_gain'), phase: pick('tx1_phase'), bot: pick('tx1_dbr_s') });
  txUnit(0, 520, 2, { top: pick('tx2_dbr_top'), gain: pick('tx2_gain'), phase: pick('tx2_laser_phase'), bot: pick('tx2_dbr_bot') });
  const RX = 860, X = v => RX + v;
  const u1 = rxUnit(RX, 0, 1, 'te1', 'tm1', 'TE3', 'TM3', false);
  const u2 = rxUnit(RX, 520, 2, 'tm2', 'te2', 'TM4', 'TE4', true);
  // WLL: each top-end splitter -> SH section -> 2x1 junction -> WLL port
  const wc = pick('rxlo_wll_comb'), wp = pick('rxlo_wll_port'), yj = 485;
  [[u1, pick('rxlo_sh_right'), 1, 'SH1'], [u2, pick('rxlo_sh_left'), -1, 'SH2']].forEach(([u, sh, d, lab]) => {
    const yb = u.c + 76 * d;
    wire([[X(96), u.c + 14 * d], [X(118), u.c + 14 * d], [X(118), yb], [X(560), yb]], u.ts, sh);
    device('soa', sh, X(560), yb - 10, 26, 20, '');
    text(X(573), yb + (d > 0 ? 22 : -14), lab, { fs: 7.5, a: 'middle' });
    wire([[X(586), yb], [X(680), yb], [X(680), yj - 10 * d], [X(700), yj - 10 * d]], sh, wc);
  });
  device('comb', wc, X(700), yj - 16, 22, 32, '');
  wire([[X(722), yj], [X(740), yj]], wc, wp);
  device('port', wp, X(740), yj - 8, 26, 16, '');
  text(X(770), yj + 3.5, 'WLL', { fs: 9.5, c: '#e0e4ea', b: true });
  text(X(620), yj + 3, 'light direction N/A', { fs: 7.5, a: 'middle', c: '#6b7380' });
  line([[835, -40], [835, 990]]);
  text(820, -32, 'TX', { a: 'end', b: true, c: '#6b7380' });
  text(850, -32, 'RX', { b: true, c: '#6b7380' });
  text(0, 980, 'All optical ports (TE1-TM2 out, TE3-TM4 signal in, WLL) are on the bottom facet of the die.', { fs: 9, c: '#6b7380' });
  return { viewBox: [-70, -55, 1740, 1055], items };
};
