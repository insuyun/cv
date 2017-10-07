all:
	./bin/latexrun -Wall cv.tex 

clean:
	rm -rf *.out *.pdf *.aux
