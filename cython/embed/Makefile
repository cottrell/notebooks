all:
	cat Makefile

build:
	cython --embed -o example.c example.py
	gcc -Os -I /home/cottrell/anaconda3/envs/38/include/python3.8 example.c -lpython3.8 -o example

clean:
	rm -rf example example.c

