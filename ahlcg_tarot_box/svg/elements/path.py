from dataclasses import dataclass
from functools import reduce
from typing import Callable

from .core import Element
from ..attributes import Attribute, CoreAttributes, StylingAttributes, PresentationAttributes


class DrawSegment:
  def __neg__(self):
    raise NotImplementedError()

  @property
  def rel_x(self):
    return 0

  @property
  def rel_y(self):
    return 0

  def abs_x(self, x: float):
    return x + self.rel_x

  def abs_y(self, y: float):
    return y + self.rel_y

  def placeholder(self, width: float, height: float) -> 'DrawSegment':
    return self


class d(Attribute[list[DrawSegment]], DrawSegment):
  sep = ' '

  def __str__(self):
    value = (
        str(value)
        for value in self.flat_values
    )
    return f'{self.sep.join(value)}'

  def __add__(self, other: 'd'):
    return d(self.value + other.value)

  def __sub__(self, other: 'd'):
    return self + -other

  def __neg__(self):
    return d([-value for value in self.value])

  @property
  def flat_values(self):
    for value in self.value:
      if isinstance(value, d):
        yield from value.fill_placeholders.flat_values
      else:
        yield value

    return None

  @property
  def width(self):
    x = 0.0
    widths: set[float] = set()
    for value in self.flat_values:
      widths.add(x)
      x = value.abs_x(x)
    widths.add(x)

    return max(widths) - min(widths)

  @property
  def height(self):
    y = 0.0
    heights: set[float] = set()
    for value in self.flat_values:
      heights.add(y)
      y = value.abs_y(y)
    heights.add(y)

    return max(heights) - min(heights)

  @property
  def rel_x(self):
    return reduce(lambda x, value: value.abs_x(x), self.flat_values, 0.0)

  @property
  def rel_y(self):
    return reduce(lambda y, value: value.abs_y(y), self.flat_values, 0.0)

  @property
  def fill_placeholders(self):
    return d([
        value.fill_placeholders
        if isinstance(value, d) else
        value.placeholder(self.width, self.height)
        for value in self.value
    ])

  def placeholder(self, width: float, height: float) -> DrawSegment:
    return d([
        value.placeholder(width, height)
        for value in self.value
    ])

  class m(DrawSegment):
    def __init__(self, x: float, y: float):
      self.x = x
      self.y = y

    def __str__(self):
      return f'm {self.x:.2f} {self.y:.2f}'

    @property
    def rel_x(self):
      return self.x

    @property
    def rel_y(self):
      return self.y

  class v(DrawSegment):
    def __init__(self, value: float):
      self.value = value

    def __add__(self, other: 'd.v'):
      return d.v(self.value + other.value)

    def __sub__(self, other: 'd.v'):
      return d.v(self.value - other.value)

    def __neg__(self):
      return d.v(-self.value)

    def __str__(self):
      return f'v {self.value:.2f}'

    @property
    def rel_y(self):
      return self.value

  class h(DrawSegment):
    def __init__(self, value: float):
      self.value = value

    def __add__(self, other: 'd.h'):
      return d.h(self.value + other.value)

    def __sub__(self, other: 'd.h'):
      return d.h(self.value - other.value)

    def __neg__(self):
      return d.h(-self.value)

    def __str__(self):
      return f'h {self.value:.2f}'

    @property
    def rel_x(self):
      return self.value

  class c(DrawSegment):
    def __init__(self, dx1: float, dy1: float, dx2: float, dy2: float, dx: float, dy: float):
      self.dx1 = dx1
      self.dx2 = dx2
      self.dx = dx
      self.dy1 = dy1
      self.dy2 = dy2
      self.dy = dy

    def __neg__(self):
      return d.c(-self.dx1, -self.dy1, -self.dx2, -self.dy2, -self.dx, -self.dy)

    def __str__(self):
      return f'c {self.dx1:.2f} {self.dy1:.2f} {self.dx2:.2f} {self.dy2:.2f} {self.dx:.2f} {self.dy:.2f}'

    @property
    def rel_x(self):
      return self.dx

    @property
    def rel_y(self):
      return self.dy

  class z(DrawSegment):
    def __neg__(self):
      return self

    def __str__(self):
      return 'z'


class placeholder(DrawSegment):
  def __init__(self, remaining: Callable[[float, float], DrawSegment]):
    self._remaining = remaining

  def __neg__(self):
    return placeholder(lambda width, height: -self.placeholder(width, height))

  def placeholder(self, width: float, height: float) -> DrawSegment:
    return self._remaining(width, height)


@dataclass
class PathAttributes(CoreAttributes, StylingAttributes, PresentationAttributes):
  d: 'd | None' = None
  pathLength: int | None = None


class path(Element[PathAttributes]):
  element = 'path'
  attrs = PathAttributes
