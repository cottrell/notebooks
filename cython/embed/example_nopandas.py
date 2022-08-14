#cython: language_level=3
# https://github.com/astropy/astropy/pull/8106/commits/73fc5a4537af3fc79165b400434a8caaf55b1645
import numpy as np

def main():
    x = np.random.randn(10, 3)
    print(x)
    print('look at me')

if __name__ == '__main__':
    main()
