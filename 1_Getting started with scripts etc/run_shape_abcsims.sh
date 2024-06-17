#!/bin/bash

#PBS -N run_msprime_shapeabc
#PBS -j oe
#PBS -k oe

#PBS -J 1-500

#PBS -m ae

#PBS -l walltime=72:00:00
#PBS -l select=1:ncpus=1:mem=30gb

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
source activate msprime

## command timed to get mem and wallclock info
##
### pop size, n*n grid size, migration rate, number of samples, size of anc pop, time of anc pop, length of genome
m=30
n=20
mig_rate=$(sed "${PBS_ARRAY_INDEX}q;d" ./next_params.txt | cut -f1)
pop_size=$(sed "${PBS_ARRAY_INDEX}q;d" ./next_params.txt | cut -f2)
emptypops=$(wc -l ./outside_pops_irreg.txt | awk '{print $1}')
pops=$(((m*n)-emptypops))
anc_size=$((pops*pop_size))
#nsamp=10

## Simulate
/usr/bin/time -v \
python ~/mig/scripts/abc/2d_sims_triangular_realshape.py $pop_size $m $n $mig_rate $anc_size 10000 1000000

## Set variable from sim parameters
#sim="tree_triangular${pop_size}_${ndeme}_${mig_rate}__${anc_size}_10000_1000000"

## Mutate tree
#~/mig/scripts/abc/mutate_job.py ~/ephemeral/abc/second/$sim.ts 456 $ndeme $nsamp $anc_size

## Convert to VCF
#tskit vcf ~/ephemeral/abc/second/$sim.ts_mutated.ts > ~/ephemeral/$sim.vcf

## Change conda environments
#source deactivate
#source activate f2

## Perform haplosetup
#/usr/bin/time -v \
#/rds/general/user/jjr18/home/mig/scripts/abc/sim_haplo_setup.sh $sim /rds/general/user/jjr18/home/ephemeral/$sim.vcf 1000000 $ndeme $nsamp

## move LOGFILE to cwd
##
mv $HOME/$LOGFILE $PBS_O_WORKDIR
