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

The instructor archive is downloads/QM1_2026-2027_28_PDF_FR_EN.zip (all 28 PDFs). The machine-readable audit file is downloads/QM1_PDF_manifest_2026.json (pages, exercise counts, vector-chart counts, source paths, sizes and SHA-256).

The older downloads/QM1_2026_LaTeX_sources.zip is a **historical archive**; the authoritative current PDF sources are the website's JSON files.

## Academic LaTeX edition (October 2026)

The **28 downloadable PDFs** (7 chapters × 2 languages × exercises/solutions) are now compiled with **XeLaTeX** using a consistent black-and-white academic template: Latin Modern Roman 11 pt, A4, proper mathematical typesetting, booktabs tables, consistent heading hierarchy, running headers/footers and page numbering. Graphs are embedded as vector PDFs, not screenshots.

- `downloads/QM1_2026-2027_28_PDF_FR_EN.zip`: complete academic PDF collection.
- `downloads/QM1_2026-2027_LaTeX_sources_academic.zip`: **28 editable .tex files and their vector figure assets**, ready for XeLaTeX/Overleaf.
- `downloads/QM1_PDF_manifest_2026.json`: per-document page count, source file, figure count and SHA-256.

The PDF source is derived **without rewriting the exercise content** from the same `renderPairedWorksheet`/ `renderQM1Charts` functions as the website. The source HTML is translated into real LaTeX by Pandoc; equations and tables are typeset by XeLaTeX. The on-page exercises and session-code workflow remain unchanged.

The workflow `.github/workflows/qm1-academic-latex.yml` rebuilds all 28 documents, verifies the complete 38-exercise bilingual curriculum, checks missing glyphs and overfull content, audits core numerical examples, and publishes PDFs and sources **only after all checks pass**. The former browser-to-PDF generator is retained as a manual legacy workflow.

## Reproducible PDF generation and checks

The GitHub Actions workflow .github/workflows/qm1-academic-latex.yml runs whenever the exercise sources, rendering code or LaTeX generator change. It installs Chromium, Playwright, Pandoc, XeLaTeX, CairoSVG and PyMuPDF and invokes scripts/build_academic_latex.py. This generator uses the **same** renderPairedWorksheet and renderQM1Charts functions as the website. It checks for missing/duplicated exercises, absent or very short solutions, unresolved charts, XeLaTeX compilation failures, missing glyphs, overfull text, empty PDFs and unsearchable documents.

All 28 PDFs are published to main only after the entire build passes. To rebuild locally, install the required dependencies and run: python scripts/build_academic_latex.py.

## Main source files

- revised-worksheets-2026.json — core bilingual worksheets.
- exercise-data-export.json — supplementary exercises and solutions.
- pedagogy-upgrade-2026.json — new exercises and enhanced worked solutions.
- app.js — interactive rendering, session-code interface and graphs.
- config.json — existing access settings and code hashes.
- scripts/build_academic_latex.py — reproducible academic XeLaTeX source and PDF generation.
- scripts/build_complete_pdfs.py — original browser-based generator (manual fallback).

## Important access note

The static GitHub Pages site hides solution links until the session code is entered. **This is an interface restriction, not server-side security**: static PDF files can still be accessed directly by URL. True authentication requires a protected backend or file service.

## GitHub Pages

The site is published from the repository root on main.

© 2026 Badr ABOUFARASSE, PhD. All rights reserved.
