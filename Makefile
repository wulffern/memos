
FILE= 2021-07-08_diodes

one:
	cd build; pandoc --csl=ieee-with-url.csl --citeproc --resource-path='../media' --bibliography=memo.bib  -s ../${FILE}/memo.md -o ${FILE}.pdf --template memo.latex
	cp build/${FILE}.pdf delivery/




aic2022:
	cd ${HOME}/pro/NTNU/aic2022; ./d2pan ${FILE}
	cd build; pandoc --csl=ieee-with-url.csl --citeproc --resource-path='${HOME}/pro/NTNU/aic2022/pandoc' --bibliography=memo.bib  -s ${HOME}/pro/NTNU/aic2022/pandoc/${FILE}.md -o aic2022_${FILE}.pdf --template memo.latex
	cp build/aic2022_${FILE}.pdf delivery/

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
