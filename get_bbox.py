import fiona
import os

path = '/Users/stuart/CardiffProject/climate_zones/singlepart_files/'

results = {}
for f in os.listdir(path):
    if f.endswith('.shp'):

        with fiona.open(path + f) as shp:
            geoms = (shp[0]['geometry']['coordinates'])

        lats = []
        longs = []

        for g in geoms[0]:
            lats.append(g[1])
            longs.append(g[0])

        maxlat = max(lats)
        minlat = min(lats)
        maxlong = max(longs)
        minlong = min(longs)

        output = {'bbox': [maxlat, minlat, maxlong, minlong],
                  'south_max': False, 'south_min': False,
                  'west_max': False, 'west_min': False}

        if maxlat < 0:
            output['south_max'] = True
        if minlat < 0:
            output['south_min'] = True
        if maxlong < 0:
            output['west_max'] = True
        if minlong < 0:
            output['west_min'] = True

        results[f] = output

print(results)
