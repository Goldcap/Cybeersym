// CI fidelity gate (the JS side). Extracts the ACTUAL Goodwin–Keen model block from viz/index.html
// (between the // ==GK-MODEL-START== / ==GK-MODEL-END== markers), runs its RK4 over the reference
// checkpoints emitted by the numpy engine (viz/fidelity-reference.json, produced by gen_reference.py),
// and fails if the JS diverges from numpy by >= TOL. Testing the extracted page code — not a copy —
// is what makes this a real anti-drift gate. Run from the repo root: `node viz/verify_fidelity.mjs`.
import fs from "node:fs";

const TOL = 1e-6;
const html = fs.readFileSync("viz/index.html", "utf8");
const m = html.match(/\/\/ ==GK-MODEL-START==[^\n]*\r?\n([\s\S]*?)\/\/ ==GK-MODEL-END==/);
if (!m) { console.error("FAIL: GK model markers not found in viz/index.html"); process.exit(2); }

// Evaluate the extracted block in an isolated function scope and hand back the entry points.
// (block-scoped consts stay local to this factory; nothing leaks to the module or global.)
let M;
try {
  M = new Function(m[1] + "\n;return {DEF,P,gkStep,keenGoodEq,rhs};")();
} catch (e) {
  console.error("FAIL: could not evaluate the extracted model block:", e.message); process.exit(2);
}

const ref = JSON.parse(fs.readFileSync("viz/fidelity-reference.json", "utf8"));
let maxErr = 0, n = 0;
for (const c of ref) {
  const p = M.P(c.params);
  let s = c.s0.slice();
  const stops = Object.keys(c.checkpoints).map(Number).sort((a, b) => a - b);
  let idx = 0;
  for (let i = 0; i <= stops[stops.length - 1]; i++) {
    if (i === stops[idx]) {
      const exp = c.checkpoints[String(i)];
      for (let k = 0; k < 3; k++) maxErr = Math.max(maxErr, Math.abs(s[k] - exp[k]));
      n++; idx++;
    }
    s = M.gkStep(s, p);
  }
}

console.log(`fidelity: max Δ = ${maxErr.toExponential(3)} over ${n} checkpoints (tol ${TOL})`);
if (!(maxErr < TOL)) {
  console.error("FIDELITY FAIL: the viz JS port diverges from the numpy engine.");
  process.exit(1);
}
console.log("PASS — viz/index.html mirrors src/goodwin_keen/model.py");
