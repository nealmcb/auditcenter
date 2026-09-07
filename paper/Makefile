## Build the EVT/WOTE submission PDF from sections/*.md.
##
## Usage: make            (or: make pdf)
##        make clean

.PHONY: pdf clean paper-md

pdf: latex/corla_10.pdf

latex/corla_10.pdf: latex/corla_10.tex latex/references.bib latex/usenix.sty sections/*.md
	cd latex && python3 md2latex.py ../sections/*.md > body.tex
	cd latex && tectonic corla_10.tex

clean:
	cd latex && rm -f body.tex corla_10.pdf corla_10.bbl corla_10.blg

## Regenerate the repo-root paper.md companion (a plain concatenation of
## sections/*.md, in order -- see the repo root's own paper.md).
paper-md:
	cat sections/*.md > ../paper.md
