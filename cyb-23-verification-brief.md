# Verification brief — CYB-23: is the "inflationary, not deflationary" collapse a *conditional* result?

## Why this matters
We're about to describe CYB-23's headline result in outreach to a Minsky/Keen-orbit economist. Before it goes anywhere near an expert, I need the ground truth, because the framing hinges entirely on it. Reconstructing from the ticket (not the code), the claim is that the inflationary-contagion collapse is a **conditional** finding — NOT a contradiction of debt-deflation. Verify that against the actual code and committed results. **If the reconstruction is wrong, say so plainly — a correction here is worth far more than a confirmation.** We are trying not to overclaim to someone who will know.

## The reconstruction to check
The belief is that the collapse comes out inflationary *because*:
1. the Fisher / price-level engine was deliberately gated **OFF** in the headline runs;
2. the demand/price channel was verified **too weak to pull the price level negative** on its own (something like min ≈ −0.00%/step); and
3. forcing the Fisher gate **ON** *does* produce deflation.

If all three hold, the honest characterization is: "two collapse engines; which one you land in is parametric, gated by the strength of the price channel — and in the shipped configuration the *spontaneously reachable* collapse is inflationary, while the deflationary regime is reachable only when forced." That is a conditional result, not a refutation of the canon.

## Specific checks (read/verify existing code + results — no rebuild unless genuinely ambiguous)
1. In the CYB-23 headline runs, was the Fisher / price-level engine actually gated OFF (not contributing)? Confirm from the model config and `run_v0`.
2. What did the demand-channel-strength verification actually conclude? Quote the real number and what it means — can that channel drive the price level negative on its own, or not?
3. With the Fisher gate forced ON, does the model actually produce a deflationary collapse? Under what parameters — a switch, or a sweep? Is the deflationary regime reachable at all, and how "forced" is reaching it?
4. Therefore: is the one-line characterization above correct, or is the real result stronger / different? (e.g. collapse stays inflationary even with Fisher on; or deflation isn't reachable at all; or the verification said something other than what I remember.)
5. If visible: what parameter(s) set the inflationary-vs-deflationary boundary, and is there a clean threshold?

## Deliverable
A short written answer (a comment on CYB-23 is fine) that plainly states whether the reconstruction holds, cites the actual figures, and gives the single most honest one-sentence characterization of what the model showed. No modeling work needed unless a point is genuinely ambiguous and needs one confirming run.
