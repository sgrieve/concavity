# Global River Concavity

This project aims to perform an analysis of global rivers using the SRTM 30 dataset and the LSDTopoTools package. The code presented here could be adapted to other projects which require the bulk downloading and processing of SRTM data based on polygon areas of interest.

This workflow has been designed to run on the UCL Legion supercomputer so some modification of the scripts will most likely be needed if this is to be run in a different environment.

The original project plan for this project can be found in `ProjectPlan/` in both markdown and pdf formats.

## Directory Structure

This section provides an overview of the files contained within this repository and how to use them.

#### `climate_zones/`

The files within this directory are generated using some of the preprocessing scripts. The initial input data, taken from [this paper](Koppen link) is provided as a `geotiff`. This raster is split into a series shapefiles, which are subdivided until each climate sub zone is small enough to be processed in a sane amount of time and with a sane amount of memory. The final files which should be used are contained within `singlepart_files_split/`, the other folders contain intermediate data which is preserved for debugging purposes.

#### `preprocessing/`

`srtm_filenames.lst` is the list of every SRTM 30 tile stored on the OpenTopography servers.

`reclassify.py` is used to reclassify the input Koppen climate zone raster to merge the similar climate zones to produce a final file which can be used for the rest of the preprocessing. This resultant final file is stored in `climate_zones/`.

`multi_to_single.py` Following the conversion of the reclassified climate zone raster to a polygon shapefile using QGIS, this script is used to break each multipart polygon geometry into a singlepart polygon geometry, needed so that we can create a single tile for each contiguous climate sub zone without having to nest attribute queries within GDAL commands.

`quadpoly.py` Script to use a quadtree-like algorithm to divide large climate sub zones into smaller chunks, to cut down on processing time on Legion. This script is hard coded with a list of the climate sub zones which need to be split and an approximate maximum size of polygon to be processed in one step. This second value will need tweaked based on the compute power available.

`parse_srtm_filenames.py` This script processes the list of SRTM tiles into a json file, `srtm_coords.json`, which stores the corner coordinates of each SRTM tile, keyed with the filename of the tile on the OpenTopography server.

`get_bbox.py` This script identifies the bounding box coordinates, the UTM zone and if the bottom left corner of the bounding box is in the Northern or Southern hemisphere for each shapefile generated using `quadpoly.py`. The results are stored in `../processing/bboxes.json`.

`get_dl_list.py` The final preprocessing script, this loads the bounding box of each shapefile from `../processing/bboxes.json` and calculates all of the SRTM tiles which intersect this bounding box. From this intersection a json containing a list of download urls, keyed by the climate sub zone name is written to `../processing/download_links.json`.

#### `processing/`

`get_urls.py` Simple command line script to return a list of the download urls for a given input climate sub zone filename.

`runner.sh` Main script which handles the download, merging, clipping and reprojection of the SRTM tiles, runs the file through the LSD code and postprocesses the outputs. Takes three input arguments:

```
$1 - shapefile name without .shp
$2 - utm zone
$3 - north or south
```

`legion_script.sh` Example legion script used to deploy a single instance of `runner.sh`.

`build_array_params.py` Use this script to generate a file containing the matrix of parameters needed to deploy an array job. Takes 2 input arguments, the minimum and maximum number of SRTM tiles to be included in the job. This allows multiple array jobs to be created with different memory requirements.

`legion_array_job.sh` Example legion script used to deploy an array job composed of multiple instances of `runner.sh`.

`SRTM.driver` parameter file for the LSD code. Write path will need to be configured for the user who is running the code, and the other parameters are documented in the [LSDTopoTools User Guide](LSDTopoTools book).

#### `LSD_code/`

This project lightly modifies the LSDTopoTools `chi_mapping_tool` to generate the required output data from the clipped SRTM tiles. This driver can be used with any recent LSDTopoTools distribution. If you need guidance on getting started with LSDTopoTools, see [this user guide](LSD book link).

#### `postprocessing/`

Following the execution of the LSD code, `export_rivers.py` is used to identify the longest river in each drainage basin and export it to its own `csv` file.

`concavity.py` is the new visualisation script for these output river files. It is an optimized port of the original `concavity.m` script described above and can be used at the command line as follows:

```
$ python concavity.py <output_filename> <list of river filenames>
```

Which will write the average concavity statistics to the screen and save a figure, named using the supplied output filename,  containing boxplots of all of the input rivers.

#### `matlab_code/`

This directory contains the original matlab analysis code (`Concavity.m`) used to calculate and plot river concavity data alongside the example input data (`Af_distance.txt` and `Af_elevation.txt`) provided at the start of the project.

`python_port.py` is a straight port of the matlab code to python, which runs on the same input data and produces identical outputs.

`data_to_matlab_fmt.py` is a script to take output data from the LSD code and reformat it into the structure needed to be loaded by the original matlab code or its python port. It is only used for debugging.


## Workflow

This section outlines the steps required to go from the Koppen climate zone raster to the final processed files, via a series of preprocessing steps, an automated processing workflow and some postprocessing.


#### 1. Climate Zone Processing

1. Download [Koppen Climate Zone dataset](koppen link)
1. `reclassify.py`
1. Use QGIS to convert reclassified raster to polygon
1. `multi_to_single.py`
1. `quadpoly.py`

#### 2. SRTM Tile Processing

1. Download SRTM filenames from OpenTopography
1. `parse_srtm_filenames.py`
1. `get_bbox.py`
1. `get_dl_list.py`

#### 3. HPC Processing

For a single job:
1. `legion_script.sh`

For an array job:
1. `build_array_params.py`
2. `legion_array_job.sh`

#### 4. Result Visualisation

1. `concavity.py`


## Naming Conventions

The Koppen climate zones are described by letter codes in the original paper. We have merged some of the similar zones to allow us to identify more general trends in the data to emerge.

This table contains the mappings between the letter codes used in the paper and our numerical codes.

**table here**

As the climate zones are not contiguous, we need to be able to split each climate zone into a series of individual polygons, to achieve this, a sub zone ID is added to each climate zone so that the 5th polygon of zone 4 would be referred to as `4_5`. Not that no information is contained within these sub zone IDs, we cannot assume any spatial relationship between sub zones based on their numerical value.

In some cases the sub zones are still too big to be processed efficiently. These are further divided using a quadtree-like algorithm. In order to ensure files are never overwritten whilst running this recursive algorithm, the output subsets of a given climate sub zone are given an additional unique id: `4_5_a6a60415-78a8-4ed7-8f74-f9fbfceb09f5`. Again, these additional IDs confer no other information and serve solely to ensure the uniqueness of each climate sub zone.
