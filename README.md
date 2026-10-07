# QM1 Practice Lab — KEDGE Business School

Interactive GitHub Pages platform for progressive Quantitative Methods 1 exercises.

## Current content

- Six chapters covering the complete QM1 course
- Ten progressive exercises in Chapter 1 and seven in Chapters 2–6
- Complete English/French switching on every chapter page
- Method prompts, figures when relevant, and progress saved in the browser
- Twenty-four printable PDFs: student series and detailed solutions in both languages
- On-page and PDF solutions unlocked by session code or by the live `solutionsOpen` switch

## Initial access code

`KEDGE-CH1`

The codes are stored as SHA-256 hashes in `config.json` and can be changed directly in the repository.

## Live access control

- `"solutionsOpen": true` opens solutions for all students.
- `"solutionsOpen": false` requires the session code.
- Student pages check `config.json` every 15 seconds.

This is classroom access control on a static site, not examination-grade security. A student with advanced web knowledge may inspect downloaded page resources.

## Regenerating the PDFs

Run `export_exercise_data.js`, then `generate_exercise_pdfs.py`. The generated files are written to `downloads/` with the names used by the chapter pages.

## GitHub Pages

Publish from the repository root on the `main` branch via **Settings → Pages → Deploy from a branch**.

© 2026 Badr ABOUFARASSE, PhD. — KEDGE Business School
