
pscript =  python3 2022-09-12_Range_model/model.py

plotchan:
	cd ../; ${pscript} response --distance 10 --rays 1 --no-show
	cd ../; ${pscript} response --distance 10 --rays 2  --no-show
	cd ../; ${pscript} response --distance 10 --rays 100 --no-show


plotdist:
	cd ../; ${pscript} distance --dstart 1 --dstop 20 --rays 10 --no-show
	cd ../; ${pscript} distance --dstart 1 --dstop 20 --rays 100 --no-show
	cd ../; ${pscript} distance --dstart 1 --dstop 20 --rays 1000 --no-show


doc:
	cd ../; make one FILE=2022-09-12_Range_model
