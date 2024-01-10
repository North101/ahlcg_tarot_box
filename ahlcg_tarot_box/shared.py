from typing import NamedTuple, Protocol
import pathlib

from .svg.elements.path import *


class IconArgs(NamedTuple):
  path: pathlib.Path
  width: float
  height: float
  scale: float


class MagnetArgs(NamedTuple):
  v: float
  r: float


class SVGArgs(NamedTuple):
  output: pathlib.Path
  width: float
  height: float
  depth: float
  thickness: float
  kerf: float
  tab: float
  gap: float
  finger_cutout: float
  magnet: MagnetArgs
  sleeve_icon: IconArgs
  tray_icon: IconArgs

  @property
  def tray_width(self):
    return self.width + (self.thickness * 2)

  @property
  def tray_height(self):
    return self.height + (self.thickness * 2)

  @property
  def tray_depth(self):
    return self.depth + self.thickness

  @property
  def sleeve_width(self):
    return self.tray_width

  @property
  def sleeve_height(self):
    return self.tray_height + (self.thickness * 2) + (self.gap * 2)

  @property
  def sleeve_depth(self):
    return self.tray_depth + (self.thickness * 2) + (self.gap * 2)

  @property
  def h_tab_half(self):
    return d.h(self.tab / 2)

  @property
  def h_tab_in(self):
    return d([
        d.h((self.tab / 2) + self.kerf),
        d.v(self.thickness),
        d.h(self.tab + -self.kerf + -self.kerf),
        -d.v(self.thickness),
        d.h(self.kerf + (self.tab / 2)),
    ])

  @property
  def h_tab_out(self):
    return d([
        d.h((self.tab / 2) + -self.kerf),
        -d.v(self.thickness),
        d.h(self.kerf + self.tab + self.kerf),
        d.v(self.thickness),
        d.h((self.tab / 2) + -self.kerf),
    ])

  @property
  def v_tab_half(self):
    return d.v(self.tab / 2)

  @property
  def v_tab_in(self):
    return d([
        d.v((self.tab / 2) + self.kerf),
        -d.h(self.thickness),
        d.v(self.tab + -self.kerf + -self.kerf),
        d.h(self.thickness),
        d.v(self.kerf + (self.tab / 2)),
    ])

  @property
  def v_tab_out(self):
    return d([
        d.v((self.tab / 2) + -self.kerf),
        d.h(self.thickness),
        d.v(self.kerf + self.tab + self.kerf),
        -d.h(self.thickness),
        d.v((self.tab / 2) + -self.kerf),
    ])


class RegisterSVGCallable(Protocol):
  def __call__(self, args: SVGArgs) -> tuple[pathlib.Path, float, float]:
    ...


svg_list: list[RegisterSVGCallable] = []


def register_svg(f: RegisterSVGCallable):
  svg_list.append(f)
  return f


def write_all_svg(args: SVGArgs):
  return [
      write_svg(args)
      for write_svg in svg_list
  ]
