import pathlib

from .svg.path import d
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  path = d([
      d.m(0, 0),
      d.h(10),
      args.v_tab_half,
      args.v_tab_out,
      args.v_tab_out,
      args.v_tab_half,
      -d.h(10),
      -d.v(25),
      d.m(15, 0),
      d.h(10),
      args.v_tab_half,
      args.v_tab_in,
      args.v_tab_in,
      args.v_tab_half,
      -d.h(10),
      -d.v(25),
      d.z(),
  ])

  filename = pathlib.Path(__file__).with_suffix('.svg').name
  with SVGTemplate(args.template / filename) as f:
    f.write(
        args.output / filename,
        path=path,
        thickness=args.thickness,
        magnet_r=args.magnet.r - args.kerf,
    )

  return args.output / filename, path.width, path.height
