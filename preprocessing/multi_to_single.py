import fiona
from shapely.geometry import mapping, Polygon

# Define a polygon feature geometry with one attribute
schema = {
    'geometry': 'Polygon',
    'properties': {'cz': 'int'},
}

# List of climate zone IDs to process
czs = [1, 2, 3, 4, 5, 6, 7, 8, 11, 14, 17, 21, 25]

base = 'climate_zones/'

for cz in czs:

    with fiona.open('{}multipart_files/{}.shp'.format(base, cz)) as shp:
        geoms = (shp[0]['geometry']['coordinates'])

    for i, g in enumerate(geoms):
        poly = Polygon(g[0], holes=g[1:])

        # Write a new Shapefile
        with fiona.open('{}singlepart_files/{}_{}.shp'.format(base, cz, i),
                        'w', 'ESRI Shapefile', schema) as c:
            c.write({
                'geometry': mapping(poly),
                'properties': {'cz': cz},
            })
