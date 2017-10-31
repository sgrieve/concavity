#!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.

module load python
module load perl
module load hdf/5-1.8.15/gnu-4.9.2
module load netcdf/4.3.3.1/gnu-4.9.2
module load gdal

# 1. Force bash as the executing shell.
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=4:00:0

# 3. Request 1 gigabyte of RAM
#$ -l mem=256G

# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=60G

# 5. Set the name of the job.
#$ -N serial_LSD_Test_SRTM

# 6. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/ccearie/Scratch/SRTM

# 7. Your work *must* be done in $TMPDIR
cd $TMPDIR

# 8. Run the application.
sh /home/ccearie/concavity/processing/runner.sh 11_21 48 north
