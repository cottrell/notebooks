all:
	cat Makefile

example.c: example.py
	cython --embed -o example.c example.py

example.o: example.c
	gcc -c example.c $(shell python3-config --includes --embed) -I/home/cottrell/anaconda3/envs/3.10.4/lib/python3.10/site-packages/pandas/_libs/src

build: example.o
	# reminders on flags:
	# * http://web.cs.ucla.edu/classes/fall14/cs143/project/cpp/gcc-intro.html
	# * https://renenyffenegger.ch/notes/development/languages/C-C-plus-plus/GCC/options/s/index
	# -O Generate optimized code on a Linux machine.
	# -Wall Have the compiler generate many warnings about syntactically correct but questionable looking code. It is good practice to always use this option with gcc and g++.
	#  -s Remove all symbol table and relocation information from the executable.
	gcc -O -s example.o -o example $(shell python3-config --cflags --embed) $(shell python3-config --embed --ldflags)

clean:
	rm -rf example example.o example.c

test2:
	# this one misses pandas
	./example

test:
	# this one runs
	PYTHONHOME=~/anaconda3/envs/3.10.4/ ./example


build_pyinstaller:
	pyinstaller example.py
