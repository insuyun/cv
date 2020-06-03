all: gen
	./bin/latexrun -Wall cv-gen.tex -o cv.pdf

gen: download cv.tex
	bin/make.py cv-gen.tex

download:
	./download.sh

clean:
	rm -rf *.out *.pdf *.aux

.PHONY: all gen clean download
