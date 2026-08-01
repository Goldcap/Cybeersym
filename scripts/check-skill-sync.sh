#!/usr/bin/env bash
# Drift-guard: the cybeersym-research skill is discovered by two runtimes at two paths —
# .claude/skills/ (Claude Code) and .agents/skills/ (OpenAI Codex). They MUST stay
# byte-identical, or the two agents silently follow different instructions.
set -eu
root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
a="$root/.claude/skills/cybeersym-research/SKILL.md"
b="$root/.agents/skills/cybeersym-research/SKILL.md"
if [ ! -f "$a" ] || [ ! -f "$b" ]; then
  echo "check-skill-sync: one of the skill copies is missing:" >&2
  echo "  $a" >&2; echo "  $b" >&2; exit 1
fi
if ! cmp -s "$a" "$b"; then
  echo "check-skill-sync: SKILL DRIFT — the two copies differ; edit BOTH (byte-identical):" >&2
  echo "  git --no-pager diff --no-index -- '$a' '$b'" >&2
  exit 1
fi
echo "check-skill-sync: ok (cybeersym-research skill copies are byte-identical)."
