##By Josh Reynolds, PHD candidate in the Burt Lab

#!/bin/bash

#PBS -N run_pairwise    ###REMOVE ME -  Change this to set the name of your script
#PBS -j oe
#PBS -k oe

#PBS -m ae

#PBS -l walltime=72:00:00	###REMOVE ME - change this to set your time (hh:mm:ss)
#PBS -l select=1:ncpus=4:mem=20gb       ###REMOVE ME - leave select at 1, choose your cpus and memory

## NB values for ncpus and mem are allocated
## to each node (specified by select=N)
##
## to direct output to cwd, use $PBS_O_WORKDIR:
## specify LOGFILE found in ~/ during execution then moved to cwd on job completion
##
cd $PBS_O_WORKDIR
JOBNUM=`echo $PBS_JOBID | sed 's/\..*//'`
LOGFILE=${PBS_JOBNAME}.o${JOBNUM}

#########################################
##                                     ##
## Output some useful job information. ##
##                                     ##
#########################################

echo ------------------------------------------------------
echo -n 'Job is running on node '; cat $PBS_NODEFILE
echo ------------------------------------------------------
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: originating queue is $PBS_O_QUEUE
echo PBS: executing queue is $PBS_QUEUE
echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: execution mode is $PBS_ENVIRONMENT
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: job number is $JOBNUM
echo PBS: logfile is $LOGFILE
echo PBS: node file is $PBS_NODEFILE
echo PBS: current home directory is $PBS_O_HOME
#echo PBS: PATH = $PBS_O_PATH
echo ------------------------------------------------------

## load common modules as standard
##
module load anaconda3/personal vcftools   ### load any modules you need here (e.g. vcftools, ibdseq). To see a list of available modules, use "module avail" on your login node
source activate f2

## command timed to get mem and wallclock info
##

R --vanilla --quiet --slave < ~/f2/scripts/pairwise_dif.R   ### Then supply your command. Either write the code here, or in a separate shell script that you then call on here.

## move LOGFILE to cwd
##
mv $HOME/$LOGFILE $PBS_O_WORKDIR
