# Iterator Design Pattern
# Example: Iterative Tree Traversal
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/iterator
#            https://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion/

from __future__ import annotations
from typing import Any


class Tree:
    """
    A tree node with a value and two possible children
    """
    def __init__(self, value: Any, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def iterator(self) -> IIterator:
        """
        Get a corresponding iterator to the tree
        :return: An iterator for the tree
        """
        return TreeIterator(self)


class IIterator:
    """
    Interface for an Iterator object
    """

    def __init__(self):
        self.current = 0

    def next(self) -> Any:
        """
        Abstract method for getting the next element
        """
        pass

    def is_done(self) -> bool:
        """
        Abstract method for telling if the iterator is done
        """
        pass


class TreeIterator(IIterator):
    """
    A tree traversal iterator
    """

    def __init__(self, tree: Tree):
        super().__init__()
        self.current = tree
        self.stack = []

    def next(self) -> Any:
        """
        Get the next element in the tree
        :return: The next element in the tree
        """
        if not self.is_done():
            while self.current is not None:
                self.stack.append(self.current)
                self.current = self.current.left

            if len(self.stack) != 0:
                popped = self.stack.pop()
                self.current = popped.right
                return popped.value
        return None

    def is_done(self) -> bool:
        """
        Tell if the iterator is done
        :return: True if the iterator is done, False otherwise
        """
        return self.current is None and len(self.stack) == 0


if __name__ == "__main__":
    tree = Tree(1, Tree(2, Tree(4), Tree(5, Tree(10))), Tree(3, Tree(6), Tree(7)))
    iterator = tree.iterator()
    while not iterator.is_done():
        print(iterator.next())
