# Isolated code proposal: line-art test exit status

This folder contains a candidate replacement for the existing root-level `test_improved_lineart.py`.

## Why
The original catches generation exceptions and only prints them. The process can exit with status 0 even when one or more methods failed. Automation and CI may therefore report a false pass.

## Proposed change
`test_improved_lineart.py` attempts all three methods, collects failures, returns status 1 if any failed, and uses `raise SystemExit(main())`. The quick path also returns a non-zero status on failure and checks for a missing output directory result.

## Important limits
- This is a candidate copy, not a replacement of the product file.
- It has not been run against the project dependencies or a live provider.
- The generator's actual return type and output validity must be checked before adoption; a truthy path does not prove the generated images/PDF are correct.
- Add deterministic unit tests by injecting a fake generator that succeeds/fails; add image/PDF preflight tests separately.
- Do not run network-backed generation in ordinary CI. Use deterministic fixtures/mocks for CI and an opt-in integration test for the provider.
