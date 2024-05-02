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







- how many ticks in a simulation (till 80% fixation for VGSC and 40% for RDL)
- what size of genome  (10kb haplotype from Anusha's report?)
- what kind of mutations do i want to sweep?? VGSC and RDL mutations

- how many repeats of the soft sweep simulations? as many as I can. at least 10 (is roughly 1/3 error, having 100 repeats is 10% error)
    - just 1 subpopulation

# Current Status
### Update questions:
- why do we use the Farthest Point Algorithm in the dendrogram clustering?? Should be average UPGMA algorithm
- can we do our neutral burn in for 10N generations (page 597 of SLIM manual) incase not enough coalescence? record the number of generations first
- calculate heterozygosity every set timepoint instead of every generation
- contact hpc

### Progress since last update meeting (19 March):
- Redoing Theo's work, fixed Theo's Burn in SLIM code
- 20 burn ins done on HPC
- struggling to finish burn in 19-24, 10-12... keeps timing out because of pop size and heterozygosity calculation i think

- edited SLIM simulation to have VGSC mutation parameters, introduced sweep, fixed up array simulation script+slim

- finished TMRCA python calculation code block

- did poster

### Planned work
- finish burnins
- fix and run simulation array
- begin report
