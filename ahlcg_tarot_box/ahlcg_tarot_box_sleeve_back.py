import pathlib

from pysvg import circle, g, length, path, svg, transforms

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
              attrs=g.attrs(
                  transform=transforms.translate(
                      args.thickness,
                      round(args.thickness + args.gap + args.thickness, 2),
                  ),
              ) | args.cut,
              children=[
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 4, 2),
                      cy=args.magnet.v,
                      r=args.magnet.r - args.kerf,
                  )),
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 2, 2),
                      cy=args.magnet.v,
                      r=args.magnet.r - args.kerf,
                  )),
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 4 * 3, 2),
                      cy=args.magnet.v,
                      r=args.magnet.r - args.kerf,
                  )),
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 4, 2),
                      cy=round(args.height - args.magnet.v, 2),
                      r=args.magnet.r - args.kerf,
                  )),
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 2, 2),
                      cy=round(args.height - args.magnet.v, 2),
                      r=args.magnet.r - args.kerf,
                  )),
                  circle(attrs=circle.attrs(
                      cx=round(args.width / 4 * 3, 2),
                      cy=round(args.height - args.magnet.v, 2),
                      r=args.magnet.r - args.kerf,
                  )),
              ],
          ),
      ],
  )

  filename = args.output / pathlib.Path(__file__).with_suffix('.svg').name
  return filename, s
