# Undergraduate Final Year Project
## FYP: Why is my population size so small? Estimating recent effective population sizes from resistance loci in Anopheles gambiae

##### Supervised by: Dr Khatri Bhavin

Code used during my undergraduate final year project, with much previous work done by Anushka Thawani, Theo Sebastian Hemmant and other previous students on this project.

### Data Repository
https://imperiallondon-my.sharepoint.com/:f:/g/personal/cqs21_ic_ac_uk/Egu0jDWKCxNBhjx7cOh0s40B6CMgt4aPcoo4BdXK1RVBag?e=6k6hGw

![alt text](<FYP (5).png>)

### Burn in simulations
completed by me: all burnins run (all finished before termination point 100k ticks)
Theo's burnins: NOTE: wrong calculation method used in calculating heterozygosity [theo's burnins are missing no.24-27]

### Running SLIM simulations via HPC 
- made parameter combination.txt, and job script
- run simulations 


### Post-Simulation Python code
- done with TMRCA code
- TO CHECK: cluster by TMRCA and draw tree with tips coloured for mutations. adapt for figures later



# Current Status: Done with seed 1 simulations
### Update questions:
- confused with the post-simulation check... 
    Plot nucleotide diversity for each simulation and also separately 
    plot number of independent gene loci/origins (L) against population size (N) for each population size?


80% theta /(1+2theta)

### Progress since 19 March:
- burnin array on HPC, made heterozygosity user-defined function + track progress to csv using logfile
- finished TMRCA python calculation code block, simulation array
- did poster

### Planned work this week
- 70kb burnins
- try to run theos and my simulations
- test post simulation check and tmrca/dendrogram on theos vcf file (they are all test files??)
- run 10 simulation arrays for the 10 seeds
- (post-simulation) plot nuc diversity graph for all simulations and compare against expected (has to be 10%<nuc diversity>20%)
- finish methods, intro and abstract by monday




# Answered questions
- how many ticks in a simulation (till 80% fixation for VGSC and 40% for RDL)
- what size of genome  (10kb haplotype from Anusha's report?)
- what kind of mutations do i want to sweep?? VGSC and RDL mutations [initializeMutationType("m1", 0.5, "f", 0.02); // introduced sweep mutation dominance is likely partial ]
- how many repeats of the soft sweep simulations? 
    - as many as I can. at least 10 (is roughly 1/3 error, having 100 repeats is 10% error)
    - just 1 subpopulation
- why do we use the Farthest Point Algorithm in the dendrogram clustering?? Should be average UPGMA algorithm
- can we do our neutral burn in for 10N generations (page 597 of SLIM manual) incase not enough coalescence? record the number of generations first
- issue with calculation compute time: calculate heterozygosity every set timepoint instead of every generation for problematic burn ins
