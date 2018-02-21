#!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.

# Use paid nodes designated to RSDG so we can skip waiting in the queue
#$ -P RCSoftDev

module load python
module load perl
module load hdf/5-1.8.15/gnu-4.9.2
module load netcdf/4.3.3.1/gnu-4.9.2
module load gdal

# 1. Force bash as the executing shell.
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=1:00:0

# 3. Request 1 gigabyte of RAM
#$ -l mem=64G

# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=100G

# 5. Set up the job array.  In this instance we have requested 1000 tasks
# numbered 1 to 1000.
#$ -t 1-174

# 5. Set the name of the job.
#$ -N srtm_1

# 6. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/ccearie/Scratch/SRTM

# 7. Your work *must* be done in $TMPDIR
cd $TMPDIR

# 8. Parse parameter file to get variables.
number=$SGE_TASK_ID
paramfile=/home/ccearie/concavity/processing/array_params_0_1.txt

index=`sed -n ${number}p $paramfile | awk '{print $1}'`
variable1=`sed -n ${number}p $paramfile | awk '{print $2}'`
variable2=`sed -n ${number}p $paramfile | awk '{print $3}'`
variable3=`sed -n ${number}p $paramfile | awk '{print $4}'`

# 8. Run the application.
sh /home/ccearie/concavity/processing/runner.sh $variable1 $variable2 $variable3
