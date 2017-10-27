import json

with open('srtm_filenames.lst', 'r') as f:
    srtm = f.readlines()

results = {}

for s in srtm:
    short = s.split('/')[-1].split('.')[0]
    left = short[:3]
    right = short[3:]

    if left.startswith('N'):
        left = float(left[1:])
    elif left.startswith('S'):
        left = float(left[1:]) * -1

    if right.startswith('E'):
        right = float(right[1:])
    elif right.startswith('W'):
        right = float(right[1:]) * -1

    # get the 4 points, clockwise from bottom left (lat, long)
    p1 = (left, right)
    p2 = (left + 1, right)
    p3 = (left + 1, right + 1)
    p4 = (left, right + 1)

    results[s.strip()] = (p1, p2, p3, p4)

with open('srtm_coords.json', 'w') as f:
    json.dump(results, f, sort_keys=True, indent=4)
