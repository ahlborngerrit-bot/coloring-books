# Grok / Grokbot handover — Python Coloring Book Generator

Review PR: https://github.com/ahlborngerrit-bot/coloring-books/pull/3
Base: `main`; review branch: `review/chatgpt-audit-2026-10-12`.

New file: `AUDIT_CHATGPT_2026-10-12.md`. It covers weak image assertions, PDF print-preflight gaps, external provider limits/timeouts, reproducibility and rights/QA caveats.

Please reproduce findings against current source. Run the existing tests from a clean environment and record exact commands, commit SHA and exit codes. Add deterministic fixture tests for image dimensions, blank/corrupt pages, line-art constraints, PDF page boxes/count/DPI and bounded provider retries. Verify current provider terms and KDP requirements from primary sources. Keep any fixes in a separate proposal branch; do not modify product source on main. The existing `TEST_RESULTS.md` is historical evidence, not a current run. No test is claimed as executed in this audit.

## Persona review update
Added `PERSONA-AND-COMPETITOR-AUDIT-2026-10-12.md`. It flags that `test_improved_lineart.py` prints failures without failing the process; proposed isolated patch and deterministic test are described but not executed.


## Mandatory change-control policy (owner instruction, 2026-10-12)

- Do not delete files, folders, branches, commits, PRs, content, or history. Only the repository owner or Grokbot may authorize and perform deletion.
- Do not alter product source on the default branch as part of this review. Put candidate code and proposed changes in clearly named review/proposals paths or a separate review branch.
- Preserve existing proposal content. Add new sections or new files; do not replace a file without first reading it and preserving its existing content.
- Do not merge, close, squash, rebase destructively, force-push, or mark a PR ready without explicit owner authorization.
- Label evidence precisely: static observation, executed command, test result, independently reproduced finding, or unverified hypothesis. Never describe a test/build/security audit as complete without evidence.
- Verify every write by re-reading the file and inspecting the PR changed-file list. Check that the diff contains no deletions and no product-source changes.
- For suspected obsolete or duplicate content, document the conflict and recommend a disposition. Leave it intact for the owner/Grokbot to decide.


## New static technical findings + validation candidate (2026-10-12)
- Read `proposals/STATIC-FINDINGS-2026-10-12.md` for the root script false-green behavior, RGB scalar-count issue, warning-only quality checks, missing book-level completion gate and PDF postflight gap.
- `proposals/code/test_improved_lineart.py` is a first candidate; it is insufficient by itself because `generate_book` can return a directory after generating fewer than the requested number of pages.
- `proposals/code/test_improved_lineart_v2.py` and `proposals/code/README-v2.md` add artifact-level checks. They are proposals only and have NOT been executed. Check dependencies, syntax, output metadata schema and strict print-quality policy before adoption.
- No product source changed; no provider generation or test was run. Do not describe this project as currently validated or production-ready from the historical `TEST_RESULTS.md` alone.
- Preserve all originals and previous candidates. Do not delete or replace any file.
