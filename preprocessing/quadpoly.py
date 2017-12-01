from shapely.geometry import mapping, Polygon
from shapely.ops import transform
from functools import partial
from uuid import uuid4
import pyproj
import fiona
import os


def uid():
    '''
    Wrapper around uuid4() to return a unique string with underscores instead
    of dashes.
    '''
    return str(uuid4()).replace('-', '_')


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

    outp = ('/Users/stuart/CardiffProject/climate_zones/'
            'singlepart_files_split_rerun/')

    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'cz': 'int'},
    }

    # write the shapefile using the schema
    with fiona.open(outp + out_filename, 'w', 'ESRI Shapefile', schema) as c:
        c.write({
            'geometry': mapping(geometry),
            'properties': {'cz': zone_id.split('_')[0]},
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


def get_cz_id(filename):
    '''
    Return the cz id and sub id as a string in the format 'czID_subID'
    '''
    return os.path.splitext(os.path.basename(filename))[0]


def divide_poly(poly, cz_id):
    '''
    Recursive method to divide a polygon by quartering its bounding box.
    '''

    # Early exit if the polygon is small enough already
    if bbox_area(poly) < 493000000000:
        return

    # (minx, miny, maxx, maxy)
    bounds = poly.bounds

    # Calculate dimensions of a quarter of the bbox
    xwid = (bounds[2] - bounds[0]) / 2
    ywid = (bounds[3] - bounds[1]) / 2

    # Generate the coordinates for each of the quarters
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
        types = ['GeometryCollection', 'MultiPolygon']
        if clipped.type is types[0] or clipped.type is types[1]:

            for i, geom in enumerate(clipped):
                if geom.type is 'Polygon':

                    if bbox_area(geom) < 493000000000:
                        # Write a new Shapefile if we have not made a sliver
                        if dirty_area(geom) > 1000000000:
                            write_shapefile('{}_{}.shp'.format(cz_id, uid()),
                                            geom, cz_id)
                    else:
                        # Recurse as the polygon is still too big
                        divide_poly(geom, cz_id)

        elif clipped.type is 'Polygon':
            if bbox_area(clipped) < 493000000000:
                # Write a new Shapefile if we have not made a sliver
                if dirty_area(clipped) > 1000000000:
                    write_shapefile('{}_{}.shp'.format(cz_id, uid()),
                                    clipped, cz_id)
            else:
                # Recurse as the polygon is still too big
                divide_poly(clipped, cz_id)

        else:
            print('Odd geometry:', clipped.type)


def runner():
    to_split = ['17_26', '21_9', '25_102_ada76b9b_0625_410d_bde6_824263252ff5',
                '25_102_1e28bc13_e3fe_4a62_8737_636e3312528e',
                '25_44_2aec770e_d59c_43bb_b1a6_6bb27f90f398',
                '25_102_d018e04f_a790_4963_9cfc_3062fe4c8e18',
                '25_102_7518de3a_25c4_4ca3_b736_5ed0e4c79e4e',
                '25_102_5c70f84a_7cc0_49af_a018_c2bcdc9dfcdc',
                '25_102_aa5fd30e_9601_4eeb_abc2_70339496f513',
                '25_102_9eec1bf9_f725_4417_a4e6_9c3bb9970660',
                '25_102_071b7fc2_3a23_4ed0_9a5d_054b3295a75f',
                '25_102_1a23c5b2_7ba1_444f_86ba_63d63dd8f376',
                '25_102_53c5c657_0e1a_4257_bf63_da1f9646c214',
                '25_102_0612589f_1410_46df_aa7c_93a5847f3d53']

    for i, cz in enumerate(to_split, start=1):
        print(i, 'of', len(to_split), 'processed')
        path = ('/Users/stuart/CardiffProject/climate_zones'
                '/singlepart_files_split_rerun/{}.shp').format(cz)

        divide_poly(load_poly(path), get_cz_id(path))

        # Delete original files
        path = path[:-3]
        to_delete = ['shp', 'dbf', 'shx', 'cpg']
        for d in to_delete:
            os.remove(path + d)

runner()
