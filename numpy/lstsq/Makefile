all: numpy scipy_gelsy scipy_gelsd

numpy:
	mprof run -o numpy.dat ./lstsq.py numpy
	mprof plot -o numpy.png numpy.dat

scipy_gelsy:
	mprof run -o scipy_gelsy.dat ./lstsq.py scipy_gelsy
	mprof plot -o scipy_gelsy.png scipy_gelsy.dat

scipy_gelsd:
	mprof run -o scipy.gelsd.dat ./lstsq.py scipy_gelsd
	mprof plot -o scipy_gelsd.png scipy.gelsd.day

clean:
	rm mprofile_*.dat
