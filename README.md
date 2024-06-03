# Undergraduate Final Year Project
## FYP: Why is my population size so small? Estimating recent effective population sizes from resistance loci in Anopheles gambiae

##### Supervised by: Dr Khatri Bhavin

Code used during my undergraduate final year project, with much previous work done by Anushka Thawani, Theo Sebastian Hemmant and other previous students on this project.

### Data Repository for Theos code and data which was too big
I need to figure out how to port to github. 
https://imperiallondon-my.sharepoint.com/:f:/g/personal/cqs21_ic_ac_uk/Egu0jDWKCxNBhjx7cOh0s40B6CMgt4aPcoo4BdXK1RVBag?e=6k6hGw


![alt text](image-2.png)

Anusha --> Theo --> Cheyanne --> future
good luck! jiayou! atb! help! 

### Burn in simulations
- all burnins run (change to 70kb, some other good changes I think)
Theo's burnins: NOTE: wrong calculation method used in calculating heterozygosity [theo's burnins are missing no.24-27?]

### Running SLIM simulations
- optimised! the whole burnin and simulations! much faster!

### Post-Simulation Python code
- done with TMRCA code, postsimulation check/graph code
- TO CHECK: clustering by TMRCA and dendrograms... check if the problem with Theo's dendrograms have been fixed. adapt for figures later



# Current Status: 
### Update questions for Bhavin:
-  Plot nucleotide diversity for each simulation and also separately ?
- plot number of independent gene loci/origins (L) against population size (N) for each population size?


### Progress from previous FYP:
- 70kb burnins (previously 10kb which is ...??not reflective of vgsc size)
- burnin array on HPC, 
- made heterozygosity user-defined function + calculate allele_freq function and also tracking lineages function for and in SLiM. (lawless land??)
- added track progress to csv using logfile so easy to plot graphs after burnins/simulation (lawless land before this????)
- wrote array job workflows for simulations, burnins (previously a lawless land of ??? a bajillion scripts and a lot of different slim????!)
- 10 simulation arrays for the 10 seeds
- (post-simulation) plot nuc diversity graph for all simulations and compare against expected (has to be 10%<nuc diversity>20%)
- wrote array job to run the TMRCA calculations, clustering, dendrogram but ran out of time to finish troubleshooting/ HPC died and kept dying throughout May. tuff luck.
- finished TMRCA python calculation code block, mighT have solved Theos dendrogram clustering problem but ran out of time to check (HPC why a 3 day wait time? why? )

- caught some problems, created some problems. win some lose some i guess ;/ 
- ps. I started this github bc the previous students did a ton of useful things but inheriting this project was confusing. good luck future students. hope this is understandable.



# Answered questions from supervisor meetings
- how many ticks in a simulation (till 80% fixation for VGSC and 40% for RDL)
- what size of genome  (10kb haplotype from Anusha's report?)
- what kind of mutations do i want to sweep?? VGSC and RDL mutations [initializeMutationType("m1", 0.5, "f", 0.02); // introduced sweep mutation dominance is likely partial ]
- how many repeats of the soft sweep simulations? 
    - as many as I can. at least 10 (is roughly 1/3 error, having 100 repeats is 10% error)
    - just 1 subpopulation
- why do previous FYP students use Farthest Point Algorithm in the dendrogram clustering?? Should be average UPGMA algorithm.
- can we do our neutral burn in for 10N generations (page 597 of SLIM manual) incase not enough coalescence? record the number of generations first
- issue with new calculation compute time: calculate heterozygosity every set timepoint instead of every generation for problematic burn ins
