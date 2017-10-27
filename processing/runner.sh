#!/bin/bash

# $1 - shapefile name without .shp
# $2 - utm zone
# $3 - north or south

cd /home/ccearie/Scratch/SRTM/

python /home/ccearie/concavity/processing/get_urls.py $1.shp | xargs wget

gdalwarp --config GDAL_CACHEMAX 3000 -wm 3000 -srcnodata -32768 -dstnodata -9999 -cutline /home/ccearie/concavity/climate_zones/singlepart_files/$1.shp -crop_to_cutline -of ENVI *.hgt tmp.bil

gdalwarp -t_srs '+proj=utm +zone='$2' +datum=WGS84 +'$3'' -of ENVI tmp.bil $1.bil

rm tmp.*
rm *.hgt

# Run the LSD code (on legion)
/home/ccearie/LSD/LSDTopoTools_ChiMudd2014-master/driver_functions_MuddChi2014/chi_mapping_tool.exe  /home/ccearie/concavity/processing/ SRTM.driver /home/ccearie/Scratch/SRTM/ $1 /home/ccearie/Scratch/SRTM/ $1
