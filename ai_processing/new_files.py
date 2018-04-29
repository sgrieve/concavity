import sys
import os
import numpy as np

zone = sys.argv[1]

filename = '/home/ccearie/Scratch/SRTM/{}.csv'.format(zone)

with open(filename, 'r') as f:
    f.readline()
    data = f.readlines()

output_data = []

count = 0

for d in data:
    river_name = d.split(',')[0]

    with open('/home/ccearie/Scratch/SRTM_new/{}/{}.csv'.format(zone, river_name), 'r') as r:
        river_data = r.readlines()

    ai_data = []
    for riv in river_data:
        ai = riv.split(',')[-1].strip()
        if ai != 'NaN':
            ai_data.append(float(ai))

    if ai_data:
        avg = np.mean(ai_data)
        std = np.std(ai_data)
        median = np.median(ai_data)
        max = np.max(ai_data)
        min = np.min(ai_data)
        n = len(ai_data)
    else:
        count += 1
        avg = 'NaN'
        std = 'NaN'
        median = 'NaN'
        max = 'NaN'
        min = 'NaN'
        n = 0

    out = '{},{},{},{},{},{},{}\n'.format(d.strip(), avg, median,
                                          std, min, max, n)
    output_data.append(out)


with open('/home/ccearie/Scratch/SRTM_new/{}.csv'.format(zone), 'w') as write:
    write.write('RiverName,NCI,Relief,FlowLength,TotalSlope,Country,Continent,ai_mean,ai_median,ai_std,ai_min,ai_max,ai_n\n')

    for x in output_data:
        write.write(x)

with open('/home/ccearie/Scratch/SRTM_new/{}_log.txt'.format(zone), 'w') as log:
    log.write('{} has {} rivers with no AI values.'.format(zone, count))
