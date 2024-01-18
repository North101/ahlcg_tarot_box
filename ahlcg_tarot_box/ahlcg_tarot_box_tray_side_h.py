import pathlib

from pysvg import length, path, svg

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = path.d([
      path.placeholder(lambda w, h: path.d.h((args.tray_depth - args.thickness - w) / 2)),
      args.h_tab(args.tab, True),
      path.placeholder(lambda w, h: path.d.h((args.tray_depth - args.thickness - w) / 2)),
  ])

  right_path = path.d([
      args.v_tab_half(args.tab),
      args.v_tab(args.tab, True),
      args.v_tab(args.tab, True),
      path.placeholder(lambda w, h: path.d.v((args.height - h) / 2)),
      args.v_tab(args.tab, True),
      path.placeholder(lambda w, h: path.d.v((args.height - h) / 2)),
      args.v_tab(args.tab, True),
      args.v_tab(args.tab, True),
      args.v_tab_half(args.tab),
  ])

  left_path = -path.d.v(args.tray_height - (args.thickness * 2))

  d = path.d([
      path.d.m(0, args.thickness),
      top_path,
      right_path,
      -top_path,
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
