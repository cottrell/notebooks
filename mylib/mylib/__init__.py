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

def attributedict_from_locals(text_or_list_of_text):
    return dict_from_locals(text_or_list_of_text, attributedict=True, depth=1)

def dict_from_locals(text_or_list_of_text, attributedict=False, depth=-1):
    if attributedict:
        from attributedict.collections import AttributeDict
        d = AttributeDict()
    else:
        d = dict()
    frame = sys._getframe(depth)
    _locals = frame.f_back.f_locals
    if isinstance(text_or_list_of_text, str):
        text_or_list_of_text = text_or_list_of_text.split(',')
    for k in text_or_list_of_text:
        k = k.strip()
        d[k] = _locals[k]
    return d

def _test_dict_from_locals():
    a = 1
    b = 2
    r = dict_from_locals('a,b')
    assert r == {'a': 1, 'b': 2}

def _test_attributedict_from_locals():
    a = 1
    b = 2
    r = attributedict_from_locals('a,b')
    assert r == {'a': 1, 'b': 2}
