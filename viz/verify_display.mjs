// CI display-logic regression gate. The math can be perfect while the *illustration* fails to show
// it (reviewer gate, 2026-09-07: the d0 slider never repainted the breakdown region, and the Hopf
// contour was never drawn). This test extracts the model block + the grid/BUDGET constants from
// viz/index.html and reimplements the map classifier exactly, then asserts the demonstration is
// actually visible: both regime bands exist, the Hopf boundary has segments (scanned on BOTH axes),
// and the breakdown overlay fires and grows with d0. Run from repo root: `node viz/verify_display.mjs`.
import fs from "node:fs";

const html = fs.readFileSync("viz/index.html", "utf8");
const mm = html.match(/\/\/ ==GK-MODEL-START==[^\n]*\r?\n([\s\S]*?)\/\/ ==GK-MODEL-END==/);
if (!mm) { console.error("FAIL: model markers not found"); process.exit(2); }
const M = new Function(mm[1] + "\n;return {P,gkStep,keenGoodEq,leadingEig};")();

function grab(re, name, n) { const m = html.match(re); if (!m) { console.error(`FAIL: could not read ${name} from viz/index.html`); process.exit(2); } return n === undefined ? m : m.slice(1, 1 + n).map(Number); }
const [R0, R1, K0, K1, NX, NY] = grab(/const R0=([-\d.]+),R1=([-\d.]+),K0=([-\d.]+),K1=([-\d.]+),NX=(\d+),NY=(\d+);/, "grid", 6);
const BUDGET = Number(grab(/const BUDGET=(\d+)/, "BUDGET")[1]);
const BASE = new Function("return (" + grab(/const BASE=(\{[^}]*\});/, "BASE")[1] + ");")();
console.log(`grid ${NX}x${NY}  r[${R0},${R1}]  k[${K0},${K1}]  BUDGET=${BUDGET}  BASE=${JSON.stringify(BASE)}`);

const rAt = ix => R0 + (ix + 0.5) / NX * (R1 - R0);
const kAt = iy => K0 + (iy + 0.5) / NY * (K1 - K0);
const pOf = (ix, iy) => M.P(Object.assign({}, BASE, { r: rAt(ix), ksharp: kAt(iy), rho: 0.5, nu: 3.0 }));
const broke = s => !isFinite(s[0]) || !isFinite(s[1]) || !isFinite(s[2]) || s[0] <= 1e-3 || Math.abs(s[2]) > 1e3;
function breaksFrom(p, d0) {
  const eq = M.keenGoodEq(p); if (!eq) return false;
  let s = [eq[0] * 0.98, eq[1] * 0.98, d0];
  for (let i = 0; i < BUDGET; i++) { const ns = M.gkStep(s, p); if (broke(ns)) return true; s = ns; }
  return false;
}
function classify(d0) {
  const reg = new Uint8Array(NX * NY), brk = new Uint8Array(NX * NY);
  for (let iy = 0; iy < NY; iy++) for (let ix = 0; ix < NX; ix++) {
    const p = pOf(ix, iy), eq = M.keenGoodEq(p), k = ix + iy * NX;
    if (!eq) { reg[k] = 0; continue; }
    reg[k] = M.leadingEig(eq, p).re < 0 ? 1 : 2;
    brk[k] = breaksFrom(p, d0) ? 1 : 0;
  }
  let stable = 0, unstable = 0, breakdown = 0;
  for (let i = 0; i < reg.length; i++) { if (reg[i] === 1) stable++; else if (reg[i] === 2) unstable++; if (brk[i]) breakdown++; }
  const st = k => reg[k] === 1; let seg = 0;
  for (let iy = 0; iy < NY; iy++) for (let ix = 0; ix < NX; ix++) { const k = ix + iy * NX; if (reg[k] === 0) continue;
    if (ix < NX - 1 && reg[k + 1] !== 0 && st(k) !== st(k + 1)) seg++;
    if (iy < NY - 1 && reg[k + NX] !== 0 && st(k) !== st(k + NX)) seg++; }
  return { stable, unstable, breakdown, hopfSegments: seg };
}

const lo = classify(0.85), hi = classify(9.0);
console.log("d0=0.85:", JSON.stringify(lo));
console.log("d0=9.0 :", JSON.stringify(hi));
const checks = [
  ["both regime bands exist (stable>0 && unstable>0)", lo.stable > 0 && lo.unstable > 0],
  ["Hopf boundary has segments (contour is drawable)", lo.hopfSegments > 0],
  ["breakdown overlay FIRES at high d0 (the d0 demo is not inert)", hi.breakdown > 0],
  ["breakdown overlay RESPONDS to d0 (grows from low→high)", hi.breakdown > lo.breakdown],
];
let ok = true;
for (const [name, pass] of checks) { console.log(`${pass ? "✓" : "✗"} ${name}`); ok = ok && pass; }
if (!ok) { console.error("DISPLAY FAIL: the viz would not demonstrate its own thesis."); process.exit(1); }
console.log("PASS — the demonstration is visible.");
