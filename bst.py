# Name: David Jantz
# OSU Email: jantzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4, BST/AVL Tree Implementation
# Due Date: 11/18/2024
# Description: Implementation of all standard BST functionality


import random
from queue_and_stack import Queue, Stack
from typing import Union


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def print_tree(self):
        """
        Prints the tree using the print_subtree function.

        This method is intended to assist in visualizing the structure of the
        tree. You are encouraged to add this method to the tests in the Basic
        Testing section of the starter code or your own tests as needed.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.get_root():
            self._print_subtree(self.get_root())
        else:
            print('(empty tree)')

    def _print_subtree(self, node, prefix: str = '', branch: str = ''):
        """
        Recursively prints the subtree rooted at this node.

        This is intended as a 'helper' method to assist in visualizing the
        structure of the tree.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        def add_junction(string):
            if len(string) < 2 or branch == '':
                return string
            junction = '|' if string[-2] == '|' else '`'
            return string[:-2] + junction + '-'

        if not node:
            print(add_junction(prefix) + branch + "None")
            return

        if len(prefix) > 2 * 16:
            print(add_junction(prefix) + branch + "(tree continues)")
            return

        if node.left or node.right:
            postfix = ' (root)' if branch == '' else ''
            print(add_junction(prefix) + branch + str(node.value) + postfix)
            self._print_subtree(node.right, prefix + '| ', 'R: ')
            self._print_subtree(node.left, prefix + '  ', 'L: ')
        else:
            print(add_junction(prefix) + branch + str(node.value) + ' (leaf)')

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds new value to proper location in BST.
        """
        self.recursive_add(value, self._root)

    def recursive_add(self, value: object, curr_node: BSTNode) -> None:
        """ Recursively adds new BSTNode to the tree."""
        # base case #1: if tree is empty, make it the root and return
        if self._root is None:
            self._root = BSTNode(value)
            return

        # Base case #2: figure out whether to go left or right, if at bottom create new leaf
        if value < curr_node.value:
            next_node = curr_node.left
            if next_node is None:
                curr_node.left = BSTNode(value)
                return
        else:
            next_node = curr_node.right
            if next_node is None:
                curr_node.right = BSTNode(value)
                return

        # recursive case: drill deeper into the BST.
        self.recursive_add(value, next_node)

    def get_node_and_parent(self, value: object) -> (BSTNode, BSTNode):
        """Finds and returns the node of a particular value (or None, if no such node exists)."""
        return self.recursive_get_node_and_parent(value, self._root)

    def recursive_get_node_and_parent(self, value: object, curr_node: Union[BSTNode, None]) -> (BSTNode, BSTNode):
        """
        Recursively traverses tree to find desired node
        @:returns tuple with two BSTNodes in the order parent, child
        """
        # base case #1: there's no node with this value -- return None (and None for parent too)
        #       This also covers the base case where the root is empty
        if curr_node is None:
            return None, None

        # base case #2: root is the desired node, return it with no parent
        if curr_node.value == value:
            return None, curr_node

        # base case #3: found desired node, return it
        if curr_node.left is not None and curr_node.left.value == value:
            return curr_node, curr_node.left
        if curr_node.right is not None and curr_node.right.value == value:
            return curr_node, curr_node.right

        if value < curr_node.value:
            # recursion to the left to the left
            return self.recursive_get_node_and_parent(value, curr_node.left)
        else:
            # recursion to the right subtree
            return self.recursive_get_node_and_parent(value, curr_node.right)

    def remove(self, value: object) -> bool:
        """
        Removes value from a tree, restructures the tree to preserve BST qualities
        """
        # traverse down the tree until finding the node to remove
        nodes = self.get_node_and_parent(value)
        parent = nodes[0]
        child = nodes[1]

        # edge case: child doesn't exist (is None). removal failed, return False
        if child is None:
            return False

        has_left_subtree = child.left is not None
        has_right_subtree = child.right is not None

        # handle the four cases -- it has zero, left, right, or both subtrees.
        if has_left_subtree and has_right_subtree:
            self._remove_two_subtrees(parent, child)
        elif has_left_subtree and not has_right_subtree:
            self._remove_one_subtree(parent, child)
        elif not has_left_subtree and has_right_subtree:
            self._remove_one_subtree(parent, child)
        else:
            self._remove_no_subtrees(parent, child)

        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has no subtrees (no left or right nodes)
        """
        # edge case -- removing the root node. Can't alter a parent reference, so we just
        #       have to empty the tree.
        if remove_parent is None:
            self.make_empty()
            return

        # check to see if remove node is left or right
        if remove_parent.left == remove_node:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes node that has one subtree, left or right
        """
        # edge case -- remove_node is root. Promote its left or right child to become the new root
        if remove_parent is None:
            if remove_node.left is not None:
                self._root = remove_node.left
                return
            else:
                self._root = remove_node.right
                return

        # check to see if remove node is left or right and act accordingly... four cases:
        #       remove left child of parent, promote left grandchild
        #       remove left child of parent, promote right grandchild
        #       remove right child of parent, promote left grandchild
        #       remove right child of parent, promote right grandchild
        if remove_parent.left == remove_node:
            if remove_node.left is not None:
                remove_parent.left = remove_node.left
            else:
                remove_parent.left = remove_node.right
        else:
            if remove_node.left is not None:
                remove_parent.right = remove_node.left
            else:
                remove_parent.right = remove_node.right

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node that has two subtrees, replacing it with its inorder successor to preserve BST attributes.
        """
        inorder_parent, inorder_successor = self.get_inorder_successor_and_parent(remove_node)

        # if the inorder successor is not the immediate right child of remove_node, we have to:
        #       make S's right child PS's left child
        #       make N's right child S's right child
        if inorder_parent != remove_node:
            inorder_parent.left = inorder_successor.right
            inorder_successor.right = remove_node.right

        # Regardless of which descendant the inorder successor is, we need to:
        #       make N's left child S's left child
        #       make S become PN's left or right child, or make S into self._root
        inorder_successor.left = remove_node.left
        if remove_parent is None:
            self._root = inorder_successor
        elif remove_parent.left == remove_node:
            remove_parent.left = inorder_successor
        else:
            remove_parent.right = inorder_successor

    def get_inorder_successor_and_parent(self, curr: BSTNode) -> (BSTNode, BSTNode):
        """Finds and returns the inorder successor and its parent of a given node."""
        # edge case -- curr's right child is inorder successor.
        if curr.right.left is None:
            return curr, curr.right

        # go right -- guaranteed to have at least one right descendant
        curr = curr.right

        # check to see if curr's leftmost grandchild is None, if it is we can return
        while curr.left.left is not None:
            curr = curr.left
        return curr, curr.left

    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        pass

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def is_empty(self) -> bool:
        """
        Returns True or False depending on if the tree is empty.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Empties the tree.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((3, 2, 1), 1),
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
