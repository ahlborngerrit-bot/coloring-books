# Python Coloring Book Generator — persona and competitor audit
Date: 2026-10-12. Static README and test-script review only.

## Personas
- Beginner: guided setup, small preview, understandable backend errors and clear distinction between generated art and a publishable book.
- Batch publisher: resumable jobs, per-page retries, deterministic manifest, cost/rate-limit visibility and no silent partial success.
- Print specialist: PDF preflight for page count, trim/bleed, effective DPI, color mode, margins and blank-back policy.
- Rights-conscious publisher: current provider terms, provenance and human originality review. “Free/no key” does not imply unlimited, stable or commercially cleared use.
- Accessibility-minded customer: printable contrast, broad closed regions and a readable interface.

## Concrete code concern
`test_improved_lineart.py` catches generation exceptions and prints failure but does not re-raise or set a nonzero exit code. Static finding in the inspected file; not runtime-reproduced.

## Isolated proposed patch
Initialize `failures = []` before the method loop. In each `except Exception as exc`, append `(method, str(exc))`, print the failure, continue attempting the remaining methods, then after the loop `if failures: raise SystemExit(f"{len(failures)} line-art method(s) failed")`. Add a deterministic test that injects a generator exception and asserts a nonzero exit code.

## Competitor lessons
- KDP Coloring Book Studio advertises page regeneration, consistent style, progression and cover/safe-zone exports: https://kdpcoloringbook.com/en.
- KDPEasy advertises end-to-end book + wrap production: https://www.kdpeasy.com/use-cases/coloring-books.
These are marketing claims, not proof of print acceptance. Differentiate through reproducibility, transparent QA reports and robust batch workflows.

## Follow-up
P0: fail process on failed generation and test corrupt/blank/missing outputs. P1: PDF preflight and resumable per-page manifests; bounded provider timeouts/retries and explicit rate-limit states. P2: beginner preview wizard and downloadable preflight report.

No tests were executed. The patch is a proposal and must be adapted to exact function scope and tested before use.