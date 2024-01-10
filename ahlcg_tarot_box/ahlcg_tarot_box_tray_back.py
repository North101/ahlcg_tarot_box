import pathlib

from .svg import *
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
              attrs=g.attrs(
                  transform=transform.translate(args.thickness, args.thickness),
                  fill='none',
                  stroke='black',
                  stroke_width=0.001,
              ),
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
                      attrs=g.attrs(transform=transform.translate(
                          round((args.width - (args.tray_icon.width * args.tray_icon.scale)) / 2, 2),
                          round((args.height - (args.tray_icon.height * args.tray_icon.scale)) / 2, 2),
                      )),
                      children=[
                          g(
                              attrs=g.attrs(
                                  transform=transform.scale(args.tray_icon.scale),
                                  fill='black',
                                  stroke='none',
                                  stroke_width=0.001,
                              ),
                              children=[
                                  pathlib.Path(args.tray_icon.path).read_text().strip(),
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
