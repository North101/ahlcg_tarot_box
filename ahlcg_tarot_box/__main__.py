import argparse
import pathlib

from .shared import *


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--output',
                      type=pathlib.Path, default='output', help='output path')
  parser.add_argument('--width',
                      type=float, default=123, help='card width (mm)')
  parser.add_argument('--height',
                      type=float, default=73, help='card height (mm)')
  parser.add_argument('--depth',
                      type=float, default=15, help='card stack depth (mm)')
  parser.add_argument('--thickness',
                      type=float, default=3.17, help='wood thickness (mm)')
  parser.add_argument('--kerf',
                      type=float, default=0.07, help='kerf (mm)')

  parser.add_argument('--padding',
                      type=float, default=2, help='padding added to card width and height (mm)')
  parser.add_argument('--gap',
                      type=float, default=0.1, help='gap between sleeve and tray (mm)')
  parser.add_argument('--tab',
                      type=float, default=5, help='tab size (mm)')
  parser.add_argument('--finger_cutout',
                      type=float, default=20, help='size of the finger cutout (mm)')

  parser.add_argument('--magnet_r',
                      type=float, default=1.5, help='magnet radius (mm) (half the width)')
  parser.add_argument('--magnet_v',
                      type=float, default=16.5, help='magnet vertical offset (mm)')

  parser.add_argument('--sleeve_icon',
                      type=pathlib.Path, default='icons/the_circle_undone.svg', help='sleeve icon path')
  parser.add_argument('--sleeve_icon_width',
                      type=float, default=65, help='sleeve icon width')
  parser.add_argument('--sleeve_icon_height',
                      type=float, default=64, help='sleeve icon height')
  parser.add_argument('--sleeve_icon_scale',
                      type=float, default=1.0, help='sleeve icon scale')

  parser.add_argument('--tray_icon',
                      type=pathlib.Path, default='icons/inexorable_fate.svg', help='tray icon path')
  parser.add_argument('--tray_icon_width',
                      type=float, default=65, help='tray icon width')
  parser.add_argument('--tray_icon_height',
                      type=float, default=64, help='tray icon height')
  parser.add_argument('--tray_icon_scale',
                      type=float, default=0.5, help='tray icon scale')

  return parser.parse_args()


def main():
  args = parse_args()
  svgs = write_all_svg(args=SVGArgs(
      output=args.output,
      width=args.width + args.padding,
      height=args.height + args.padding,
      depth=args.depth,
      thickness=args.thickness,
      kerf=args.kerf,
      tab=args.tab,
      gap=args.gap,
      finger_cutout=args.finger_cutout,
      magnet=MagnetArgs(
          r=args.magnet_r,
          v=args.magnet_v,
      ),
      sleeve_icon=IconArgs(
          path=args.sleeve_icon,
          width=args.sleeve_icon_width,
          height=args.sleeve_icon_height,
          scale=args.sleeve_icon_scale,
      ),
      tray_icon=IconArgs(
          path=args.tray_icon,
          width=args.tray_icon_width,
          height=args.tray_icon_height,
          scale=args.tray_icon_scale,
      ),
  ))

  svgs = [
      (str(svg[0]), f'{svg[1]:.2f}mm', f'{svg[2]:.2f}mm')
      for svg in svgs
  ]
  name_len = max(len(svg[0]) for svg in svgs)
  width_len = max(len(svg[1]) for svg in svgs)
  height_len = max(len(svg[2]) for svg in svgs)
  for svg in svgs:
    print(f'{str(svg[0]):<{name_len}} @ {svg[1]:>{width_len}} x {svg[2]:>{height_len}}')


if __name__ == '__main__':
  main()
