#!/bin/bash

# $1 - shapefile name without .shp
# $2 - utm zone
# $3 - north or south

# Set up paths so we have a folder for each sub zone
cd /home/ccearie/Scratch/SRTM/
mkdir $1
cd $1

# Download the tiles we need
python /home/ccearie/concavity/processing/get_urls.py $1.shp | xargs -n 1 -P 8 wget -nv

# Build virtual raster from tiles
gdalbuildvrt input.vrt *.hgt

# Clip the merged raster using the corresponding shapefile
gdalwarp -multi -wo 'NUM_THREADS=val/ALL_CPUS' -srcnodata -32768 -dstnodata -9999 -cutline /home/ccearie/concavity/climate_zones/singlepart_files_split_rerun/$1.shp -crop_to_cutline -of ENVI input.vrt tmp.bil

# Reproject the clipped raster to utm and save as a floating point file
gdalwarp -t_srs '+proj=utm +zone='$2' +datum=WGS84 +'$3'' -of ENVI -ot Float32 tmp.bil $1.bil

# Tidy up some temp files
rm tmp.*
rm *.hgt
rm *.vrt

# Run the LSD code (on legion)
/home/ccearie/LSD/LSDTopoTools_ChiMudd2014-master/driver_functions_MuddChi2014/chi_mapping_tool.exe /home/ccearie/concavity/processing/ SRTM.driver /home/ccearie/Scratch/SRTM/$1/ $1 /home/ccearie/Scratch/SRTM/$1/ $1

# Extract the rivers from the output data
python /home/ccearie/concavity/postprocessing/export_rivers.py $1_MChiSegmented.csv

# Remove the raster files
rm $1.bil
rm $1.hdr
rm $1.bil.aux.xml
