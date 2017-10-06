# Global River Concavity

## Overview

This project aims to perform an analysis of global rivers using the SRTM 30 dataset and the LSDTopoTools package.

## Project Plan

The technical aspects of the project can be divided into 5 stages:

#### Climate zone processing (0.5 day)

1. Convert the climate zone raster to shapefile
2. Generalize the shapefile and remove any small areas below a threshold area
3. Break each climate zone out into its own multipart polygon
4. Divide each multipart polygon into individual polygon files so that we have a series of discrete climate zone polygons

#### SRTM Download (1.5 days)

5. Write a script to cycle through each climate zone polygon and extract it's bounding box in lat/long
6. Write script to automate the download the SRTM tiles that correspond to each bounding box
7. Merge the downloaded STRM tiles into a single file, using GDAL

#### SRTM Processing (1.5 day)

7. Clip the SRTM DEM to the outline of the given climate zone polygon
8. Reproject the clipped DEM to UTM and convert to ENVI BIL format ready for LSDTopoTools

#### River Analysis (1 day)

1. Compile LSDTopoTools on the Legion supercomputer
1. Modify the `chi_mapping_tool` to run efficiently on these datasets
9. Run the `chi_mapping_tool` code on each climate zone DEM

#### Post processing (0.5 day)

10. Post-process the output csv files to get the longest channel in each basin and strip out the data we are interested in
10. Modify the matlab script to load the new data files
11. Run the matlab script to get the concavity indexes for each river in each climate zone

The time estimates are not set in stone, but represent the approximate amount of time it will take to complete each stage. As discussed previously the final stage may be performed by Andrew under our supervision if other parts of the project over-run.

The river analysis section is estimated as a day of effort: this represents the time to write the code and set the automated process to run on the Legion Supercomputer. The actual time for this stage to complete could be longer, due to processing time and job queuing on Legion, which we have no control over. This additional time is not billed, but must be considered when deciding on a delivery date.

## Science Questions

In the configuration of the software and the planning of the project a number of questions need to be resolved before proceeding:

- What threshold area do we use for the channel extraction?
- Below what threshold area do we want to exclude climate zones from analysis?
- Do we only want the longest river in each basin?
- Do we want to exclude rivers that cross boundaries?

## Data Requirements

The two datasets required for this project are:

- Climate zone raster
- Global SRTM data

We have the climate zone raster, and can download small tiles of SRTM data from a web interface, but do not have a way at present of automating the download process.

The total amount of SRTM data is ~100 GB. It is likely that we will not download all of the data at once and so the amount that UCL's supercomputer Legion provides (200 GB of scratch storage and 50 GB of backed up storage) should be sufficient for this analysis.

If there is a desire to store a tiled, global SRTM dataset for future projects, a location to store this data will need to be found on either Cardiff or Bristol's servers.

## Technical Challenges

- Downloading the SRTM data automatically
- Large DEMs may be too big to join, project and process. To solve this we may need to tile the largest climate zones
- Ensuring that the coordinate projections used for all the files are consistent and we use an equal-area projection eg UTM for the DEM input to LSDTopoTools, otherwise the data will be meaningless.

The biggest challenge is the automated downloading of the data, not in the downloading itself, but in getting access to a service where we can automate the downloading of large areas at once. A contingency plan would be to work on the SRTM 90 data which is available from a public FTP service (https://dds.cr.usgs.gov/srtm/) but is at a lower resolution and will not resolve as much detail as the newer 30m product.

The other main technical challenge will be in the projection and conversion of the data to run in the LSDTopoTools format. This may take some experimentation and trial and error, but SRTM data has been used many times in LSDTopoTools in the past, so there is documentation of this process available.

It is possible that even on the Legion Supercomputer we may come up against memory limits when processing some of the larger climate zone DEMs. If this happens we will discuss how best to tile the data in a scientifically meaningful way.

## Outcomes

The result of this project will be a series of `csv` files sampled on a per-pixel basis for each river in each climate zone identified in the Koppen dataset, ready to be processed by the a modified version of the existing Matlab processing script.

So there will be a directory structure as follows:

```
+-- zone_Af/
|   +-- af_river_1.csv
|   +-- af_river_2.csv
|   +-- af_river_3.csv
|   +-- af_river_4.csv
+-- zone_BSk/
|   +-- BSk_river_1.csv
|   +-- BSk_river_2.csv
|   +-- BSk_river_3.csv
|   +-- BSk_river_4.csv
```

and the `csv` files will have the following headers:

`X`,`Y`,`Latitude`,`Longitude`,`Elevation`,`Flow_Distance`, `Drainage_Area`, `Source_Key`, `Basin_key`
