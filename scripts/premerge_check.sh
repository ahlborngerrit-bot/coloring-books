#!/usr/bin/env bash
# Pre-merge gate (same pattern as compressor/scripts/premerge_check.sh). Checks only — merging stays manual.
#
#   scripts/premerge_check.sh        # check the current checkout
#   scripts/premerge_check.sh 123    # check PR 123 merged with origin/main in a temp worktree (no merge)
#
# Steps (all run, then a PASS/FAIL/SKIP summary):
#   1 lock installable (pip install --require-hashes -r requirements-dev.lock, into the chosen venv)
#   2 tests (pytest, offline; live API tests skipped unless RUN_NETWORK_TESTS=1)
#   3 ruff (ruff.toml, per-file baseline)   4 markdown links   5 gitleaks (full history, .gitleaks.toml)
# Exit codes: 0 green · 1 red step(s) · 2 tool missing · 3 merge conflict with main.
set -euo pipefail
PR="${1:-}"
ROOT="$(git rev-parse --show-toplevel)"
if [ -n "${PYTHON:-}" ]; then PY="$PYTHON"
elif [ -x "$ROOT/.venv/bin/python" ]; then PY="$ROOT/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY=python3
else echo "PREMERGE: python fehlt"; exit 2; fi
command -v git >/dev/null 2>&1 || { echo "PREMERGE: git fehlt"; exit 2; }
WORK="$ROOT"
cleanup() { [ -n "${TMPWT:-}" ] && git -C "$ROOT" worktree remove --force "$TMPWT" >/dev/null 2>&1 || true; }
trap cleanup EXIT

if [ -n "$PR" ]; then
  git -C "$ROOT" fetch -q origin main "pull/$PR/head:premerge-$PR" --force
  TMPWT="$(mktemp -d /tmp/premerge-XXXX)"
  git -C "$ROOT" worktree add -q --detach "$TMPWT" "premerge-$PR"
  WORK="$TMPWT"
  git -C "$WORK" -c user.email=gate@local -c user.name=premerge merge -q --no-edit origin/main \
    || { echo "PREMERGE: Konflikt mit main – nicht mergen"; exit 3; }
fi
cd "$WORK"

RESULTS=()
FAILED=0
step() {  # step "<name>" cmd...
  local name="$1"; shift
  echo "== $name"
  local t0=$SECONDS
  if "$@"; then RESULTS+=("PASS  $name ($((SECONDS - t0))s)")
  else RESULTS+=("FAIL  $name ($((SECONDS - t0))s): $*"); FAILED=$((FAILED + 1)); fi
}
skip() { echo "== $1 — SKIP: $2"; RESULTS+=("SKIP  $1: $2"); }

step "Lock installierbar (requirements-dev.lock, --require-hashes)" "$PY" -m pip install -q --disable-pip-version-check --require-hashes -r requirements-dev.lock
step "Tests (pytest, offline)" "$PY" -m pytest -q -p no:cacheprovider
step "Ruff (ruff.toml)" "$PY" -m ruff check .
step "Markdown-Links" "$PY" scripts/check_md_links.py
if command -v gitleaks >/dev/null 2>&1; then
  step "gitleaks (Historie, .gitleaks.toml)" gitleaks git --no-banner --redact --config .gitleaks.toml .
elif [ -n "${CI:-}" ]; then
  step "gitleaks" false  # CI must have it
else
  skip "gitleaks" "gitleaks nicht installiert (CI führt den Scan aus)"
fi

echo
echo "== PREMERGE SUMMARY ($(git rev-parse --short HEAD), python: $PY)"
printf '   %s\n' "${RESULTS[@]}"
if [ "$FAILED" -gt 0 ]; then
  echo "PREMERGE ROT: $FAILED Schritt(e) fehlgeschlagen – nicht mergen"
  exit 1
fi
echo "PREMERGE GRÜN (Merge bleibt manuell)"
