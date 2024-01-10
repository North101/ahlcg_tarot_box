import pathlib

from .svg import *
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

  p = d([
      d.m(0, args.thickness),
      top_path,
      right_path,
      -top_path,
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
