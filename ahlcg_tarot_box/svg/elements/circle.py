from dataclasses import dataclass

from .core import Element
from ..attributes import CoreAttributes, StylingAttributes, length, percentage


@dataclass
class CircleAttributes(CoreAttributes, StylingAttributes):
  cx: float | length | percentage | None = None
  cy: float | length | percentage | None = None
  r: float | length | percentage | None = None
  pathLength: float | None = None


class circle(Element[CircleAttributes]):
  element = 'circle'
  attrs = CircleAttributes
