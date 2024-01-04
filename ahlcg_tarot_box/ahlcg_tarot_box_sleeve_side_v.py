import pathlib

from .svg.path import d, placeholder
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = d([
      d.h(args.thickness),
      args.h_tab_half,
      args.h_tab_out,
      args.h_tab_out,
      placeholder(lambda w, h: d.h((args.sleeve_width - w) / 2)),
      args.h_tab_out,
      args.h_tab_out,
      args.h_tab_half,
      d.h(args.finger_cutout),
      args.h_tab_half,
      args.h_tab_out,
      args.h_tab_out,
      placeholder(lambda w, h: d.h((args.sleeve_width - w) / 2)),
      args.h_tab_out,
      args.h_tab_out,
      args.h_tab_half,
      d.h(args.thickness),
  ])

  right_path = d.v(args.sleeve_depth - (args.thickness * 2))

  bottom_path = -top_path

  left_path = -right_path

  path = d([
      d.m(0, args.thickness),
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
