from shapely.geometry import mapping, Polygon
from shapely.ops import transform
from functools import partial
import pyproj
import fiona

path = '/Users/stuart/CardiffProject/climate_zones/singlepart_files/11_13.shp'


def divide_poly(path):

    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'cz': 'int'},
    }

    with fiona.open(path) as shp:
        geoms = (shp[0]['geometry']['coordinates'])

    poly = Polygon(geoms[0], holes=geoms[1:])

    # Convert the poly to equal area coords so we can get its approx area
    # this is an approximation, and will not equal the utm areas for the
    # properly converted polygons.
    poly_equal = transform(partial(pyproj.transform,
                                   pyproj.Proj(init='EPSG:4326'),
                                   pyproj.Proj(proj='aea',
                                               lat1=poly.bounds[1],
                                               lat2=poly.bounds[3])), poly)

    # Early exit if the polygon is small enough already
    if poly_equal.area < 725000:
        return

    # (minx, miny, maxx, maxy)
    bounds = poly.bounds

    xwid = (bounds[2] - bounds[0]) / 2
    ywid = (bounds[3] - bounds[1]) / 2

    four_quarters = []

    bl = [(bounds[0], bounds[1]),
          (bounds[0], bounds[1] + ywid),
          (bounds[0] + xwid, bounds[1] + ywid),
          (bounds[0] + xwid, bounds[1])]

    tl = [(bounds[0], bounds[1] + ywid),
          (bounds[0], bounds[3]),
          (bounds[0] + xwid, bounds[3]),
          (bounds[0] + xwid, bounds[1] + ywid)]

    tr = [(bounds[0] + xwid, bounds[1] + ywid),
          (bounds[0] + xwid, bounds[3]),
          (bounds[2], bounds[3]),
          (bounds[2], bounds[1] + ywid)]

    br = [(bounds[0] + xwid, bounds[1]),
          (bounds[0] + xwid, bounds[1] + ywid),
          (bounds[2], bounds[1] + ywid),
          (bounds[2], bounds[1])]

    four_quarters = [bl, tl, tr, br]

    for j, quarter in enumerate(four_quarters):

        clipper = Polygon(quarter)
        clipped = clipper.intersection(poly)

        # If there are more than one polygons in an intersection output it is
        # stored as a MultiPolygon, if there are lines and polys as a result of an
        # intersection it is stored as a GeometryCollection.
        # Otherwise it is just a polygon.
        # Need to decide on a naming scheme that will not overwrite any files.
        if clipped.type is 'GeometryCollection' or clipped.type is 'MultiPolygon':

            for i, geom in enumerate(clipped):
                if geom.type is 'Polygon':

                    # Write a new Shapefile
                    with fiona.open('11_{}_{}.shp'.format(j, i), 'w', 'ESRI Shapefile', schema) as c:
                        c.write({
                            'geometry': mapping(geom),
                            'properties': {'cz': 11},
                        })
        elif clipped.type is 'Polygon':
            # Write a new Shapefile
            with fiona.open('11_{}_0.shp'.format(j), 'w', 'ESRI Shapefile', schema) as c:
                c.write({
                    'geometry': mapping(clipped),
                    'properties': {'cz': 11},
                })

        else:
            print('Odd geometry:', clipped.type)

divide_poly(path)
