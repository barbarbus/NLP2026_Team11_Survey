# ACL survey report

- `main.tex`: editable English report.
- `main.pdf`: compiled review copy.
- `references.bib`: working bibliography keyed by the 124-paper catalogue IDs.
- `acl.sty` and `acl_natbib.bst`: ACL template files used for compilation.

The report synthesizes the literature review; it does not report a new experiment. Its quantitative claims should be checked against `../Reading_Notes/Numerical_Evidence_Ledger.md` before submission. The bibliography is a working citation library: only cited entries were checked by BibTeX in this build, and published metadata should be verified against the final version selected for every paper.

Build locally with `pdflatex main`, `bibtex main`, then `pdflatex main` twice. MiKTeX may need to install packages on first run.
