import csv
import os
import sys
from collections import Counter


def koppen_number_to_string(filename):
    '''
    Helper function to convert a filename with a numerical koppen code into
    a string koppen code, using the dictionary below.
    '''
    koppen = {'1': 'Af', '2': 'Am', '3': 'Aw', '4': 'BWh', '5': 'BWk',
              '6': 'BSh', '7': 'BSk', '8': 'Cs', '11': 'Cw', '14': 'Cf',
              '17': 'Ds', '21': 'Dw', '25': 'Df'}

    split_sub_zone = filename.split('_')
    koppen_zone = koppen[split_sub_zone[0]]
    return koppen_zone + '_' + '_'.join(split_sub_zone[1:])

localpath = '/Users/stuart/CardiffProject/raw_files/{}/'.format(sys.argv[1])
file_list = os.listdir(localpath)

for i, input_file in enumerate(file_list, start=1):
    print(i, 'of', len(file_list))

    filename = os.path.basename(input_file)
    sub_zone = filename.split('MChiSegmented')[0][:-1]

    # We want to convert back from the numerical climate zone codes to strings
    sub_zone = koppen_number_to_string(sub_zone)

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

        # Create a dict keyed with basin ids and the values are empty lists
        basins = {id: [] for id in basin_ids}

        # Jump back to the start of the file and skip the header
        csvfile.seek(0)
        next(reader)

        # Select the data we want from the raw file so we have a list of rows
        # of data for each basin.
        for row in reader:
            basins[row[12]].append((row[1:5] + row[6:9] + [row[11]]))

    # Get the main stem ID for each basin in the input file
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

    # Rename the MChiSegmented file to a more descriptive name
    new_input_name = input_file.replace('MChiSegmented', 'RawBasins')
    new_input_name = koppen_number_to_string(new_input_name)

    os.rename(input_file, new_input_name)
