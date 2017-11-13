# Global River Concavity

This project aims to perform an analysis of global rivers using the SRTM 30 dataset and the LSDTopoTools package. The code presented here could be adapted to other projects which require the bulk downloading and processing of SRTM data based on polygon areas of interest.

This workflow has been designed to run on the UCL Legion supercomputer so some modification of the scripts will most likely be needed if this is to be run in a different environment.

The original project plan for this project can be found in `ProjectPlan/` in both markdown and pdf formats.

## Directory Structure

This section provides an overview of the files contained within this repository.

#### `climate_zones/`

The files within this directory are generated using some of the preprocessing scripts. The initial input data, taken from [this paper](koppen link) is provided as a `geotiff`. This raster is split into a series


## Workflow

This section works through the steps required to go from the koppen climate zone raster to the final processed files, via a series of preprocessing steps, an automated processing workflow and some postprocessing.


## LSDTopoTools

This project lightly modifies the LSDTopoTools `chi_mapping_tool` to generate the required output data from the clipped SRTM tiles. This driver can be used with any recent LSDTopoTools distribution. If you need guidance on getting started with LSDTopoTools, see [this user guide](LSD book link).

## Naming Convention

The koppen climate zones are described by letter codes in the original paper. We have merged some of the similar zones to allow us to identify more general trends in the data to emerge.

This table contains the mappings between the letter codes used in the paper and our numerical codes.

**table here**

As the climate zones are not contiguous, we need to be able to split each climate zone into a series of individual polygons, to achieve this, a sub zone ID is added to each climate zone so that the 5th polygon of zone 4 would be referred to as `4_5`. Not that no information is contained within these sub zone IDs, we cannot assume any spatial relationship between sub zones based on their numerical value.

In some cases the sub zones are still too big to be processed efficiently. These are further divided using a quadtree-like algorithm. In order to ensure files are never overwritten whilst running this recursive algorithm, the output subsets of a given climate sub zone are given an additional unique id: `4_5_a6a60415-78a8-4ed7-8f74-f9fbfceb09f5`. Again, these additional IDs confer no other information and serve solely to ensure the uniqueness of each climate sub zone.
