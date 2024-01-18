import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  width = (args.tray_width - args.finger_cutout) / 2

  top_path = path.d([
      path.d.h(args.thickness),
      path.placeholder(lambda w, h: path.d.h(width - w - 5)),
  ])

  right_path = path.d([
      path.d.c(0, 0, 5, 0, 5, 5),
      path.placeholder(lambda w, h: path.d.v(args.tray_depth - args.thickness - h)),
  ])

  bottom_path = path.d([
      -args.h_tab_half(args.tab),
      -args.h_tab(args.tab, True),
      -args.h_tab(args.tab, True),
      -path.placeholder(lambda w, h: path.d.h(width - w)),
      -args.h_tab(args.tab, True),
      -args.h_tab(args.tab, True),
      -args.h_tab_half(args.tab),
      -path.d.h(args.thickness),
  ])

  left_path = path.d([
      -path.placeholder(lambda w, h: path.d.v((args.depth - h) / 2)),
      -args.v_tab(args.tab, False),
      -path.placeholder(lambda w, h: path.d.v((args.depth - h) / 2)),
  ])

  d = path.d([
      path.d.m(0, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
      path.d.z(),
  ])

  s = svg(
      attrs=svg.attrs(
          width=length(round(d.width, 2), 'mm'),
          height=length(round(d.height, 2), 'mm'),
          viewBox=(0, 0, round(d.width, 2), round(d.height, 2)),
      ),
      children=[
          path(attrs=path.attrs(
              d=d,
          ) | args.cut),
      ]
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
