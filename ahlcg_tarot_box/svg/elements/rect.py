from dataclasses import dataclass

from .core import Element
from ..attributes import CoreAttributes, StylingAttributes, auto, length, percentage


@dataclass
class CircleAttributes(CoreAttributes, StylingAttributes):
  x: float | length | percentage | None = None
  y: float | length | percentage | None = None
  width: auto | float | length | percentage | None = None
  height: auto | float | length | percentage | None = None
  rx: auto | float | length | percentage | None = None
  ry: auto | float | length | percentage | None = None
  pathLength: float | None = None


class rect(Element[CircleAttributes]):
  element = 'rect'
  attrs = CircleAttributes
