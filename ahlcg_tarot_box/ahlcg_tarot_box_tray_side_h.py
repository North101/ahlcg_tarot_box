import pathlib

from .svg.path import d, placeholder
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = d([
      placeholder(lambda w, h: d.h((args.tray_depth - args.thickness - w) / 2)),
      args.h_tab_out,
      placeholder(lambda w, h: d.h((args.tray_depth - args.thickness - w) / 2)),
  ])

  right_path = d([
      args.v_tab_half,
      args.v_tab_out,
      args.v_tab_out,
      placeholder(lambda w, h: d.v((args.height - h) / 2)),
      args.v_tab_out,
      placeholder(lambda w, h: d.v((args.height - h) / 2)),
      args.v_tab_out,
      args.v_tab_out,
      args.v_tab_half,
  ])

  left_path = -d.v(args.tray_height - (args.thickness * 2))

  path = d([
      d.m(0, args.thickness),
      top_path,
      right_path,
      -top_path,
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
