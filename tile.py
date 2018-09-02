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

def load_tile(x, y, z):
    log.debug('loading tile %s', (x, y, z))

def main(args):
    x_centre, y_centre = deg2num(args.lat, args.lon, args.zoom)
    width, height = tuple(map(int, args.size.split('x')))

    x_halfspan = div_roundup(width//2 - TILE_SIZE//2, TILE_SIZE)
    y_halfspan = div_roundup(height//2 - TILE_SIZE//2, TILE_SIZE)

    result = Image.new('RGB', (width, height))
    for x in range(x_centre - x_halfspan, x_centre + x_halfspan + 1):
        for y in range(y_centre - y_halfspan, y_centre + y_halfspan + 1):
            tile = load_tile(x, y, args.zoom)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('lat', type=float)
    ap.add_argument('lon', type=float)
    ap.add_argument('-z', '--zoom', type=int, default=13)
    ap.add_argument('-s', '--size', default='2048x2048')
    ap.add_argument('-c', '--cache', default='cache/')
    main(ap.parse_args())
