all:
	cat Makefile

build:
	cython --embed -o example.c example.py
	gcc -Os -I ~/anaconda3/envs/3.10.4/include/python3.10 example.c -o example

clean:
	rm -rf example example.c

