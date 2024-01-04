import pathlib

from .svg.path import d, placeholder
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  half_circle = args.finger_cutout / 2

  top_path = d([
      d.h(args.thickness),
      args.h_tab_half,
      args.h_tab_in,
      args.h_tab_in,
      placeholder(lambda w, h: d.h((args.tray_width - w) / 2)),
      args.h_tab_in,
      args.h_tab_in,
      args.h_tab_half,
      d.v(args.thickness),
      d.c(0, half_circle, half_circle, half_circle, half_circle, half_circle),
      d.c(0, 0, half_circle, 0, half_circle, -half_circle),
      -d.v(args.thickness),
      args.h_tab_half,
      args.h_tab_in,
      args.h_tab_in,
      placeholder(lambda w, h: d.h((args.tray_width - w) / 2)),
      args.h_tab_in,
      args.h_tab_in,
      args.h_tab_half,
      d.h(args.thickness),
  ])

  right_path = d([
      d.v(args.thickness),
      args.v_tab_half,
      args.v_tab_in,
      args.v_tab_in,
      placeholder(lambda w, h: d.v((args.tray_height - h) / 2)),
      args.v_tab_in,
      placeholder(lambda w, h: d.v((args.tray_height - h) / 2)),
      args.v_tab_in,
      args.v_tab_in,
      args.v_tab_half,
      d.v(args.thickness),
  ])

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
        icon=pathlib.Path(args.tray_icon.path).read_text(),
        icon_scale=args.tray_icon.scale,
        icon_x=round((args.width - (args.tray_icon.width * args.tray_icon.scale)) / 2, 2),
        icon_y=round((args.height - (args.tray_icon.height * args.tray_icon.scale)) / 2, 2),
        magnet_r=args.magnet.r - args.kerf,
        magnet_top=args.magnet.v,
        magnet_left=round(args.width / 4, 2),
        magnet_center=round(args.width / 2, 2),
        magnet_right=round(args.width / 4 * 3, 2),
        magnet_bottom=round(args.height - args.magnet.v, 2),
    )

  return args.output / filename, path.width, path.height
