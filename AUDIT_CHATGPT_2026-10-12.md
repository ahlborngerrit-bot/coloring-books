# Coloring Book Generator — static audit

Date: 2026-10-12. Baseline main tree: a4a98789b0e798db2f98c26fd2069abc2d06ec47. The previous TEST_RESULTS.md is dated 2026-01-26; it is historical evidence, not a current test run.

## Findings

### P1: public README overstates external generation guarantees
README says Pollinations.ai is 100% free and unlimited, and calls outputs KDP-ready. An external service's availability, rate limits, terms and generated-image rights can change; code-level PDF generation does not prove Amazon KDP acceptance or commercial rights. Reword claims as current assumptions verified on a date, and make generation failure/rate-limit behavior explicit.

### P1: quality tests include weak/non-operative assertions
test_quality_assurance.py includes test_image_validation_mock that only asserts a function is available and prints success; it does not validate an image. Other tests assert constants and method presence rather than checking actual output. Replace with deterministic fixture images covering dimensions, DPI metadata, binary colors, blank/near-blank pages, corrupted images and PDF page size/count.

### P1/P2: print-ready claim needs PDF-level validation
Validate actual PDF media box, page count, embedded image dimensions, image DPI, margins/bleed and metadata; inspect a rendered PDF page-by-page. A PNG with a 300-DPI tag does not guarantee the PDF has correct physical dimensions.

### P2: external calls need bounded retries/timeouts
Review all provider HTTP calls for connect/read timeouts, bounded retries with backoff, HTTP status validation, response size caps and safe error messages. Avoid an infinite batch when a provider rate-limits or returns an invalid image.

### P2: reproducibility and cost
Batch generation needs a manifest of prompt, backend, model/version, parameters, source hash, generated asset hash, time, retries and estimated spend. Use a resumable queue and stop switch; avoid claiming a batch is unlimited or guaranteed.

### P2: content and rights QA
For each page, inspect for text artifacts, duplicates, cropped objects, trademarked characters, inconsistent style and age appropriateness. Keep generated assets and prompt provenance. A human QA gate is required before compiling a commercial book.

## Product ideas
1. PDF preflight CLI: page boxes, image DPI, margins, page count, blank/duplicate detection and report.
2. Per-page contact sheet and reviewer approval workflow.
3. Backend adapter contract tests and bounded batch queue with resumability.
4. Asset provenance manifest with prompt/model/hash and rights checklist.
5. Book-level consistency checks for character identity, line density and scene variety.

## Status
Not re-executed. Historical test results do not prove current main works. No KDP compliance, rights clearance or current provider SLA was verified.
