import json

# load all of the srtm coords and loop thru the key value pairs
# for each coord, test if the point is within the cz polygon
# if it is, store the dict key in a new list of tiles to dl
# write this list to an output dict where the key is the cz filename

# if this is horrifyingly slow (it will be), it can be run on an as needed
# basis for each file to be processed rather than all at once, but it might
# be worth just running this step on legion

from shapely.geometry.polygon import Polygon

polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
poly2 = Polygon([(0, 0), (0, 1), (-1, 1), (-1, 0)])
print(polygon.intersects(poly2))
