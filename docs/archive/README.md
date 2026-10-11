# Archive

Dated reviews, session summaries and status reports from January 2026 (v2.0.1 → v2.2.1). They are kept unchanged for history. File paths mentioned inside them refer to the old root layout. For current guidance see [docs/README.md](../README.md).

| File | Date | Summary |
|---|---|---|
| [COMPREHENSIVE_REVIEW](COMPREHENSIVE_REVIEW.md) | 2026-01-26 | System validation review of v2.0.1 |
| [CODE_REVIEW](CODE_REVIEW.md) | 2026-01-26 | Code review of v2.1.0 |
| [BUGFIXES](BUGFIXES.md) | 2026-01-26 | Bug fixes and improvements in that release |
| [TROUBLESHOOTING_SESSION_SUMMARY](TROUBLESHOOTING_SESSION_SUMMARY.md) | 2026-01-26 | Session log: testing the generator and fixing production blockers |
| [TEST_RESULTS](TEST_RESULTS.md) | 2026-01-26 | Results of `test_improved_lineart.py --quick` |
| [REGENERATION_REPORT](REGENERATION_REPORT.md) | 2026-01-26 | Re-generating older books with `regenerate_old_books.py` |
| [ITERATIVE_IMPROVEMENTS_v2.1.0](ITERATIVE_IMPROVEMENTS_v2.1.0.md) | 2026-01-26 | v2.1.0 preventive QA improvements |
| [SESSION_SUMMARY_ITERATIVE_IMPROVEMENTS](SESSION_SUMMARY_ITERATIVE_IMPROVEMENTS.md) | 2026-01-26 | Session summary of the same v2.1.0 work |
| [PROJECT_STATUS](PROJECT_STATUS.md) | 2026-01-26 | Project status snapshot |
| [IMPROVEMENTS_SUMMARY](IMPROVEMENTS_SUMMARY.md) | 2026-01-27 | v2.1.0 → v2.1.1 improvements summary |
| [CODE_REVIEW_V2](CODE_REVIEW_V2.md) | 2026-01-27 | Code review of v2.2.0 (parallel generator, themes) |
| [REFACTORING_SUMMARY](REFACTORING_SUMMARY.md) | 2026-01-27 | v2.2.1 refactoring based on CODE_REVIEW_V2 |

## Overlaps (not merged)

Measured line overlap is low (at most 17 %), so these overlap in topic and are not copies:
- **ITERATIVE_IMPROVEMENTS_v2.1.0** ↔ **SESSION_SUMMARY_ITERATIVE_IMPROVEMENTS**: the same v2.1.0 QA session. The first is the change log, the second the session narrative (17 % shared lines, the highest pair).
- **CODE_REVIEW_V2** → **REFACTORING_SUMMARY**: review findings and their implementation (v2.2.x).
- **TROUBLESHOOTING_SESSION_SUMMARY** ↔ **BUGFIXES** ↔ guides/TROUBLESHOOTING: the same January bugs (e.g. #001, low resolution) from the session, release and guide angles.
- **COMPREHENSIVE_REVIEW** (v2.0.1) and **CODE_REVIEW** (v2.1.0): successive reviews, same day.
- **PROJECT_STATUS**, **IMPROVEMENTS_SUMMARY**: status snapshots overlapping with CHANGELOG.md.
