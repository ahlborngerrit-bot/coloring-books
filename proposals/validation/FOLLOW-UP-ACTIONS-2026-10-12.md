# Follow-up actions — 2026-10-12

## Verified evidence update

Validation PR #4 head `8d67f6f617855dbb341fda861219069d180268f5` has no GitHub Actions run returned by an exact-SHA query. The January test report remains historical. No current generator test or build is claimed as executed.

Static repository inspection confirms `test_improved_lineart.py` constructs a Pollinations backend and calls `generate_book`; it performs remote image generation and must not be used as an ordinary smoke test.

## Next orders for Grokbot

1. Inspect all test scripts to classify them as offline/unit, filesystem/PDF, or remote-provider tests before running anything.
2. Start with `python -m compileall -q coloring_book_generator.py complete_book_workflow.py cover_generator.py` in a disposable environment.
3. Inspect `requirements.txt` and pin/lock reproducible dependencies in a separate proposal; record Python version and platform.
4. Run only confirmed offline tests first. Do not run `test_improved_lineart.py`, full-book generation, or remote image requests until provider limits, cost, terms, and commercial-use permissions are checked.
5. Add deterministic tests for image thresholding, output dimensions, PDF page count, corrupt/blank outputs and cleanup behavior without deleting existing user files.

## Guardrails

No external image generation by default, no provider spend without explicit budget approval, no claims of KDP compliance without a current checklist and actual output inspection.