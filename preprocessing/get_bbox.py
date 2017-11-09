import fiona
import os
import json
import utm

path = '/Users/stuart/CardiffProject/climate_zones/singlepart_files_split/'

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

        # Compute the utm zone for the lower left corner of the bbox
        utm_zone = utm.from_latlon(minlat, minlong)

        # Convert latitude band into N or S
        if ord(utm_zone[3]) >= 78:
            utm_letter = 'north'
        elif ord(utm_zone[3]) < 78:
            utm_letter = 'south'

        output = {'bbox': [maxlat, minlat, maxlong, minlong],
                  'south_max': False, 'south_min': False,
                  'west_max': False, 'west_min': False,
                  'utm_zone': [utm_zone[2], utm_letter]}

        if maxlat < 0:
            output['south_max'] = True
        if minlat < 0:
            output['south_min'] = True
        if maxlong < 0:
            output['west_max'] = True
        if minlong < 0:
            output['west_min'] = True

        results[f] = output

with open('../processing/bboxes.json', 'w') as f:
    json.dump(results, f, sort_keys=True, indent=4)
