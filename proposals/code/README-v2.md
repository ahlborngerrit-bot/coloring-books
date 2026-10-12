# Candidate v2: artifact-level line-art test runner

This is an additive alternative; the root production script and earlier candidate remain unchanged.

It checks the generator's actual `metadata.json`, expected accepted page count, referenced local image files, decodability, pixel dimensions, DPI metadata and strict black/white binary pixels. It exits non-zero on any validation issue.

## Important caveats
- Not executed in this environment. It must be syntax-checked and tested in a clean checkout before Grokbot considers it.
- This is a network-backed provider integration test, not a deterministic CI test. It must be opt-in; do not run it automatically on every pull request.
- Strict binary and DPI checks may reveal that the current pipeline does not meet the proposed print-quality threshold. That is an actionable failure, not a reason to weaken the test without documented evidence.
- Add separate deterministic unit tests for the validator using small local fixtures and a fake generator; test 0/N, N-1/N, N/N, corrupt image, color image, grayscale image, low-resolution image, missing metadata and missing image.
- DPI metadata alone does not establish physical print size. PDF page size, embedded image resolution, margins and visual defects need separate PDF-level checks and human proofing.
- NumPy is already listed in the project's requirements, and Pillow is installed as `Pillow` in requirements.
