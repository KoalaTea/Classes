filename=main.tex
output_folder=output

pdf:
	pdflatex -output-directory ${output_folder} ${filename}
	cp ref.bib output/
	cd output && bibtex main.aux
	pdflatex -output-directory ${output_folder} ${filename}
	pdflatex -output-directory ${output_folder} ${filename}

clean:
	rm -f output/*.{ps,pdf,log,aux,out,dvi,bbl,blg,bib,xml}
