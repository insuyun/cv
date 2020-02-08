all: gen
	./bin/latexrun -Wall cv-gen.tex -o cv.pdf

gen: cv.tex
	bin/make.py cv-gen.tex

clean:
	rm -rf *.out *.pdf *.aux

.PHONY: all gen clean
