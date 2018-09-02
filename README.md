# osmstitch

Stitch raster maps from OSM tiles.

Please be careful about your data usage and don't overload the OSM tileservers.
See the OSM tile policies: https://operations.osmfoundation.org/policies/tiles/

## Synopsis

```
$ ./osmstitch.py --help
usage: osmstitch.py [-h] [-z ZOOM] [-s SIZE] [-c DIRNAME_CACHE] [-o FNAME_OUT]
                    lat lon

positional arguments:
  lat                   latitude of the centre (deg)
  lon                   longitude of the centre (deg)

optional arguments:
  -h, --help            show this help message and exit
  -z ZOOM, --zoom ZOOM  zoom [13]
  -s SIZE, --size SIZE  size of output image [2048x2048]
  -c DIRNAME_CACHE, --cache DIRNAME_CACHE
                        cache directory [cache/]
  -o FNAME_OUT          output filename [map.png]
```

## License

MIT
