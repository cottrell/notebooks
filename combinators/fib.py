import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
        print('took {}'.format(self.interval))

def fib(x):
    if x==0:
        return 0
    elif x==1:
        return 1
    else:
        return fib(x-1) + fib(x-2)

Y = lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))

# this formulation still has exponential complexity
fib_functional = lambda f: lambda n: 0 if n == 0 else (1 if n == 1 else f(n-1) + f(n-2))
fib2 = Y(fib_functional)

def Ymem(F, cache=None):
    if cache is None:
        cache = dict()
    def inner(arg):
        if arg in cache:
            return cache[arg]
        answer = F(lambda n: Ymem(F, cache)(n))(arg)
        cache[arg] = answer
        return answer
    return inner

fib3 = Ymem(fib_functional)

n = 30

# with Timer():
#     print(fib(n))
# with Timer():
#     print(fib2(n))
# with Timer():
#     print(fib3(n))

def gettimings(n=n):
    import pandas as pd
    d = list()
    timer = Timer()
    for i in range(0, n, 2):
        temp = [i]
        with timer:
            fib(i)
        temp.append(timer.interval)
        with timer:
            fib2(i)
        temp.append(timer.interval)
        with timer:
            fib3(i)
        temp.append(timer.interval)
        d.append(temp)
    d = pd.DataFrame(d)
    d.columns = ['n', 'fib', 'fib2', 'fib3']
    d = d.set_index('n')
    return d

def doplot():
    from pylab import clf, show, figure, gca
    figure(1)
    clf()
    df = gettimings()
    df.plot(ax=gca(), logy=True, logx=True, style='o')
    show()


