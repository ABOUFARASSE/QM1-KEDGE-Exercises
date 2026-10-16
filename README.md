# QM1 Practice Lab — KEDGE Business School

Bilingual Quantitative Methods 1 practice platform for EBP1.

## Published exercises (2026–2027)

The **seven revised worksheets** are the primary on-page exercises. They contain **22 exercises/cases**: 3 in Chapter 1, 3 in Chapter 2, 3 in Chapter 3, 4 in Chapter 4, 4 in Chapter 5, 3 in Chapter 6 and 2 integrated cases in Chapter 7.

A curated set of **12 additional exercises** from `exercise-data-export.json` appears below the revised worksheet: four in Chapter 1, two in Chapter 2, two in Chapter 3, one in Chapter 4, one in Chapter 5 and two in Chapter 6. Total: **34 on-page exercises/cases**.

- Full English/French switching.
- Exercise statements and detailed solutions displayed directly on the chapter page.
- The existing session-code mechanism is preserved; solution sections and downloadable solution links are hidden until unlocked.
- Four updated PDF resources per chapter (EN/FR × statements/solutions): **28 PDFs**, located in `downloads/`.
- The matching LaTeX source archive is available as `downloads/QM1_2026_LaTeX_sources.zip`.
- Charts for the discrete distribution, unequal-width histogram and Lorenz curve are rendered as inline SVG.
- The former on-page series remains in `content/` as a fallback, but is not the primary published version.

## Content files

- `revised-worksheets-2026.json`: bilingual revised worksheets, converted from the 2026–2027 LaTeX sources.
- `exercise-data-export.json`: supplementary exercise data, including bilingual detailed solutions.
- `app.js`: loads revised worksheets first, then curated supplementary exercises; falls back to the legacy chapter content if the revised data cannot load.
- `config.json`: chapter availability and SHA-256 session-code hashes (unchanged).
- `downloads/chapter-N-exercises-LANG.pdf` and `downloads/chapter-N-solutions-LANG.pdf`: printable resources.

## Maintenance

To change exercises, update the bilingual HTML fields in `revised-worksheets-2026.json` or the supplementary data and then bump the `VERSION` string in `app.js`. To rebuild PDFs, use the LaTeX sources from the archive and replace the corresponding PDF files.

This is a static GitHub Pages website. The existing code-based hiding mechanism is a teaching convenience, **not cryptographic protection**: public client-side files can be inspected by technically proficient visitors.

## GitHub Pages

Publish from the repository root on the `main` branch using **Settings → Pages → Deploy from a branch**.

© 2026 Badr ABOUFARASSE, PhD. — KEDGE Business School.

## Exercise-by-exercise solution layout (17 October 2026)

The session-code card is now displayed **before** the exercises. Each of the 34 exercise statements is followed immediately by its own detailed solution, which stays hidden until the session code is accepted. This pairing works in both languages, including the three subsections of integrated Case B. PDF downloads and the existing session-code hashes are unchanged.

## Révision pédagogique — octobre 2026

La version en ligne propose **38 exercices et cas bilingues**, classés en **applications fondamentales**, **préparation CC/partiel** et **approfondissement**. Chaque corrigé est placé directement après son énoncé et peut être masqué individuellement après déverrouillage. Les exercices de régression, séries temporelles et indices ont été complétés, avec de nouveaux tableaux et graphiques. **Les anciens PDF du dossier downloads/ ne contiennent pas tous les ajouts** ; utiliser « Imprimer la fiche à jour » pour exporter la version actuelle.

Voir [le rapport de révision](PEDAGOGICAL-REVISION-2026.md).
