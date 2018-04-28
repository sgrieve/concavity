import sys
import os
import numpy as np

zone = sys.argv[1]

filename = '/home/ccearie/Scratch/SRTM/{}.csv'.format(zone)

with open(filename, 'r') as f:
    f.readline()
    data = f.readlines()

output_data = []

for d in data:
    river_name = d.split(',')[0]

    with open('/home/ccearie/Scratch/SRTM_new/{}/{}.csv'.format(zone, river_name), 'r') as r:
        river_data = r.readlines()

    ai_data = []
    for riv in river_data:
        ai = riv.split(',')[-1]
        if ai != 'NaN':
            ai_data.append(float(ai))

    avg = np.mean(ai_data)
    std = np.std(ai_data)
    median = np.median(ai_data)
    max = np.max(ai_data)
    min = np.min(ai_data)

    out = '{},{},{},{},{},{}\n'.format(d.strip(), avg, median, std, min, max)
    output_data.append(out)


with open('/home/ccearie/Scratch/SRTM_new/{}.csv'.format(zone), 'w') as write:
    write.write('RiverName,NCI,Relief,FlowLength,TotalSlope,Country,Continent,ai_mean,ai_median,ai_std,ai_min,ai_max\n')

    for x in output_data:
        write.write(x)
