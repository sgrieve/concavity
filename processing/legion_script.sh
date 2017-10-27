#!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.

# 1. Force bash as the executing shell.
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=0:10:0

# 3. Request 1 gigabyte of RAM
#$ -l mem=1G

# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=1G

# 5. Set the name of the job.
#$ -N serial_LSD_Test_SRTM

# 6. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/ccearie/Scratch/LSD_output

# 7. Your work *must* be done in $TMPDIR
cd $TMPDIR

# 8. Run the application.
/home/ccearie/LSD/LSDTopoTools_ChiMudd2014-master/driver_functions_MuddChi2014/chi_mapping_tool.exe  /home/ccearie/drivers/ Example_ChiTool.driver
