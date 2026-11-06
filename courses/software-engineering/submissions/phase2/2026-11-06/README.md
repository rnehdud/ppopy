# Ppopy — Phase 2 LaTeX submissions

These editable sources are based on the latest Revised A and B PDFs, with **Ppopy** in the title. Team names and role assignments have been updated to the current allocation: Doyeong Koo (app/backend, KB and integration), Takgeon Kang (agent) and Geonil Won (smart mirror). The proposal, requirements and specifications are otherwise unchanged. Line breaks, table placement and pagination can differ from the PDF originals.

| Main file | Contents |
| --- | --- |
| [Ppopy_Submission_A.tex](Ppopy_Submission_A.tex) | Proposal and requirements, R1–R10 and Q1–Q3 |
| [Ppopy_Submission_B.tex](Ppopy_Submission_B.tex) | A plus the development environment, budget, specifications and planned verification |

Each `.tex` file contains its complete document. The included `IEEEtran.cls` supplies the IEEE conference class and retains its original license notice. Other packages are standard TeX packages, including `listings`, `tabularx`, `tikz`, `amsmath` and `hyperref`.

## Build

Run in this directory with [Tectonic](https://tectonic-typesetting.github.io/):

```sh
tectonic Ppopy_Submission_A.tex
tectonic Ppopy_Submission_B.tex
```

In Overleaf, upload both `.tex` files and `IEEEtran.cls`, then choose the desired submission as the main document. Alternatively, use a full TeX Live installation and run `pdflatex` twice on each main file.

## Verification

On 2026-11-06, both files compiled with Tectonic without errors, undefined references or overfull boxes. The resulting US Letter PDFs have 2 pages (A) and 8 pages (B). All pages were rendered and inspected; the requirements and 15 pseudocode blocks were checked against the Revised PDFs. The author names and member responsibilities were also checked after the team update.

Compilation checks the document source. The integration and acceptance checks described in the submissions remain planned work.
