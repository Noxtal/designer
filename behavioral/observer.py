# Observer Design Pattern
# Example: Drag and Drop UI
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/observer
# Note: Handling *genuine* mouse events was ommitted for simplicity

from __future__ import annotations
import enum


class MouseEvent(enum.Enum):
    """
    Every handled mouse events
    """
    MOUSE_DOWN = 1
    MOUSE_UP = 2
    MOUSE_MOVE = 3


class MouseEventManager:
    """
    Manager class for updating all subscribed MouseEventListeners based on given mouse events
    """

    def __init__(self):
        self.listeners = []

    def subscribe(self, subscriber: MouseEventListener) -> MouseEventManager:
        """
        Subscribe a new MouseEventListener to later mouse events
        :param subscriber: The MouseEventListener to subscribe
        :return: Itself (for chaining)
        """
        self.listeners.append(subscriber)
        return self

    def unsubscribe(self, subscriber: MouseEventListener):
        """
        Unsubscribe a MouseEventListener from later mouse events
        :param subscriber: The MouseEventListener to unsubscribe
        :return: Itself (for chaining)
        """
        self.listeners.remove(subscriber)
        return self

    def notify(self, event: MouseEvent, x: int, y: int):
        """
        Notify all subscribed MouseEventListeners about a new mouse event to let them handle it properly
        :param event: The mouse event that occurred
        :param x: The x coordinate of the mouse at the time of the event (px)
        :param y: The y coordinate of the mouse at the time of the event (px)
        """

        # (This part would be triggered by true mouse events)
        for subscriber in self.listeners:
            subscriber.notify(event, x, y)


class MouseEventListener:
    """
    Interface for a mouse event listener to be subscribed to a MouseEventManager
    """

    def notify(self, event: MouseEvent, x: int, y: int):
        """
        Notify the listener about a new mouse event
        :param event: The mouse event that occurred
        :param x: The x coordinate of the mouse at the time of the event (px)
        :param y: The y coordinate of the mouse at the time of the event (px)
        """
        pass


class Draggable(MouseEventListener):
    """
    A draggable rectangular object
    """

    def __init__(self, x, y, width, height):
        """
        Create a new draggable object
        :param x: The x center coordinate of the object (px)
        :param y: The y center coordinate of the object (px)
        :param width: The width of the object (px)
        :param height: The height of the object (px)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dragging = False

    def notify(self, event: MouseEvent, x, y):
        """
        Update the draggable object based on a new mouse event
        :param event: The mouse event that occurred
        :param x: The x coordinate of the mouse at the time of the event (px)
        :param y: The y coordinate of the mouse at the time of the event (px)
        """
        if event == MouseEvent.MOUSE_MOVE:
            if self.dragging:
                self.x = x
                self.y = y
                print("Dragging to", x, y)
        elif event == MouseEvent.MOUSE_DOWN:
            if abs(x - self.x) <= self.width / 2 and abs(y - self.y) <= self.height / 2:
                self.dragging = True
                print("Dragging started")
        elif event == MouseEvent.MOUSE_UP:
            if self.dragging:
                self.dragging = False
                print("Dragging stopped")

    def __repr__(self):
        # For debugging purposes
        return "Draggable(x: {}, y: {}, width: {}, height: {})".format(self.x, self.y, self.width, self.height)


if __name__ == "__main__":
    manager = MouseEventManager()

    draggable1 = Draggable(10, 10, 30, 30)
    manager.subscribe(draggable1)

    draggable2 = Draggable(120, 120, 10, 10)
    manager.subscribe(draggable2)

    print("Initial state:", manager.listeners)  # For debugging purposes ONLY
    print("Moving the mouse around, nothing should happen")
    manager.notify(MouseEvent.MOUSE_MOVE, 10, 10)
    manager.notify(MouseEvent.MOUSE_MOVE, 120, 120)
    print(manager.listeners)  # For debugging purposes ONLY
    print("Drag the first draggable from (10, 10) to (100, 100)")
    manager.notify(MouseEvent.MOUSE_DOWN, 15, 5)
    manager.notify(MouseEvent.MOUSE_MOVE, 100, 100)
    manager.notify(MouseEvent.MOUSE_UP, 100, 100)
    print(manager.listeners)  # For debugging purposes ONLY
    print("Drag the second draggable from (120, 120) to (40, 40)")
    manager.notify(MouseEvent.MOUSE_MOVE, 125, 115)
    manager.notify(MouseEvent.MOUSE_DOWN, 125, 115)
    manager.notify(MouseEvent.MOUSE_MOVE, 40, 40)
    manager.notify(MouseEvent.MOUSE_UP, 100, 100)
    print(manager.listeners)  # For debugging purposes ONLY
