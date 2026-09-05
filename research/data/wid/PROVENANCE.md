---
id: data-wid-provenance
status: raw-reference
tags: [data, wid, piketty, inequality, slow-manifold, external, provenance]
created: 2026-08-02
---

# WID.world — full bulk dataset (raw external reference)

Raw, immutable snapshot of the **World Inequality Database** (Piketty / Saez / Zucman
et al.) — the maintained cross-country successor to the *Capital in the 21st Century*
spreadsheets. Acquired to serve the **slow-manifold / distributional slow-variable** role
in the phase-space classifier ([phase-space-macroeconomics](../../notes/concepts/phase-space-macroeconomics.md),
Q-2026-005). Held on disk "so we have it when we're ready" — **acquisition, not fitting.**
Pre-registration of what we test against it was done *before* download (Q-2026-005).

## Source

- **Download URL:** `https://wid.world/bulk_download/wid_all_data.zip`
- **Downloaded:** 2026-08-02
- **Reported size:** 882,403,433 bytes (~841 MB), `content-type: application/zip`
- **sha256:** `d9c5e261a0d7da0b70af6d2aef7020d9825983a7f70eaed77457e6427261805c` (verified 2026-08-02; zip integrity `unzip -t` OK; size matches reported 882,403,433 bytes exactly)
- **License / citation:** WID.world data are released for research use; cite as
  *WID.world (2026), World Inequality Database* + the standard Alvaredo–Chancel–Piketty–Saez–Zucman
  methodological references. Confirm the current citation string on wid.world before any
  publication use.

## Layout (once extracted)

WID bulk ships as **per-country flat CSVs**, not one monolith:

- `WID_data_XX.csv`     — the observations for country `XX` (ISO-2 code), long format:
  `country · variable · percentile · year · value · age · pop`.
- `WID_metadata_XX.csv` — variable definitions / units / notes for that country.
- `WID_countries.csv`   — country code table.
- (variable codebook conventions are documented on wid.world/codebook.)

## Storage decision — flat files, no database

Deliberate (see session 2026-08-02):

- WID is a **static snapshot**, read-mostly reference data → a DB server is all cost
  (running service, schema, backups) and no analytical gain.
- Stack discipline is **numpy + matplotlib only**; we load annual country series into
  arrays, not join millions of rows.
- The **raw zip, stamped + hashed, IS the provenance record** — a DB would obscure it.
- Escalation point *if* SQL-style querying is ever wanted: **SQLite** (single file, no
  server, ships with Python). Not needed now.

Pattern: **immutable raw zip → thin numpy loader when we build.** Do not edit `raw/`.

## Status

Raw reference only. **No model consumes this yet.** Building a slow–fast substrate on it
is the ticket-worthy crossing (`CYB-<n>`), per the collaboration protocol — not done here.

## Related

[Phase-Space Macroeconomics](../../notes/concepts/phase-space-macroeconomics.md) ·
[Natural-experiment portfolio](../../notes/concepts/natural-experiment-portfolio.md) ·
[Piketty](../../notes/people/piketty.md) · [Open questions](../../indexes/questions.md)
