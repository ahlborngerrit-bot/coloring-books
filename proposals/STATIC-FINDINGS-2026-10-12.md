# Static technical findings — 2026-10-12

Scope: source inspection only. No local execution, provider request, PDF generation, or test command was performed in this environment. These are reproducible code observations, not runtime-confirmed failures. Original files remain untouched.

## F-001 — Test runner can report success after failures
**Evidence:** root `test_improved_lineart.py` catches exceptions inside the loop and prints them, but never aggregates failures or exits non-zero. The quick test similarly catches and prints exceptions without a non-zero exit. The script can therefore exit with status 0 after generation failed.
**Risk:** CI/automation can produce false-green results.
**Candidate:** `proposals/code/test_improved_lineart.py` returns non-zero on caught errors, but this candidate is still incomplete: it checks only whether `generate_book` returned a truthy path. The inspected `generate_book` implementation always returns `book_dir` after the loop, even if zero pages were generated. So the candidate can still report PASS for an empty/partial book.
**Next action:** keep the original and first candidate; add a new version that verifies the directory, metadata `pages_data` count, each referenced image file, image dimensions/color distribution/DPI, and the generated PDF when requested. Add deterministic unit tests using a fake backend. Run network-provider integration only as an opt-in test.

## F-002 — Quality validator counts scalar channel values, not actual RGB colors
**Evidence:** `validate_image_quality` does `arr = np.array(img)` followed by `len(np.unique(arr))`. For RGB/RGBA images this counts distinct scalar channel values, not distinct pixel colors. An image with many different colored pixels can still have only a small set of scalar values, so this does not prove black-and-white line art.
**Risk:** colored or otherwise unsuitable pages may pass the “binary” check.
**Recommended candidate:** normalize to grayscale or inspect per-pixel RGB tuples after converting to RGB; require pixels to be near pure black/white under a documented threshold; measure the percentage of non-binary pixels. Include a deliberately colored fixture that must fail.

## F-003 — DPI and color checks are warnings, not validity failures
**Evidence:** low DPI metadata and too many “colors” append entries to `warnings`, while `valid` remains true. The generator only rejects a page when `validation['valid']` is false.
**Risk:** output can be recorded as validated even when print metadata or line-art properties are unsuitable.
**Recommended candidate:** define explicit release policy: hard-fail on insufficient pixel dimensions, unreadable/corrupt file, unacceptable non-binary pixels, and missing expected files; warn or fail on DPI metadata according to the output format. Verify actual PDF physical page dimensions and embedded image resolution separately.

## F-004 — Book-level completion is not enforced
**Evidence:** `generate_book` logs `Generated {len(generated)}/{num_pages} pages` and returns `book_dir` even when fewer pages than requested were accepted.
**Risk:** calling code can mistake partial output for a complete book.
**Recommended candidate:** expose a structured result with requested/accepted/failed counts or raise a dedicated exception in a proposed version. Since the original product must not be changed by this audit, prototype this separately and include regression tests for 0/N, N-1/N, and N/N outputs.

## F-005 — PDF generation needs independent postflight checks
**Evidence:** `create_pdf` returns `None` when it cannot create a PDF and otherwise writes a PDF, but the current test script does not validate PDF existence, page count, page dimensions, or whether every expected image appears.
**Risk:** a file existing is mistaken for a print-ready artifact.
**Recommended candidate:** use a PDF parser in tests to assert page count, page size and non-empty page content. Inspect a rasterized proof of every page before commercial publication.

## Prioritized next work
1. Add deterministic tests for F-001 through F-005 with no network calls.
2. Implement a candidate quality validator in a new proposal file, not in the product module.
3. Run static typing/lint and tests in a connected clean checkout; record exact command, environment, exit code and output.
4. Only after deterministic tests pass, run provider integration under current provider terms and known limits.
5. Human-inspect a full sample PDF before calling it print-ready.

## Status
- Findings: static review.
- Tests authored: not in this file.
- Tests executed: none.
- Product source changes: none.
- Deletion: none.
