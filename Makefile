
FILE= 2021-07-08_diodes

one:
	cd build; pandoc --csl=ieee-with-url.csl --citeproc  --bibliography=memo.bib  -s ../${FILE}/memo.md -o ${FILE}.pdf --template memo.latex


clean:
	-rm build/*.bbl
	-rm build/*.aux
	-rm build/*.log
	-rm build/*.blg
	-rm build/*.dvi
	-rm build/*.fff
	-rm build/*.lof
	-rm build/*.lot
	-rm build/*.ttt
	-rm build/*.xml
	-rm build/*.pdf
	-rm build/*.tex
	-rm build/*.bcf
