import pathlib

from .svg.path import d, placeholder
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = d([
      d.h(args.thickness),
      args.h_tab_half,
      args.h_tab_in,
      args.h_tab_in,
      placeholder(lambda w, h: d.h((args.sleeve_width - w) / 2)),
      args.h_tab_in,
      args.h_tab_in,
      args.h_tab_half,
      d.h(args.finger_cutout),
      args.h_tab_half,
      args.h_tab_in,
      args.h_tab_in,
      placeholder(lambda w, h: d.h((args.sleeve_width - w) / 2)),
      args.h_tab_in,
      args.h_tab_in,
      args.h_tab_half,
      d.h(args.thickness),
  ])

  right_path = d.v(args.sleeve_height)

  bottom_path = -top_path

  left_path = -right_path

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
        play=args.gap,
        icon=pathlib.Path(args.sleeve_icon.path).read_text(),
        icon_scale=args.sleeve_icon.scale,
        icon_x=round((args.width - (args.sleeve_icon.width * args.sleeve_icon.scale)) / 2, 2),
        icon_y=round((args.height - (args.sleeve_icon.height * args.sleeve_icon.scale)) / 2, 2),
    )

  return args.output / filename, path.width, path.height
