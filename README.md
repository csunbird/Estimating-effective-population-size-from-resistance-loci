# Undergraduate Final Year Project
## FYP: Why is my population size so small? Estimating recent effective population sizes from resistance loci in Anopheles gambiae

##### Supervised by: Dr Khatri Bhavin

Code used during my undergraduate final year project, with much previous work done by Anushka Thawani, Theo Sebastian Hemmant and other previous students on this project.

![alt text](image.png)

### Burn in simulations
SLIM Burn in Code but NO simulated burn in populations from previous students

### Running SLIM simulations via HPC 
- made parameter combination.txt, and draft job script
- TO DO: currently drafting python script (slim code)


### Python code
- almost done with TMRCA code
- TO DO: cluster by TMRCA and draw tree with tips coloured for mutations. adapt for figures later


### Haplotype graph tests
- Work done by TSH11, Anusha and previous students
- TO DO: Add my own calculated graphs etc


# Current Status
### Update questions:
- contact HPC (drop in on Tuesdays 2-6pm only)


### Progress since 19 March:
- 18 burn ins done on HPC, made heterozygosity user-defined function + track progress to csv using logfile
completed by me: 1-9, 13-18, 25-27
replaced by Theo's burnins: 10-12, 19-23 (NOTE: wrong calculation method used in calculating heterozygosity)
missing: burn in 24

- struggling to finish burn in 19-24, 10-12... keeps timing out because of pop size and heterozygosity calculation i think
- finished TMRCA python calculation code block, simulation array and trialled it.
- did poster

### Planned work this week
- finish burnins! (trial running calc at timepoints 2/5/24) (8.5 hr to reach gen 40k)
- change sweep site nonsense in simulation SLIM script (done)
- fix and run simulation array with theos burn ins to fill gaps (sunday after burnins are done)
- (post-simulation) plot nuc diversity graph for all simulations and compare against expected (has to be 10%<nuc diversity>20%)
- begin report writing
- HPC drop in to figure out why output file stops outputting after 1000 generations (book 48hr before tuesday)


# Optimising HPC work
- burn in trial 1, data seems to show calcPairHeterozygosity plateaus about 0.0002... may never reach 10% heterozygosity? 
- took 8.5 hr to reach gen 40k and terminate (achieved optimisation!)
![alt text](image-1.png)

- trial 2 using logfile taking the incorrect heterozygosity measure every 1000 gen, and also increase the expiry point from 40k to 100k gen to see if there is indeed a plateau. removed a lot of savepoints as now we know the burnin can finish under 72 hr.
- now can redo all the burnins to standardise at 100k gen if it doesnt terminate earlier

# Answered questions
- how many ticks in a simulation (till 80% fixation for VGSC and 40% for RDL)
- what size of genome  (10kb haplotype from Anusha's report?)
- what kind of mutations do i want to sweep?? VGSC and RDL mutations [initializeMutationType("m1", 0.5, "f", 0.02); // introduced sweep mutation dominance is likely partial ]
- how many repeats of the soft sweep simulations? as many as I can. at least 10 (is roughly 1/3 error, having 100 repeats is 10% error)
    - just 1 subpopulation
- why do we use the Farthest Point Algorithm in the dendrogram clustering?? Should be average UPGMA algorithm
- can we do our neutral burn in for 10N generations (page 597 of SLIM manual) incase not enough coalescence? record the number of generations first
- calculate heterozygosity every set timepoint instead of every generation for problematic burn ins
