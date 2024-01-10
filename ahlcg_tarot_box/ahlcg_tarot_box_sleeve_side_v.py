import pathlib

from .svg import *
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

  p = d([
      d.m(0, args.thickness),
      top_path,
      right_path,
      bottom_path,
      left_path,
      d.z(),
  ])

  s = svg(
      attrs=svg.attrs(
          width=length(round(p.width, 2), 'mm'),
          height=length(round(p.height, 2), 'mm'),
          viewBox=(0, 0, round(p.width, 2), round(p.height, 2)),
      ),
      children=[
          path(attrs=path.attrs(
              d=p,
              fill='none',
              stroke='black',
              stroke_width=0.001,
          )),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  with filename.open('w') as f:
    f.write(str(s))

  return filename, p.width, p.height
