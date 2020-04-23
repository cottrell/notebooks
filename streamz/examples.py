from streamz import Stream

def increment(x):
    return x + 1

def example1():
    source = Stream()
    source.map(increment).sink(print)
    source.emit(1)
    source.emit(10)
    source.emit(100)

def add(x, y):
    return x + y

def example2():
    source = Stream()
    source.accumulate(add).sink(print)
    source.emit(1)
    source.emit(2)
    source.emit(3)
