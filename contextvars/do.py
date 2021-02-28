import contextvars

var = contextvars.ContextVar('a')
var.set(123)

ctx = contextvars.copy_context()
ctx2 = contextvars.copy_context()

def g():
    var.set(111)

def f():
    print('f', var.get())
    g()
    print('f', var.get())

def h():
    print('h', var.get())


ctx.run(f)
ctx.run(h)
ctx2.run(h)
ctx.run(h)
