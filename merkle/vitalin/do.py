"""
copy paste of this ... not really that useful.

https://ethresear.ch/t/data-availability-proof-friendly-state-tree-transitions/1453/6
"""

import hashlib

def sha3(x):
    return hashlib.sha3_256(x).digest()


class DB(dict):
    def put(self, *args, **kwargs):
        self.__setitem__(*args, **kwargs)


def new_tree(db):
    h = b'\x00' * 32
    for i in range(256):
        newh = sha3(h + h)
        db.put(newh, h + h)
        h = newh
    return h


def key_to_path(k):
    o = 0
    for c in k:
        o = (o << 8) + c
    return o


def get(db, root, key):
    v = root
    path = key_to_path(key)
    for i in range(256):
        if (path >> 255) & 1:
            v = db.get(v)[32:]
        else:
            v = db.get(v)[:32]
        path <<= 1
    return v


def update(db, root, key, value):
    v = root
    path = path2 = key_to_path(key)
    sidenodes = []
    for i in range(256):
        if (path >> 255) & 1:
            sidenodes.append(db.get(v)[:32])
            v = db.get(v)[32:]
        else:
            sidenodes.append(db.get(v)[32:])
            v = db.get(v)[:32]
        path <<= 1
    v = value
    for i in range(256):
        if path2 & 1:
            newv = sha3(sidenodes[-1] + v)
            db.put(newv, sidenodes[-1] + v)
        else:
            newv = sha3(v + sidenodes[-1])
            db.put(newv, v + sidenodes[-1])
        path2 >>= 1
        v = newv
        sidenodes.pop()
    return v


def make_merkle_proof(db, root, key):
    v = root
    path = key_to_path(key)
    sidenodes = []
    for i in range(256):
        if (path >> 255) & 1:
            sidenodes.append(db.get(v)[:32])
            v = db.get(v)[32:]
        else:
            sidenodes.append(db.get(v)[32:])
            v = db.get(v)[:32]
        path <<= 1
    return sidenodes


def verify_proof(proof, root, key, value):
    path = key_to_path(key)
    v = value
    for i in range(256):
        if path & 1:
            newv = sha3(proof[-1 - i] + v)
        else:
            newv = sha3(v + proof[-1 - i])
        path >>= 1
        v = newv
    return root == v
