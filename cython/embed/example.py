import numpy as np
import csv

def main():
    x = np.random.randn(10000, 3)
    for i in range(x.shape[0]):
        print(x[i])
    print('look at me')

if __name__ == '__main__':
    main()
