# Factory Method Design Pattern
# Example: Cross-Platform Command-Line Interface
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/factory-method

from __future__ import annotations
from typing import List


# Products
class Terminal:
    """
    A general terminal command to be executed
    """
    def __init__(self, command: str, args: List[str]):
        self.command = command
        self.args = args

    def execute(self):
        """
        Execute the command
        """
        print("Would execute", self.command, ' '.join(self.args))


class Powershell(Terminal):
    """
    A Powershell command to be executed
    """
    def execute(self):
        """
        Execute the Powershell command
        """
        print(f"Executing Powershell \"{self.command}{' '.join(self.args)}\"")


class Bash(Terminal):
    """
    A bash command to be executed
    """
    def execute(self):
        """
        Execute the bash command
        """
        print(f"Executing bash -c \"{self.command} {' '.join(self.args)}\"")


# Creators
class TerminalFactory:
    """
    The Factory Method for creating a terminal command
    """
    def __init__(self, command):
        self.command = command
        self.args = []

    def arg(self, arg) -> TerminalFactory:
        """
        Add an argument to the command
        :param arg: The argument to add
        :return: The factory itself after adding the argument
        """
        self.args.append(arg)
        return self

    def args(self, args: List[str]) -> TerminalFactory:
        """
        Add a list of arguments to the command
        :param args: The list of arguments to add
        :return: The factory itself after adding the arguments
        """
        self.args += args
        return self

    def create(self) -> Terminal:
        """
        Finally create the terminal command
        :return: The corresponding terminal command
        """
        return Terminal(self.command, self.args)


class WindowsFactory(TerminalFactory):
    """
    The Factory Method for creating a Windows-compatible command
    """
    def create(self) -> Terminal:
        """
        Finally create the Powershell command
        :return: The corresponding Powershell command
        """
        return Powershell(self.command, self.args)


class LinuxFactory(TerminalFactory):
    """
    The Factory Method for creating a linux-compatible command
    """
    def create(self) -> Terminal:
        """
        Finally create the bash command
        :return: The corresponding bash command
        """
        return Bash(self.command, self.args)


# We do not do Mac here. We do not do Mac here. We do not do Mac here.

if __name__ == '__main__':
    import sys

    if sys.platform == 'win32':
        factory = WindowsFactory('dir')
    else:
        factory = LinuxFactory('ls').arg('-l').arg('-a')
    factory.create().execute()
