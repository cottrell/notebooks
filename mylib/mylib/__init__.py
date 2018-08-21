import sys

try:
    _STUFF
except NameError as e:
    _STUFF = list()

def clear():
    global _STUFF
    _STUFF = list()

def bok(name=None, depth=-1):
    frame = sys._getframe(depth)
    _locals = frame.f_back.f_locals
    name = (name, frame.f_code.co_filename)
    _STUFF.append((name, _locals))

def wok():
    name, _locals = _STUFF.pop()
    print("wak vars from {}".format(name))
    sys._getframe(-1).f_back.f_locals.update(_locals)

