# https://github.com/hyperpy/merkle-tree-stream

import hashlib

from merkle_tree_stream import MerkleTreeGenerator


def _leaf(node, roots=None):
    return hashlib.sha256(node.data).digest()


def _parent(first, second):
    sha256 = hashlib.sha256()
    sha256.update(first.data)
    sha256.update(second.data)
    return sha256.digest()


merkle = MerkleTreeGenerator(leaf=_leaf, parent=_parent)

merkle.write(b"a")
merkle.write(b"b")

print(merkle._nodes)
