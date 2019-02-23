import bc

@bc.cachecalc()
def a():
    pass
@bc.cachecalc()
def b():
    a()
@bc.cachecalc()
def c():
    b()
@bc.cachecalc()
def d():
    c()
