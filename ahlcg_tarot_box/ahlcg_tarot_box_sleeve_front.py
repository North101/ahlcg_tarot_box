import pathlib

from pysvg import g, length, path, svg, transforms

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  top_path = path.d([
      path.d.h(args.thickness),
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.h((args.sleeve_width - w) / 2)),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      args.h_tab_half(args.tab),
      path.d.h(args.finger_cutout),
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.h((args.sleeve_width - w) / 2)),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      args.h_tab_half(args.tab),
      path.d.h(args.thickness),
  ])

  right_path = path.d.v(args.sleeve_height)

  bottom_path = -top_path

  left_path = -right_path

  d = path.d([
      path.d.m(0, 0),
      top_path,
      right_path,
      bottom_path,
      left_path,
      path.d.z(),
  ])

  s = svg(
      attrs=svg.attrs(
          width=length(round(d.width, 2), 'mm'),
          height=length(round(d.height, 2), 'mm'),
          viewBox=(0, 0, round(d.width, 2), round(d.height, 2)),
      ),
      children=[
          path(attrs=path.attrs(
              d=d,
          ) | args.cut),
          g(
              attrs=g.attrs(transform=transforms.translate(
                  x=args.thickness,
                  y=round(args.thickness + args.gap + args.thickness, 2),
              )),
              children=[
                  g(
                      attrs=g.attrs(
                          transform=transforms.translate(
                              x=round((args.width - (args.sleeve_icon.width * args.sleeve_icon.scale)) / 2, 2),
                              y=round((args.height - (args.sleeve_icon.height * args.sleeve_icon.scale)) / 2, 2),
                          ),
                      ) | args.engrave,
                      children=[
                          g(
                              attrs=g.attrs(transform=transforms.scale(args.sleeve_icon.scale)),
                              children=[
                                  args.sleeve_icon.path.read_text().strip(),
                              ],
                          ),
                      ],
                  ),
              ],
          ),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
