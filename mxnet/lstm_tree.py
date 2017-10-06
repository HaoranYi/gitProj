import mxnet as mx
from mxnet.gluon import Block, nn
from mxnet.gluon.parameter import Parameter

class Tree(object):
    def __init__(self, idx):
        self.children = []
        self.idx = idx

    def __repr__(self):
        if self.children:
            return '{0}: {1}'.format(self.idx, str(self.children))
        else:
            return (self.idx)

tree = Tree(0)
tree.children.append(Tree(1))
tree.children.append(Tree(2))
tree.children.append(Tree(3))
tree.children[1].children.append(Tree(4))

