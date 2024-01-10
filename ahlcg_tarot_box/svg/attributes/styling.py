from dataclasses import dataclass

from .base import Attributes


@dataclass
class StylingAttributes(Attributes):
  class_: str | list[str] | None = None
  style: str | list[str] | None = None
