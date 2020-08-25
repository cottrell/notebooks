import pandas as pd
import time
import concurrent.futures as futures

executor = futures.ProcessPoolExecutor(max_workers=5)

T = time.time()

def f(i):
    return i, time.time() - T

fut = list()
for i in range(10):
    print(f'launching {i}')
    time.sleep(0.1)
    fut.append(executor.submit(f, i))

res = [x.result() for x in fut]
df = pd.Series(dict(res))
print(df)
