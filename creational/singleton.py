# Singleton Design Pattern
# Example: Simple Logging System
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/singleton

from datetime import datetime


class Logger:
    """
    A singleton logger that writes to a file
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Gets the current singleton instance of the Logger class
        :return: The current singleton instance of the Logger class
        """
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self

        self.file = "log.txt"
        with open(self.file, "w") as f:
            f.write("Hello World!\n")

    def log(self, message):
        """
        Logs a message at a certain time to the log file
        :param message: The message to log
        """
        with open(self.file, "a") as f:
            f.write(f"[{datetime.now().ctime()}] {message}\n")


if __name__ == "__main__":
    logger = Logger.get_instance()
    logger.log("This is a log message")

    logger2 = Logger.get_instance()
    logger2.log("This is another log message")

    # This will raise an exception!
    logger3 = Logger()
