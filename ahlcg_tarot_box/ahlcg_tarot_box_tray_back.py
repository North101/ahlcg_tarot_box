import pathlib

from pysvg import circle, g, length, path, svg, transforms

from .shared import *


@register_svg
def write_svg(args: SVGArgs):
  half_circle = args.finger_cutout / 2

  top_path = path.d([
      path.d.h(args.thickness),
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.h((args.tray_width - w) / 2)),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      args.h_tab_half(args.tab),
      path.d.v(args.thickness),
      path.d.c(0, half_circle, half_circle, half_circle, half_circle, half_circle),
      path.d.c(0, 0, half_circle, 0, half_circle, -half_circle),
      -path.d.v(args.thickness),
      args.h_tab_half(args.tab),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.h((args.tray_width - w) / 2)),
      args.h_tab(args.tab, False),
      args.h_tab(args.tab, False),
      args.h_tab_half(args.tab),
      path.d.h(args.thickness),
  ])

  right_path = path.d([
      path.d.v(args.thickness),
      args.v_tab_half(args.tab),
      args.v_tab(args.tab, False),
      args.v_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.v((args.tray_height - h) / 2)),
      args.v_tab(args.tab, False),
      path.placeholder(lambda w, h: path.d.v((args.tray_height - h) / 2)),
      args.v_tab(args.tab, False),
      args.v_tab(args.tab, False),
      args.v_tab_half(args.tab),
      path.d.v(args.thickness),
  ])

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
                  transform=transforms.translate(args.thickness, args.thickness),
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
                  g(
                      attrs=g.attrs(transform=transforms.translate(
                          x=round((args.width - (args.tray_icon.width * args.tray_icon.scale)) / 2, 2),
                          y=round((args.height - (args.tray_icon.height * args.tray_icon.scale)) / 2, 2),
                      )),
                      children=[
                          g(
                              attrs=g.attrs(
                                  transform=transforms.scale(args.tray_icon.scale),
                              ) | args.engrave,
                              children=[
                                  args.tray_icon.path.read_text().strip(),
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
