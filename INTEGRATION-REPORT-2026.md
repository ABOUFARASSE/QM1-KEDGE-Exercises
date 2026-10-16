# QM1 Practice Lab — integration report
**Date:** 17 October 2026  
**Scope:** 2026–2027 revised bilingual worksheets and curated supplementary practice.

## What changed

1. Added `revised-worksheets-2026.json`: all seven revised worksheets, with French/English statements and detailed solutions converted from the supplied LaTeX sources. Preserved the original mathematical notation, tables and structure; three source plots are available as responsive inline SVG in each language.
2. Replaced the primary displayed chapter content via `app.js`, retaining the legacy `content/` scripts as a fallback. This prevents duplicate exercises and removes the old *médiale* exercise from the displayed Chapter 3 sequence.
3. Selected 12 distinct supplementary exercises from `exercise-data-export.json` (4/2/2/1/1/2 for Chapters 1–6). The other source exercises remain available in the JSON but are not repeated on-page.
4. Replaced all 28 existing `downloads/chapter-*-*.pdf` files with the revised printable statements and detailed solutions in French and English.
5. Added `downloads/QM1_2026_LaTeX_sources.zip` for reproducibility.
6. Added responsive worksheet/figure/table styles, updated cache-busting versions across eight HTML pages, and added MathJax macros for the course's covariance/variance notation.
7. Corrected the arithmetic product `1.244376` / `1,244376` to `1.244208` / `1,244208` in the supplementary Chapter 2 growth example; the rounded equivalent annual growth rate remains 5.61%.
8. Updated `README.md` and `EXERCISE-COVERAGE.md` to reflect the actual published material.

## Coverage

| Chapter | Revised | Supplements | On-page total |
|---|---:|---:|---:|
| 1 | 3 | 4 | 7 |
| 2 | 3 | 2 | 5 |
| 3 | 3 | 2 | 5 |
| 4 | 4 | 1 | 5 |
| 5 | 4 | 1 | 5 |
| 6 | 3 | 2 | 5 |
| 7 | 2 | 0 | 2 |
| **Total** | **22** | **12** | **34** |

## Checks completed before deployment

- Valid JSON and full bilingual coverage of all 22 revised statements.
- Exactly 28 expected PDF paths present in the staged Git tree.
- All 28 PDFs are valid and text-extractable; representative pages rendered and visually inspected.
- Chapter 3 revised content contains no *médiale*.
- The patched `app.js` passes JavaScript syntax validation.
- Existing `config.json` and the chapter code hashes are unchanged.
- Supplementary Chapter 2 arithmetic correction verified in the staged JSON.

## Limitations and follow-up

The session-code workflow hides solutions in the user interface, but a public static website cannot make browser-delivered solution data secret. A server-side access check would be required for strict confidentiality. Browser-level checks after GitHub Pages deployment are still recommended, especially on mobile.

## Follow-up correction — 17 October 2026: solution positioning

After reviewing user feedback, fixed the page structure that previously displayed all exercise statements first and all solutions afterwards. The new renderer matches each revised exercise to its solution by exercise number or integrated case letter and places the protected solution immediately beneath its statement. The 12 supplementary exercises are paired in their existing order. Moved the session-code card above the exercise list. No exercise text, numerical result, session code or PDF was modified in this layout-only correction. Static pairing check: 34/34 exercises have matching FR and EN solution content. Browser-level verification remains recommended.
