import sys
import os
from scipy import stats
import numpy as np

# We collect each file's data into a list of arrays
offset_elevs = []
median_norm_offsets = []

# The first input argument is the name of the output figure, without extension
output_filename = sys.argv[1]

# Store the output strings as a list, where the first item is a header
output = ['RiverName,NCI,Relief,FlowLength,TotalSlope\n']

# Get the list of files to be processed from the second command line arg
processing_path = sys.argv[2]
file_list = os.listdir(processing_path)

# Make sure we only process the river files
final_file_list = []
for f in file_list:
    if 'river' in f:
        final_file_list.append(os.path.join(processing_path, f))

# Cycle through every river file in our list and get the metrics.
for i, filename in enumerate(final_file_list, start=1):
    print(i, 'of', len(final_file_list))

    data = np.genfromtxt(filename, delimiter=',')

    A = data[:, 5]  # FlowLength
    B = data[:, 4]  # Elevation

    # Cant use np.ptp as it doesnt handle nans
    R = np.nanmax(B) - np.nanmin(B)
    FlowLength = np.nanmax(A) - np.nanmin(A)

    # where x1,y1 x2,y2 are the long profile endpoints
    x = [A[0], np.nanmax(A)]
    y = [B[0], np.nanmax(B)]

    result = stats.linregress(x, y)

    # Unpack the slope and intercept from the result of the linregress function
    m = result[0]
    b = result[1]

    Y = m * A + b  # Y values on the line
    offset_elev = (B - Y) / R

    # Add the results to out list of results
    offset_elevs.append(offset_elev)
    NCI = np.nanmedian(offset_elev)

    # Also need the total river length, river relief, river slope and name
    river_name = os.path.splitext(os.path.basename(filename))[0]

    output.append('{},{},{},{},{}\n'.format(river_name, NCI, R,
                                            FlowLength, R / FlowLength))


with open('{}.csv'.format(output_filename), 'w') as f:
    for o in output:
        f.write(o)
