# Decorator Design Pattern
# Example: File Operations Wrapper
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/decorator
# This example is not far from the original one shown above

from __future__ import annotations

import codecs


class Source:
    """
    An abstract data source for reading and writing
    """

    def write(self, data: str) -> Source:
        """
        Write data to the source
        :param data: The data to write
        :return: Itself (for chaining)
        """
        return self

    def read(self) -> str:
        """
        Read data from the source
        :return: The data read
        """
        return ""


class FileSource(Source):
    """
    A data source for a file to be read and written
    """

    def __init__(self, filename: str):
        """
        Create a new file source
        :param filename: The name of the file to read and write
        """
        self.filename = filename

    def write(self, data: str) -> Source:
        """
        Write data to the file
        :param data: The data to write to the file
        :return: Itself (for chaining)
        """
        with open(self.filename, "w") as f:
            f.write(data)
        return self

    def read(self) -> str:
        """
        Read data from the file
        :return: The data read from the file
        """
        with open(self.filename, "r") as f:
            return f.read()


class SourceDecorator(Source):
    """
    An abstract decorator for a data source
    """

    def __init__(self, source: Source):
        """
        Create a new data source decorator
        :param source: The data source to decorate
        """
        self.source = source

    def base(self) -> Source:
        """
        Get the base data source of the decorator
        :return: The base data source of the decorator
        """
        return self.source

    def write(self, data: str) -> Source:
        """
        Write data to the source
        :param data: The data to write
        :return: Itself (for chaining)
        """
        self.source.write(data)
        return self

    def read(self) -> str:
        """
        Read data from the source
        :return: The data read
        """
        return self.source.read()


class Rot13Decorator(SourceDecorator):
    """
    A decorator for using a data source with the rot13 algorithm
    """

    def write(self, data: str) -> Source:
        """
        Write data to the source, but encode it with rot13 first
        :param data: The data to write and encode
        :return: Itself (for chaining)
        """
        data = codecs.encode(data, "rot13")
        super().write(data)
        return self

    def read(self) -> str:
        """
        Read data from the source and decode it with rot13
        :return: The data read decoded with rot13
        """
        return codecs.decode(super().read(), "rot13")


class Base64Decorator(SourceDecorator):
    """
    A decorator for using a data source with the base64 algorithm
    """

    def write(self, data: str) -> Source:
        """
        Write data to the source, but encode it with base64 first
        :param data: The data to write and encode
        :return: Itself (for chaining)
        """
        data = codecs.encode(data.encode(), "base64").decode()
        super().write(data)
        return self

    def read(self) -> str:
        """
        Read data from the source and decode it with base64
        :return: The data read decoded with base64
        """
        return codecs.decode(super().read().encode(), "base64").decode()


if __name__ == "__main__":
    source = FileSource("test.txt")  # Create a new file source
    source = Base64Decorator(source)  # Will encode with base64 first
    source = Rot13Decorator(source)  # Then will encode with rot13

    source.write("Hello World!")
    print(source.read())  # Will print Hello World! but the file will in fact show VXJ5eWIgSmJleXEh
