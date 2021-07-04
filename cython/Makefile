all:
	cat Makefile


build:
	python setup.py build_ext --inplace

test:
	python -c "import hello; hello.say_hello_to('HUMAN')"

clean:
	rm -rf build *.c *.so
