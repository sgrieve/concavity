import json
import sys

# Load input args, the first is the lower number of tiles and the second is
# the upper number of tiles to include in this array job
lower = int(sys.argv[1])
upper = int(sys.argv[2])


with open('download_links.json') as srtm:
    links = json.load(srtm)

with open('bboxes.json') as bbox:
    bboxes = json.load(bbox)

counts = []
for key, urls in links.items():
    if len(urls) > 0:
        counts.append((key, len(urls)))

# Count the number of files to download for each sub zone
counts.sort(key=lambda tup: tup[1], reverse=True)

# Filter the data by the input args
to_process = [x for x in counts if x[1] > lower and x[1] <= upper]

# Write the required params for each job into a file
with open('array_params_{}_{}.txt'.format(lower, upper), 'w') as f:
    for i, a in enumerate(to_process):
        utm = bboxes[a[0]]['utm_zone']
        f.write('{} {} {} {}\n'.format(str(i).zfill(4),
                                       a[0][:-4], utm[0], utm[1]))