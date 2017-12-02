import csv
import os
import sys
from collections import Counter

# Processing the input filename to get the climate zone number and sub number
input_file = sys.argv[1]
filename = os.path.basename(input_file)
sub_zone = filename.split('MChiSegmented')[0][:-1]

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skip the header
    next(reader)

    # Load all of the basin ids from the file
    basin_ids = []
    for r in reader:
        basin_ids.append(r[12])

    # Set will give us a unique set of basin ids with no duplicates
    basin_ids = set(basin_ids)

    # Create a dictionary keyed with basin ids and the values are empty lists
    basins = {id: [] for id in basin_ids}

    # Jump back to the start of the file and skip the header
    csvfile.seek(0)
    next(reader)

    # Select the data we want from the raw file so we have a list of rows of
    # data for each basin.
    for row in reader:
        basins[row[12]].append((row[1:5] + row[6:9] + [row[11]]))


# get the main stem ID for each basin in the input file
for basin_key in basins:
    sources = []

    for x in basins[basin_key]:
        sources.append(x[7])

    # Main stem is the ID of the longest channel in each basin
    main_stem = Counter(sources).most_common()[0][0]

    # Write each main stem's data to its own file
    with open('{}_river_{}.csv'.format(sub_zone, main_stem), 'w') as o:
        for data in basins[basin_key][::-1]:
            if data[7] == main_stem:
                o.write(','.join(data) + '\n')
