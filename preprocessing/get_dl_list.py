import json
from shapely.geometry.polygon import Polygon


def bounds_to_poly(bbox):
    '''
    Helper function to go from lat and long max and min values to a shapely
    polygon
    '''
    return Polygon(((bbox[1], bbox[3]), (bbox[0], bbox[3]),
                   (bbox[0], bbox[2]), (bbox[1], bbox[2])))

results = {}

base_url = 'https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/SRTM_GL1/'


with open('srtm_coords.json') as srtm:
    srtm_data = json.load(srtm)

with open('../processing/bboxes.json') as cz:
    cz_coords = json.load(cz)

no_of_cz = len(cz_coords) - 1

for i, (cz_filename, cz_data) in enumerate(cz_coords.items()):
    print('Processing', i, 'of', no_of_cz)
    tmp_results = []
    cz_poly = bounds_to_poly(cz_data['bbox'])

    for srtm_filename, srtm_coords in srtm_data.items():
        srtm_poly = Polygon(srtm_coords)
        if srtm_poly.intersects(cz_poly):
            tmp_results.append(base_url + srtm_filename)
    results[cz_filename] = tmp_results


with open('../processing/download_links.json', 'w') as f:
    json.dump(results, f, sort_keys=True, indent=4)
