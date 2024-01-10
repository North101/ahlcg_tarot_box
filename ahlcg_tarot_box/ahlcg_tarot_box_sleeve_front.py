import pathlib

from .svg import *
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
          g(
              attrs=g.attrs(transform=transform.translate(
                  args.thickness,
                  round(args.thickness + args.gap + args.thickness, 2),
              )),
              children=[
                  g(
                      attrs=g.attrs(
                          transform=transform.translate(
                              round((args.width - (args.sleeve_icon.width * args.sleeve_icon.scale)) / 2, 2),
                              round((args.height - (args.sleeve_icon.height * args.sleeve_icon.scale)) / 2, 2),
                          ),
                          fill='black',
                          stroke='none',
                          stroke_width=0.001,
                      ),
                      children=[
                          g(
                              attrs=g.attrs(transform=transform.scale(args.sleeve_icon.scale)),
                              children=[
                                  pathlib.Path(args.sleeve_icon.path).read_text().strip(),
                              ],
                          ),
                      ],
                  ),
              ],
          ),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  with filename.open('w') as f:
    f.write(str(s))

  return filename, p.width, p.height
