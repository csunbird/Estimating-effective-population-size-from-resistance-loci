#!/bin/bash

#PBS -N run_cheyanne_simulation_array
#PBS -j oe
#PBS -k oe

#PBS -m ae

#PBS -l walltime=48:00:00
#PBS -l select=1:ncpus=8:mem=2gb      

#PBS -J 1-10

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
module load anaconda3/personal  
source activate slim

## command timed to get mem and wallclock info
##


input="parameter_combinations.txt"

## Get the row number based on PBS_ARRAY_INDEX environment variable
array_index=$PBS_ARRAY_INDEX

## Read the specified row from the parameter combinations file
params=$(sed -n "${array_index}p" "$input")

## Split the row into individual parameters
IFS=',' read -r -a params_array <<< "$params"

## Extract parameters and process them
counter=0
for param in "${params_array[@]}"
do
    ((counter++))
    echo "Processing element ${counter}: ${param}"
    ## Run your SLIM script with the parameters here
    slim -d seed=$PBS_ARRAY_INDEX  ~/simulations/sweep simulation.txt
done

## move LOGFILE to cwd
##
mv $HOME/$LOGFILE $PBS_O_WORKDIR
