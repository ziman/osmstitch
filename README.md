# osmstitch

Stitch raster maps from OSM tiles.

Please be careful about your data usage and don't overload OSM tileservers:
https://operations.osmfoundation.org/policies/tiles/

## Synopsis

```
$ ./osmstitch.py --help
usage: osmstitch.py [-h] [-z ZOOM] [-s SIZE] [-c DIRNAME_CACHE] [-o FNAME_OUT]
                    lat lon

positional arguments:
  lat
  lon

optional arguments:
  -h, --help            show this help message and exit
  -z ZOOM, --zoom ZOOM
  -s SIZE, --size SIZE
  -c DIRNAME_CACHE, --cache DIRNAME_CACHE
  -o FNAME_OUT
```

## License

MIT
