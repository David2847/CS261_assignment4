# Name: David Jantz
# OSU Email: jantzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: BST / AVL Implementation
# Due Date: 11/18/2024
# Description: This is an implementation of an AVL tree with remove / add functionality.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a value to the AVL tree and rebalances the tree as necessary.
        """
        # add leaf node using the same recursive process as in BST
        curr_node = self._recursive_add(value, self._root)
        # work back up the tree, updating heights and checking balance factors as we go
        # while loop terminates when we step "above" the root node to a nonexistent parent
        while curr_node is not None:
            self._rebalance(curr_node)  # rebalance as necessary
            curr_node = curr_node.parent
        x = 1

    def _recursive_add(self, value: object, curr_node: AVLNode) -> AVLNode | None:
        """
        Recursively adds new AVLNode to the tree.
        This method is exactly the same as _recursive_add in BST class with four differences:
        1. BSTNodes are replaced with AVLNodes
        2. It returns a reference to the node that was added to give a starting point for rebalancing.
        3. It updates the parent reference for the inserted node.
        4. It disallows duplicate values to be added to the tree.
        """
        # base case #1: if tree is empty, make it the root and return
        if self._root is None:
            self._root = AVLNode(value)
            return self._root

        # Base case #2: figure out whether to go left or right, if at bottom create new leaf
        if value < curr_node.value:
            next_node = curr_node.left
            if next_node is None:
                curr_node.left = AVLNode(value)
                curr_node.left.parent = curr_node  # doubly linked reference chain
                return curr_node.left
        elif value > curr_node.value:
            next_node = curr_node.right
            if next_node is None:
                curr_node.right = AVLNode(value)
                curr_node.right.parent = curr_node
                return curr_node.right
        else:
            return None  # no duplicate values allowed... if equivalent value is discovered, do nothing

        # recursive case: drill deeper into the BST.
        return self._recursive_add(value, next_node)

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        # remove node using normal BST removal (replace with inorder successor)
        #if super().remove(value):
        pass
            # update heights
            # rebalance

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        TODO: Write your implementation
        """
        pass

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Determines the balance factor of a given AVLNode.
        """
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of desired node or -1 if the node doesn't exist.
        """
        if node is None:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation, centered on node
        """
        former_parent = node.parent  # Could be None
        former_right_child = node.right  # Can't be none since we are performing a left rotation
        former_RL_grandchild = node.right.left  # Could be None

        is_left_child = False
        is_right_child = False
        # check if node is parent's left child, right child, or if node is root
        if node == self._root:
            pass # avoid error of trying to access the child of None
        elif node == former_parent.left:
            is_left_child = True
        else:
            is_right_child = True

        # former right child gets node's parent as its parent
        former_right_child.parent = former_parent
        # former right child's new parent gets former right child as its right or left child or we make former right
        # child the new root
        if is_left_child:
            former_parent.left = former_right_child
        elif is_right_child:
            former_parent.right = former_right_child
        else:
            self._root = former_right_child

        # node gets its right child's left child as node's new right child even if it's None
        node.right = former_RL_grandchild
        if former_RL_grandchild is not None:
            # node's new right child gets node as its parent
            former_RL_grandchild.parent = node

        # node gets its former right child as its parent
        node.parent = former_right_child
        # right child gets node as its left child
        former_right_child.left = node

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation, centered on node
        """
        former_parent = node.parent  # Could be None
        former_left_child = node.left  # Can't be none since we are performing a left rotation
        former_LR_grandchild = node.left.right  # Could be None

        is_left_child = False
        is_right_child = False
        # check if node is parent's left child, right child, or if node is root
        if node == self._root:
            pass  # avoid error of trying to access the child of None
        elif node == former_parent.left:
            is_left_child = True
        else:
            is_right_child = True

        # former left child gets node's parent as its parent
        former_left_child.parent = former_parent
        # former left child's new parent gets former left child as its right or left child or we make former left
        # child the new root
        if is_left_child:
            former_parent.left = former_left_child
        elif is_right_child:
            former_parent.right = former_left_child
        else:
            self._root = former_left_child

        # node gets its former left child's right child as node's new left child even if it's None
        node.left = former_LR_grandchild
        if former_LR_grandchild is not None:
            # node's new right child gets node as its parent
            former_LR_grandchild.parent = node

        # node gets its former right child as its parent
        node.parent = former_left_child
        # right child gets node as its left child
        former_left_child.right = node

    def _update_height(self, node: AVLNode) -> None:
        """
        updates the height of a given node.
        """
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the tree by performing necessary rotations centered at given node
        """
        # if unbalanced left
        if self._balance_factor(node) < -1:
            # if left child is unbalanced right
            if self._balance_factor(node.left) > 0:
                # rotate left child to the left (handles L-R imbalance)
                self._rotate_left(node.left)
                self._update_height(node.left.left)
            # rotate N right (handles L-L imbalance)
            self._rotate_right(node)
        # if unbalanced right:
        elif self._balance_factor(node) > 1:
            # if right child is unbalanced left
            if self._balance_factor(node.right) < 0:
                # rotate right child to the right (handles R-L imbalance)
                self._rotate_right(node.right)
                self._update_height(node.right.right)
            # rotate N left (handles R-R imbalance)
            self._rotate_left(node)
        self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
