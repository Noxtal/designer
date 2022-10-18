# Builder Design Pattern
# Example: Line Renderer Drawing API
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/builder

from __future__ import annotations

import math
from typing import Tuple


class Graphics:
    """
    A collection of lines to form a drawing
    """

    def __init__(self):
        self.lines = []


class GraphicsBuilder:
    """
    Allows building a graphics from a set of chained instructions
    """

    def __init__(self):
        self.graphics = Graphics()
        self.color = (255, 255, 255)

    def set_color(self, color: Tuple[int, int, int]) -> GraphicsBuilder:
        """
        Set the color of the next lines to be added
        :param color: The color to set
        """
        self.color = color
        return self

    def add_line(self, x1: float, y1: float, x2: float, y2: float) -> GraphicsBuilder:
        """
        Add a line to the graphics
        :param x1: First x coordinate
        :param y1: First y coordinate
        :param x2: Second x coordinate
        :param y2: Second y coordinate
        :return: The builder itself after adding the line
        """
        self.graphics.lines.append(((x1, y1), (x2, y2), self.color))
        return self

    def build(self) -> Graphics:
        """
        Build into a graphics object
        :return: The graphics object
        """
        return self.graphics


class GraphicsDirector:
    """
    Directs a builder into shortcuts of common shapes
    """

    def __init__(self, builder: GraphicsBuilder):
        self.builder = builder

    def rectangle(self, topleft: Tuple[float, float], width: float, height: float,
                  color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Draw a rectangle
        :param topleft: Top left corner of the rectangle
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        :param color: Color of the rectangle (defaults to white)
        """
        tmpcolor = self.builder.color
        self.builder.set_color(color)
        self.builder.add_line(topleft[0], topleft[1], topleft[0] + width, topleft[1])
        self.builder.add_line(topleft[0] + width, topleft[1], topleft[0] + width, topleft[1] + height)
        self.builder.add_line(topleft[0], topleft[1] + height, topleft[0] + width, topleft[1] + height)
        self.builder.add_line(topleft[0], topleft[1], topleft[0], topleft[1] + height)
        self.builder.set_color(tmpcolor)

    def polygon(self, n, center, apothem, color=(255, 255, 255)):
        """
        Draw a regular polygon
        :param n: Amount of sides
        :param center: Center of the polygon
        :param apothem: Apothem of the polygon
        :param color: Color of the polygon (defaults to white)
        """
        tmpcolor = self.builder.color
        self.builder.set_color(color)
        for i in range(n):
            self.builder.add_line(center[0] + apothem * math.cos(2 * math.pi * i / n),
                                  center[1] + apothem * math.sin(2 * math.pi * i / n),
                                  center[0] + apothem * math.cos(2 * math.pi * (i + 1) / n),
                                  center[1] + apothem * math.sin(2 * math.pi * (i + 1) / n))
        self.builder.set_color(tmpcolor)


if __name__ == '__main__':
    builder = GraphicsBuilder()
    director = GraphicsDirector(builder)
    director.polygon(5, (10, 10), 5)
    graphics = builder.build()
    print(graphics.lines)
