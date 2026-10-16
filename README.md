# QM1 Practice Lab — KEDGE Business School

Bilingual Quantitative Methods 1 practice platform for EBP1, maintained by Badr ABOUFARASSE, PhD.

## Published materials (2026–2027)

**38 exercises and integrated cases** in seven bilingual chapters: 7 / 5 / 6 / 6 / 6 / 6 / 2. These comprise 22 original revised exercises/cases, 12 curated supplementary exercises and 4 new comprehensive exercises. Each item has a paired solution in French and English, a pedagogical level and estimated completion time.

## Complete downloadable PDFs

**28 updated PDF files** are generated from the same HTML/JSON sources as the live Practice Lab. For each chapter N:

- downloads/chapter-N-exercises-fr.pdf — all French statements.
- downloads/chapter-N-solutions-fr.pdf — all French statements followed by fully worked solutions.
- downloads/chapter-N-exercises-en.pdf — all English statements.
- downloads/chapter-N-solutions-en.pdf — all English statements followed by fully worked solutions.

All **38 exercises/cases** are included, with supplementary cases, tables, charts, formula derivations and the new October 2026 material.

The instructor archive is downloads/QM1_2026-2027_28_PDF_FR_EN.zip (all 28 PDFs). The machine-readable audit file is downloads/QM1_PDF_manifest_2026.json (pages, exercise counts, math/chart counts, sizes and SHA-256).

The older downloads/QM1_2026_LaTeX_sources.zip is a **historical archive**; the authoritative current PDF sources are the website's JSON files.

## Reproducible PDF generation and checks

The GitHub Actions workflow .github/workflows/qm1-complete-pdfs.yml runs whenever the exercise sources, rendering code or generator change. It installs Chromium, Playwright, MathJax SVG and PyMuPDF and invokes scripts/build_complete_pdfs.py. This generator uses the **same** renderPairedWorksheet and renderQM1Charts functions as the website. It checks for missing/duplicated exercises, absent or very short solutions, unresolved charts, MathJax errors, empty PDFs and unsearchable documents.

All 28 PDFs are published to main only after the entire build passes. To rebuild locally, install the required dependencies and run: python scripts/build_complete_pdfs.py.

## Main source files

- revised-worksheets-2026.json — core bilingual worksheets.
- exercise-data-export.json — supplementary exercises and solutions.
- pedagogy-upgrade-2026.json — new exercises and enhanced worked solutions.
- app.js — interactive rendering, session-code interface and graphs.
- config.json — existing access settings and code hashes.
- scripts/build_complete_pdfs.py — reproducible PDF generation and validation.

## Important access note

The static GitHub Pages site hides solution links until the session code is entered. **This is an interface restriction, not server-side security**: static PDF files can still be accessed directly by URL. True authentication requires a protected backend or file service.

## GitHub Pages

The site is published from the repository root on main.

© 2026 Badr ABOUFARASSE, PhD. All rights reserved.
