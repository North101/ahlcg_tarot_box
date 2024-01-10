from dataclasses import dataclass

from .core import Element
from ..attributes import CoreAttributes, StylingAttributes, PresentationAttributes


@dataclass
class GAttributes(CoreAttributes, StylingAttributes, PresentationAttributes):
  pass


class g(Element[GAttributes]):
  element = 'g'
  attrs = GAttributes
