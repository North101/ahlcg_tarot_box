import pathlib

from .svg.path import d, placeholder
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  width = (args.tray_width - args.finger_cutout) / 2

  top_path = d([
      d.h(args.thickness),
      placeholder(lambda w, h: d.h(width - w - 5)),
  ])

  right_path = d([
      d.c(0, 0, 5, 0, 5, 5),
      placeholder(lambda w, h: d.v(args.tray_depth - args.thickness - h)),
  ])

  bottom_path = d([
      -args.h_tab_half,
      -args.h_tab_out,
      -args.h_tab_out,
      -placeholder(lambda w, h: d.h(width - w)),
      -args.h_tab_out,
      -args.h_tab_out,
      -args.h_tab_half,
      -d.h(args.thickness),
  ])

  left_path = d([
      -placeholder(lambda w, h: d.v((args.depth - h) / 2)),
      -args.v_tab_in,
      -placeholder(lambda w, h: d.v((args.depth - h) / 2)),
  ])

  path = d([
      d.m(0, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
      d.z(),
  ])

  filename = pathlib.Path(__file__).with_suffix('.svg').name
  with SVGTemplate(args.template / filename) as f:
    f.write(
        args.output / filename,
        path=path,
        thickness=args.thickness,
    )

  return args.output / filename, path.width, path.height
