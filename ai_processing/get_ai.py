import rasterio
import sys
import os
from glob import glob

zone = sys.argv[1]

filenames = glob('/home/ccearie/Scratch/SRTM/{}/*iver*.csv'.format(zone))

source_path = '/home/ccearie/Scratch/raster/ai.tif'

with rasterio.open(source_path) as src:

    for f in filenames:

        points = []
        ai = []

        with open(f) as read:
            lines = read.readlines()
            for l in lines:
                s = l.split(',')
                points.append([float(s[3]), float(s[2])])

        for val in src.sample(points):
            if val >= 0:
                ai.append(round(val[0], 4))
            else:
                ai.append('NaN')

        outname = '/home/ccearie/Scratch/SRTM_new/{}/{}.csv'.format(zone, os.path.basename(f)[:-4])

        with open(outname, 'w') as w:
            for q in range(len(ai)):
                w.write('{},{}\n'.format(lines[q].strip(), ai[q]))
