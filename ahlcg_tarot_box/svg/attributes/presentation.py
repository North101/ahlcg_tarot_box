from dataclasses import dataclass
from typing import Literal

from .base import Attributes, Attribute
from .core import none, length, percentage


class _transform:
  pass


class transform:
  class translate(_transform):
    def __init__(self, x: float, y: float | None = None):
      self.x = x
      self.y = y

    def __str__(self):
      if self.y is None:
        return f'translate({self.x})'

      return f'translate({self.x} {self.y})'

  class scale(_transform):
    def __init__(self, value: float):
      self.value = value

    def __str__(self):
      return f'scale({self.value})'


css_color_3 = Literal['black'] | Literal['silver'] | Literal['gray'] | Literal['white'] | Literal['maroon'] | Literal['red'] | Literal['purple'] | Literal[
    'fuchsia'] | Literal['green'] | Literal['lime'] | Literal['olive'] | Literal['yellow'] | Literal['navy'] | Literal['blue'] | Literal['teal'] | Literal['aqua']


class paint(Attribute[str]):
  pass


paint_type = none | css_color_3 | Literal['context-fill'] | Literal['context-stroke'] | paint


@dataclass
class PresentationAttributes(Attributes):
  transform: _transform | list[_transform] | None = None
  fill: paint_type | None = None
  stroke: paint_type | None = None
  stroke_width: float | length | percentage | None = None
