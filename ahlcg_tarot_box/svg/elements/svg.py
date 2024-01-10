from dataclasses import dataclass

from ..attributes import CoreAttributes, length, percentage
from .core import Element


@dataclass
class SVGAttributes(CoreAttributes):
  xmlns: str = 'http://www.w3.org/2000/svg'
  baseProfile: str | None = None
  preserveAspectRatio: str | None = None
  version: float | None = None
  viewBox: tuple[float, float, float, float] | None = None
  width: float | length | percentage | None = None
  height: float | length | percentage | None = None
  x: float | length | percentage | None = None
  y: float | length | percentage | None = None


class svg(Element[SVGAttributes]):
  element = 'svg'
  attrs = SVGAttributes
