# FYP: Why is my population size so small? Estimating recent effective population sizes from resistance loci in Anopheles gambiae
# Supervised by: Dr Khatri Bhavin
## Undergraduate Final Year Project
Code used during my undergraduate final year project, with much previous work done by Anushka Thawani, Theo Sebastian Hemmant and other previous students on this project.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/ff3f4113-f50d-4b9a-96bb-4a251441bcb4/d5456eda-ea49-4f82-a78d-d03f249a4bb8/Untitled.png)

## Burn in simulations
Code and simulated burn in populations on SLIM from previous students

## Running SLIM simulations via HPC 
- TO DO: Make matrix txt file
- TO DO: Write python script that iterates over all 27 scenarios etc


## Python code
- calculate homozygosity to find haplotypes
- TO DO: 
Calculate haplotype lengths, max, minimum nt.


## Haplotype graph tests
Work done by TSH11, Anusha and previous students
TO DO: Add my own calculated graph etc





### Current Status
## Update questions:

- how many ticks in a **burn in** simulation (10,000? or just until fixation)
- what size of genome,  (find in FYP report)
- what kind of mutations do i want to sweep?? (parameters for mutations)

- how many repeats of the soft sweep simulations?
    - just 1 subpopulation

- ask about what do examiners want to see in my poster?

## Progress since last update (14 march):

- drafted hpc job script, the python script and am drafting the slim script ( modify for parameters)
- started github
- got access to RDS on my PC
- almost done w python script for calculating TMRCA… stuck at last step

## plan for rest of this week

1. trial one SLIM simulation on my own PC, 
2. trial 1 simulation from burn in on HPC to get idea of how many cores etc I need 
3. then save the data to the RDS
4. troubleshoot my job script and SLIM/Python script for simulations
5. draft the poster and ask josh for feedback

1. set the HPC to run all my simulations over EASTer 
2. (optional/over easter) finish TMRCA python calculation