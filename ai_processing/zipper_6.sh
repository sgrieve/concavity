#!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.

# Use paid nodes designated to RSDG so we can skip waiting in the queue
#$ -P RCSoftDev

# 1. Force bash as the executing shell.
#$ -S /bin/bash

# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=12:00:0

# 3. Request 1 gigabyte of RAM
#$ -l mem=128G

# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
#$ -l tmpfs=100G

# 5. Set the name of the job.
#$ -N bwk_zipping

# 6. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
#$ -wd /home/ccearie/Scratch/SRTM

# 7. Your work *must* be done in $TMPDIR
cd $TMPDIR

# 8. Run the application.
zip /home/ccearie/Scratch/bwk.zip -r -q -0 /home/ccearie/Scratch/SRTM_new/BWk/*
