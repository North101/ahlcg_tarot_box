from dataclasses import dataclass
from typing import Literal

from .base import Attributes, Attribute, XmlNamespace


none = Literal['none']
auto = Literal['auto']


class length(Attribute[float]):
  def __init__(self, value: float, unit: str | None = None):
    super().__init__(value)
    self.unit = unit

  def __str__(self):
    if self.unit:
      return f'{str(self.value)}{self.unit}'

    return str(self.value)


class percentage(Attribute[float]):
  pass


@dataclass
class CoreAttributes(Attributes):
  id: str | None = None
  lang: str | None = None
  tabindex: int | None = None
  xml: XmlNamespace | None = None
