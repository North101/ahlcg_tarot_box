import pathlib

from .svg import *
from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  tab_out = d([
      d.m(0, 0),
      d.h(10),
      args.v_tab_half,
      args.v_tab_out,
      args.v_tab_out,
      args.v_tab_half,
      -d.h(10),
      -placeholder(lambda w, h: d.v(h)),
  ])

  tab_in = d([
      d.m(10 + args.tab + 2, 0),
      d.h(10),
      args.v_tab_half,
      args.v_tab_in,
      args.v_tab_in,
      args.v_tab_half,
      -d.h(10),
      -placeholder(lambda w, h: d.v(h)),
  ])

  p = d([
      tab_out,
      tab_in,
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
