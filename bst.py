def bst_node(value, left, right):
    return [left, value, 1 + max(height(left), height(right)), right]

def value(node):
    return node[1]

def left(node):
    return node[0]

def right(node):
    return node[3]

def height(node):
    if node is None:
        return 0
    return node[2]

### ABSTRACTION CURTAIN ###

def left_tug(node):
    return bst_node(
        value(left(node)),
        left(left(node)),
        bst_node(value(node), right(left(node)), right(node)))

def right_tug(node):
    return bst_node(
        value(right(node)),
        bst_node(value(node), left(node), left(right(node))),
        right(right(node)))

def right_left_tug(node):
    return right_tug(bst_node(value(node), left(node), left_tug(right(node))))

def left_right_tug(node):
    return left_tug(bst_node(value(node), right_tug(left(node)), right(node)))

def balance_factor(node):
    return height(right(node)) - height(left(node))

def rebalance(node):
    if balance_factor(node) < -1:
        if balance_factor(left(node)) < 0:
            return left_tug(node)
        return left_right_tug(node)
    if balance_factor(node) > 1:
        if balance_factor(right(node)) < 0:
            return right_left_tug(node)
        return right_tug(node)
    return node

def bst_lookup(key, target_key, node):
    if node is None:
        return None
    if target_key < key(value(node)):
        return bst_lookup(key, target_key, left(node))
    if key(value(node)) < target_key:
        return bst_lookup(key, target_key, right(node))
    if target_key == key(value(node)):
        return value(node)

def bst_with(key, x, node):
    if node is None:
        return bst_node(x, None, None)
    if key(x) < key(value(node)):
        return rebalance(bst_node(value(node), bst_with(key, x, left(node)), right(node)))
    if key(value(node)) < key(x):
        return rebalance(bst_node(value(node), left(node), bst_with(key, x, right(node))))
    return node

def bst_min(node):
    if node is None:
        return None
    if left(node) is None:
        return value(node)
    return bst_min(left(node))

def bst_max(node):
    if node is None:
        return None
    if right(node) is None:
        return value(node)
    return bst_max(right(node))

def bst_without(key, some_key, node):
    if node is None:
        return node
    if some_key < key(value(node)):
        return rebalance(bst_node(value(node), bst_without(key, some_key, left(node)), right(node)))
    if key(value(node)) < some_key:
        return rebalance(bst_node(value(node), left(node), bst_without(key, some_key, right(node))))
    if some_key == key(value(node)):
        if left(node) is None:
            return right(node)
        if right(node) is None:
            return left(node)
        return rebalance(bst_node(bst_min(right(node)), left(node), bst_without(key, key(bst_min(right(node))), right(node))))

### ABSTRACTION CURTAIN ###

def pretty_print(node):
    def print_right_subtree(node, line):
        if node is None:
            return
        print_right_subtree(right(node), line + '   ')
        print(f"{line}┏━━{value(node)}")
        print_left_subtree(left(node), line + '┃  ')

    def print_left_subtree(node, line):
        if node is None:
            return
        print_right_subtree(right(node), line + '┃  ')
        print(f"{line}┗━━{value(node)}")
        print_left_subtree(left(node), line + '   ')
    print_right_subtree(right(node), '')
    print(value(node))
    print_left_subtree(left(node), '')

from functools import *
identity = lambda x : x
tree = reduce(lambda acc, x: bst_with(identity, x, acc), range(15), None)
pretty_print(tree)