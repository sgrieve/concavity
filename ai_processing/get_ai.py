import rasterio
import os
from glob import glob

filenames = glob('../Results/Af/*iver*.csv')

source_path = 'processed_data/ai.tif'

with rasterio.open(source_path) as src:

    for i, f in enumerate(filenames):
        
        points = []
        ai = []

        with open(f) as read:
            lines = read.readlines()
            for l in lines:
                s = l.split(',')
                points.append([float(s[3]), float(s[2])])

        for val in src.sample(points):
            if val >= 0:
                ai.append(val[0])
            else:
                ai.append('NaN')

        outname = 'outputs/Af/' + os.path.basename(f)[:-4] + '_new.csv'
        with open(outname, 'w') as w:
            for q in range(len(ai)):
                w.write('{},{}\n'.format(lines[q].strip(), ai[q]))
