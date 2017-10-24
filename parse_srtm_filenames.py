import re

with open('srtm_filenames.lst', 'r') as f:
    srtm = f.readlines()

for s in srtm:
    short = s.split('/')[-1].split('.')[0]
    left = short[:3]
    right = short[3:]
