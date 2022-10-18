# Monad Design Pattern
# Example: Optional/Maybe Type
# Author: Noxtal
# Scaled down from my own https://github.com/Noxtal/opt4py
# Also see https://en.wikipedia.org/wiki/Monad_(functional_programming)#An_example:_Maybe

from __future__ import annotations


class Option:
    """
    A container class that handles seamlessly NoneType checks in a monadic way
    """

    def __init__(self, value=None):
        """
        Initialize a new Option object with a given value (defaults to None)
        :param value: Value stored at first inside the Option
        """
        self.value = value

    def is_none(self) -> bool:
        """
        Check if the Option's value is None
        :return: True if the Option is None
        """
        return self.value is None

    def is_some(self) -> bool:
        """
        Check if the Option contains something (opposite of is_none())
        :return: True if the Option is not None
        """
        return self.value is not None

    def unwrap(self):
        """
        Unwrap the Option object into only its value
        :return: The Option's value
        """
        return self.value

    def unwrap_or(self, default):
        """
        Unwrap the Option object into only its value. If it is None, return a default value
        :param default: Value used if the Option is_none()
        :return: The Option's value or default
        """
        if self.is_some():
            return self.value
        return default

    def map(self, f) -> Option:
        """
        Map a method to the Option's value if it is not None
        :param f: Method to map.
        :return: A new Option with the value mapped using method f
        """
        if self.is_some():
            return Option(f(self.value))
        return Option()

    def __repr__(self):
        return f"Option({self.value})"


if __name__ == '__main__':
    # Example usage
    print(Option(5).map(lambda x: x + 1))
    print(Option().map(lambda x: x + 1))
    print(Option(5).unwrap_or(10))
    print(Option().unwrap_or(10))
