#!/usr/bin/env python3

import os
import re
import math
import httpx
import logging
import argparse
import subprocess
import urllib.parse
from PIL import Image

TILE_SIZE = 256

PAPER_SIZE = {
    'a4': (210, 297),
}

TILE_URLS = {
    'osm': 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'google-satellite': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    'freemap.sk': 'https://outdoor.tiles.freemap.sk/{z}/{x}/{y}.png',
    'opentopomap': 'https://a.tile.opentopomap.org/{z}/{x}/{y}.png',
}

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

def load_tile(http, dirname_cache, url_template, x, y, z):
    log.debug('loading tile %s', (x, y, z))

    url = url_template.format(x=x, y=y, z=z)
    url_parsed = urllib.parse.urlparse(url)
    fname = os.path.join(dirname_cache, url_parsed.netloc, url_parsed.path.strip('/'))

    if not os.path.exists(fname):
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        resp = http.get(
            url,
            headers={'User-Agent': 'https://github.com/ziman/osmstitch'}
        )
        with open(fname, 'wb') as f:
            f.write(resp.content)

    return Image.open(fname)

def paper_size(ppi, rank, orientation):
    factor  = 2**(rank/2)
    longer  = round(ppi * 46.77 / factor)
    shorter = round(ppi * 33.07 / factor)

    if orientation == 'landscape':
        return longer, shorter
    elif orientation == 'portrait':
        return shorter, longer
    else:
        raise Exception('unknown page orientation: %s' % orientation)

def main(args):
    x_centre, y_centre = deg2num(args.lat, args.lon, args.zoom)

    match = re.match('a(\d)-(portrait|landscape)', args.size)
    if match:
        width, height = paper_size(
            ppi=args.ppi,
            rank=int(match.group(1)),
            orientation=match.group(2),
        )
        page_size = 'a%s' % match.group(1)
    else:
        width, height = tuple(map(int, args.size.split('x')))
        page_size = None

    x_halfspan = div_roundup(width//2 - TILE_SIZE//2, TILE_SIZE)
    y_halfspan = div_roundup(height//2 - TILE_SIZE//2, TILE_SIZE)

    url_template = TILE_URLS.get(args.url_template, args.url_template)

    http = httpx.Client()
    result = Image.new('RGB', (width, height))
    for dx in range(-x_halfspan, x_halfspan + 1):
        for dy in range(-y_halfspan, y_halfspan + 1):
            tile = load_tile(http, args.dirname_cache, url_template, x_centre + dx, y_centre + dy, args.zoom)
            result.paste(tile, (dx*TILE_SIZE - TILE_SIZE//2 + width//2, dy*TILE_SIZE - TILE_SIZE//2 + height//2))

    result.save(args.fname_out)

    if page_size:
        subprocess.check_call([
            'convert', args.fname_out,
            '-rotate', '90' if width > height else '0',
            '-page', page_size,
            '-density', str(args.ppi),
            args.fname_out + '.pdf'
        ])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('lat', type=float, help='latitude of the centre (deg)')
    ap.add_argument('lon', type=float, help='longitude of the centre (deg)')
    ap.add_argument('-z', '--zoom', type=int, default=13, help='zoom [%(default)s]')
    ap.add_argument('-s', '--size', default='a4-landscape',
        help='size of output image [%(default)s], WxH (px) or: aN-(portrait|landscape)"')
    ap.add_argument('-c', '--cache', dest='dirname_cache', default='cache/', help='cache directory [%(default)s]')
    ap.add_argument('-o', dest='fname_out', default='map.png', help='output filename [%(default)s]')
    ap.add_argument('-p', '--ppi', default=150, type=int, help='pixels per inch [%(default)s]')
    ap.add_argument('-u', '--url-template', default='osm',
        help='tile url template [%(default)s]')
    main(ap.parse_args())
