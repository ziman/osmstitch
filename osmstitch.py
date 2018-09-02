#!/usr/bin/env python3

import os
import math
import logging
import argparse
import requests
from PIL import Image

TILE_SIZE = 256

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def div_roundup(x, y):
    return (x + y-1) // y

def load_tile(dirname_cache, x, y, z):
    log.debug('loading tile %s', (x, y, z))
    fname = os.path.join(dirname_cache, f'{z}/{x}/{y}.png')

    if not os.path.exists(fname):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        resp = requests.get(f'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png')
        with open(fname, 'wb') as f:
            f.write(resp.content)

    return Image.open(fname)

def main(args):
    x_centre, y_centre = deg2num(args.lat, args.lon, args.zoom)
    width, height = tuple(map(int, args.size.split('x')))

    x_halfspan = div_roundup(width//2 - TILE_SIZE//2, TILE_SIZE)
    y_halfspan = div_roundup(height//2 - TILE_SIZE//2, TILE_SIZE)

    result = Image.new('RGB', (width, height))
    for dx in range(-x_halfspan, x_halfspan + 1):
        for dy in range(-y_halfspan, y_halfspan + 1):
            tile = load_tile(args.dirname_cache, x_centre + dx, y_centre + dy, args.zoom)
            result.paste(tile, (dx*TILE_SIZE - TILE_SIZE//2 + width//2, dy*TILE_SIZE - TILE_SIZE//2 + height//2))

    result.save(args.fname_out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('lat', type=float, help='latitude of the centre (deg)')
    ap.add_argument('lon', type=float, help='longitude of the centre (deg)')
    ap.add_argument('-z', '--zoom', type=int, default=13, help='zoom [%(default)s]')
    ap.add_argument('-s', '--size', default='2048x2048', help='size of output image [%(default)s]')
    ap.add_argument('-c', '--cache', dest='dirname_cache', default='cache/', help='cache directory [%(default)s]')
    ap.add_argument('-o', dest='fname_out', default='map.png', help='output filename [%(default)s]')
    main(ap.parse_args())
