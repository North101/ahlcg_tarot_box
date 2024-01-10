import pathlib

from .svg import *
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

  p = d([
      d.m(0, 0),
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
      ]
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  with filename.open('w') as f:
    f.write(str(s))

  return filename, p.width, p.height
