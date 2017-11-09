from shapely.geometry import mapping, Polygon
from shapely.ops import transform
from functools import partial
from uuid import uuid4
import pyproj
import fiona


def load_poly(path):
    '''
    From a path to a shapefile, load the geometry and return it as a shapely
    polygon object. Will do strange things if given non polygon input data.
    '''
    with fiona.open(path) as shp:
        geoms = (shp[0]['geometry']['coordinates'])

    return Polygon(geoms[0], holes=geoms[1:])


def write_shapefile(out_filename, geometry, zone_id):
    '''
    Wrapper around fiona's shapefile writer to standardise the attributes
    across files being written
    '''

    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'cz': 'int'},
    }

    # write the shapefile using the schema
    with fiona.open(out_filename, 'w', 'ESRI Shapefile', schema) as c:
        c.write({
            'geometry': mapping(geometry),
            'properties': {'cz': zone_id},
        })


def dirty_area(poly):
    '''
    Convert the poly to equal area coords so we can get its approx area
    this is an approximation, and will not equal the utm areas for the
    properly converted polygons. Returns area in m^2
    '''
    poly_equal = transform(partial(pyproj.transform,
                                   pyproj.Proj(init='EPSG:4326'),
                                   pyproj.Proj(proj='aea',
                                               lat1=poly.bounds[1],
                                               lat2=poly.bounds[3])), poly)

    return poly_equal.area


def bbox_area(poly):
    '''
    Return the area in m^2 of the bounding box of a given polygon
    '''
    bounds = poly.bounds

    coords = [(bounds[0], bounds[1]),
              (bounds[0], bounds[3]),
              (bounds[2], bounds[3]),
              (bounds[2], bounds[1])]

    return dirty_area(Polygon(coords))


def divide_poly(poly):

    # Early exit if the polygon is small enough already
    if bbox_area(poly) < 725000000000:
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
        # stored as a MultiPolygon, if there are lines and polys as a result of
        # an intersection it is stored as a GeometryCollection.
        # Otherwise it is just a polygon.
        if clipped.type is 'GeometryCollection' or clipped.type is 'MultiPolygon':

            for i, geom in enumerate(clipped):
                if geom.type is 'Polygon':

                    if bbox_area(geom) < 725000000000:
                        # Write a new Shapefile if we have not made a sliver
                        if dirty_area(geom) > 3000000000:
                            write_shapefile('{}.shp'.format(uuid4()), geom, 11)
                    else:
                        # Recurse as the polygon is still too big
                        divide_poly(geom)

        elif clipped.type is 'Polygon':
            if bbox_area(clipped) < 725000000000:
                # Write a new Shapefile if we have not made a sliver
                if dirty_area(clipped) > 3000000000:
                    write_shapefile('{}.shp'.format(uuid4()), clipped, 11)
            else:
                # Recurse as the polygon is still too big
                divide_poly(clipped)

        else:
            print('Odd geometry:', clipped.type)

path = '/Users/stuart/CardiffProject/climate_zones/singlepart_files/11_13.shp'
divide_poly(load_poly(path))
