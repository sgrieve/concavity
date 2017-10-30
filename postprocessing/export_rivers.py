import csv
import os
from collections import Counter

input_file = '../TMPDIR/11_21_output_MChiSegmented.csv'
filename = os.path.basename(input_file)
split_name = filename.split('_')

sub_zone = '{}_{}'.format(split_name[0], split_name[1])

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)

    basin_ids = []

    for r in reader:
        basin_ids.append(r[12])

    basin_ids = set(basin_ids)

    basins = {id: [] for id in basin_ids}

    csvfile.seek(0)
    next(reader)

    for row in reader:
        basins[row[12]].append((row[1:5] + row[6:9] + [row[11]]))


# get the main stem ID for each basin in the input file
for basin_key in basins:
    sources = []

    for x in basins[basin_key]:
        sources.append(x[7])

    main_stem = Counter(sources).most_common()[0][0]
    with open('{}_river_{}.csv'.format(sub_zone, main_stem), 'w') as o:
        for data in basins[basin_key][::-1]:
            if data[7] == main_stem:
                o.write(','.join(data) + '\n')
