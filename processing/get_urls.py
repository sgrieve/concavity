import json
import sys

with open('/home/ccearie/concavity/processing/download_links.json') as srtm:
    links = json.load(srtm)

for url in links[sys.argv[1]]:
    print(url)
