1. Convert the climate zone raster to shapefile
2. Generalize the shapefile and remove any small areas below a threshold area
3. Break each climate zone out into its own multipart polygon
4. Divide each multipart polygon into individual polygon files so that we have a series of discrete climate zone polygons
5. Cycle through each polygon and extract it's bounding box in lat/long
6. Download the SRTM tiles that correspond to this bounding box and merge them into a single file, using GDAL
7. Clip the SRTM DEM to the outline of the given climate zone polygon
8. Reproject the clipped DEM to UTM and convert to ENVI BIL format ready for LSDTopoTools
9. Run the chi_mapping_tool code on the DEM
10. Post-process the csv files to get the longest channel in each basin and strip out the data we are interested in
11. Run the matlab script to get the concavity indexes for each river in each climate zone
