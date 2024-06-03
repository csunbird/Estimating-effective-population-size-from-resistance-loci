#!/usr/bin/env python
# coding: utf-8

# Clustering simulated sequences using TMRCA
# 
# Name: CQS21 
# FYP 2024

# Import modules
import numpy as np
import zarr
import allel   
#idk why but my allel doesnt seem to load?? even though ive definitely installed it as scikit-allel
import scipy.cluster.hierarchy as sch
import scipy.spatial
import matplotlib
import matplotlib.pyplot as plt
import scipy.signal
from scipy.ndimage import gaussian_filter1d
from numpy.lib.stride_tricks import sliding_window_view
from tqdm import tqdm
import dask
from dask.delayed import delayed
from dask.base import compute
from itertools import combinations
import seaborn as sns
#import tskit
import pandas as pd


global genome_length
genome_length =70000
global mutation
mutation = int((genome_length+1)/2) 
global threshold
threshold = 0.87  #setting threshold to calculate trough points in each haplotype
global points
points=280
global window 
window=600
global sample_size
sample_size = 100
global no_haplotypes
no_haplotypes = sample_size*2


import os
global array_index 
array_index = int(os.environ['PBS_ARRAY_INDEX']) # HPC ppl suggested using os module, gets it as a str, need to int() it
#instead of using sys.argv[1] which takes the first argument passed
print (array_index)


## read in population size, mu, r from population parameters csv
parameters = pd.read_csv('parameter_combinations.csv')
index = array_index +1

global combination
combination = parameters.iloc[index]['file']

global seed
seed = int(os.environ['seed'])
print (seed)





#prev student: Like Hamming distance code, this was also taken from Anushka Thawani. Adaptations were made to this on the 
#high-performance computer using shell script, but this could not be represented.
def convert(file):
    '''
    This function extracts haplotypes sequences from a vcf file 
    Adapted from: http://alimanfoo.github.io/2018/04/09/selecting-variants.html 
    
    Arguments:
        file: name of vcf file (from SLiM soft sweep simulation)
        
    Returns:
        ht: haplotype sequences for 200 individuals
        samp_freq: frequency of sweep mutation in sample
        cols: used to color dendrogram
        pos: array of the ID and genomic position of each variant

    '''
    
    v = file + '.vcf'
    z = file + '.zarr'
    slim_sim_data = allel.read_vcf(v, fields='*')
    allel.vcf_to_zarr(v, z, fields='*', overwrite=True)
    data = zarr.open_group(z, mode='r')
    
    # Stores the ID and genomic position of each variant 
    print(data['variants/POS'])                              #debugging
    #variants = data['variants']
    #pos = allel.SortedIndex(variants['POS']) 
    pos = allel.SortedIndex(data['variants/POS'])            #KEEPS THROWING KEY ERROR meaning start and stop is the same! Why!
    
    # Extract genotypes for the first 200 individuals and convert to haplotypes
    gt = data['calldata/GT'][:,0:200] 
    ht = allel.GenotypeArray(gt).to_haplotypes()
    
    mutation = int((genome_length+1)/2) # position of sweep mutation
    
    
    # Output the frequency of the sweep mutation in the sample
    contains_sweep = pos.locate_range(mutation,mutation) #finds index of sweep mutation in the array
    sweep = ht[contains_sweep]                           # saves the haplotypes containing the sweep in the variable sweep
    sweep = np.sum(sweep, axis =0)                       #sums up mutation occurences in each haplotypes
    
    samp_freq = np.sum(sweep)/200  # finds freq in the entire sample of 100 individuals, 200 haplotypes
    
    
    # This dictionary is used later to color the dendrogram branches according to whether or not the 
    # corresponding sequence contains the sweep mutation
    cols = {}
    for i in range(200):
        if sweep[i]:
            cols[i] = "#FF0000" 
        else:
            cols[i] = "#808080"
    #analysis() checkpoint
    print(" converted")
    
    return ht, pos, samp_freq, cols, sweep

# %% [markdown]
# Step 4. Calculate Hij (S or homozygosity) for all pairs of haplotypes
# make a function 
# homozygosity = (no. of SNPs/ length of window, L)

# %%
def sliding_homozygosity(ht, pos, gts):
    '''
    This function calculates the sliding homozygosity for all pairs of haplotypes.
    
    Arguments:
    window: length of sliding window
    len_genome : length of genome 
    ht : vector?  of haplotype sequences from convert() function in previous codeblock
    pos: position of variants from convert() function in previous codeblock

    
    Returns:
    homozygosities:  homozygosity of all haplotypes in ht in a array(?)
    '''
    # Make empty vectors
    homozygosities = np.empty(shape=(genome_length,gts),dtype=np.float32)  
    reg = slice(-100,-100, None)
    
    #iterate through all nucleotides in the genome
    for x in range(0, genome_length):
        #define nt ranges 
        start  = x
        end = x + window

        try:
            # locate the position of region around a variant Nt
            region = pos.locate_range(start,end) 

            #check if current window (region) is different from previous window (reg) for streamlining purposes
            if region!= reg:
                haplotype_region = ht [region]
                #use allel.pairwise distance
                pairwise_dist = allel.pairwise_distance(haplotype_region, metric = 'hamming') #can i chunk = true to speed up computation? 
                homozygosities[x,:] = pairwise_dist/window
                reg = region

            else:
                homozygosities[x,:] = pairwise_dist/window

        except KeyError:
            pass  
    # analysis() checkpoint
    print("sliding homozygosity has been calculated.")
    
    return homozygosities

# %% [markdown]
# Step 5. Calculate Lij (shared haplotype length) from Hij by finding width at half maximum homozygosity

# %%
#half_max_homozygosity = (max(homozygosities) + min(homozygosities))/2

#Defining function to find troughs, to be used in calculating Lij in another function
def finding_troughs(smooth, pos):
    '''
    This function finds troughs for a pair of haplotype sequences. 
    Note: threshold set to 0.87
    
    Arguments:
        sliding homozygosity: smoothed sliding window homozygosity for all pairs of sequences
        sweeploc: position of sweep mutation in genome (same as previous function)
        
    Returns:
        lower: position of breakpoint left of the sweep site
        upper: position of breakpoint right of the sweep site
        SHL: shared haplotype length
    '''
    global threshold
    threshold = 0.87  #setting threshold to calculate trough points in each haplotype

    #finding troughs
    troughs = scipy.signal.find_peaks(-smooth) #- sign inverts the graph so the 'peaks' are our troughs
    troughs = troughs[0]     # Indexes of all troughs
    troughs = troughs[smooth[troughs] < threshold]   # Extract troughs where homozygosity<threshold
    
    #finds the peaks
    peaks = scipy.signal.find_peaks(smooth)
    peaks = peaks[0]  #indexes peaks
    
    # Find positions of troughs flanking sweep site
    bp = np.searchsorted(troughs,pos)  #search sorted finds index of position where mutation should be inserted in order to maintain the same order
    lower = troughs[bp - 1] #index of sweep site -1
    upper = troughs[bp]  #index of sweep site
    
    # Find the average peak position around the sweep site
    highest = peaks[(peaks >= lower) & (peaks <= upper)]
    if highest.size != 0:
        highest = np.mean(highest)
    else: 
        highest = (lower+upper)/2
    
    
    lower = (lower+highest)/2
    upper = (upper+highest)/2

    SHL = upper - lower
    
    #analysis() checkpoint
    print( "troughs found, SHL: " + SHL)
    
    return int(lower), int(upper), SHL



# %%
## function using each haplotype pair to return SHL and find lower and upper limits of SHL
# uses finding_troughs()
def find_breakpoint(haplotype_pair):
    '''
    For a pair of sequences, this function smoothes the sliding homozygosity and returns the SHL
    Arguments:haplotype_pair
        haplotype_pair: a pair of haplotype sequences
        
    Returns:
        lower: position of breakpoint left of the sweep site
        upper: position of breakpoint right of the sweep site
        SHL: shared haplotype length
    '''
    
    mutation_pos = mutation 
    smooth = gaussian_filter1d(haplotype_pair, points)
    try:
        lower, upper, SHL = finding_troughs(smooth, mutation_pos)
    except IndexError:
        lower = -1.3
        upper = -1.3
        SHL = -1.3
    
    # analysis()
    print("breakpoints have been found")
    
    return lower, upper, SHL

# %% [markdown]
# Step 6. Calculate Tij (Time to common ancestor) from Lij and Kij (which is no. of SNPs) on each shared length (haplotype)
# 
# 𝜏_𝑖𝑗=(𝑘_𝑖𝑗+1)/(2ℓ_𝑖𝑗 (𝑟+𝜇))

# %%
# Calculating Kij (No. of SNPs in each SHL)

def calculating_kij(gts,ht,result_find_breakpoint,pos):
    '''
    This function finds the number of SNPs over the shared haplotype length for all pairs of haplotype sequences
    
    Arguments:
        gts: number of haplotype pairs
        ht: haplotype sequnces
        result_find_breakpoint: output from find_breakpoint function
        
    Returns:
        diffs: number of SNPs for all pairs of haplotype sequences
        
    '''
    pairwise = []
    for combo in combinations(list(range(0,no_haplotypes)), 2): 
        pairwise.append(combo)

    diffs = np.empty(shape=(gts),dtype=np.float32)
    for i in range(gts):
        pair = ht[:,pairwise[i]]
        try:
            start = result_find_breakpoint[i,1]
            stop = result_find_breakpoint[i,2]

            window_pos = pos.locate_range(start, stop)
            window = pair[window_pos]

            d = allel.pairwise_distance(window, metric = "hamming")

            diffs[i]=d 

        except KeyError:
            diffs[i]=-1.3 
    
    return diffs

# %%
#Calculating Tij, Time to Common Ancestor (TMRCA) using mutation rate and number of SNPs
# 𝜏_𝑖𝑗=(𝑘_𝑖𝑗+1)/(2ℓ_𝑖𝑗 (𝑟+𝜇))
#for array number x:
    #read in vcf file
    # read in population size, mu, r from population parameters csv file


def calculating_Tij(array_index, seed, cutoff):
    '''
    This function calculates Tij, Time to Common Ancestor (TMRCA) using mutation rate and number of SNPs for each haplotype pair.
    It uses the convert() to convert files from vcf 
    It uses the sliding_heterozygosity() to calculate heterozygosity in the window for all pairs of haplotypes

    
    Arguments:
        array_index: array index or combination number of simulation
        seed: seed number of simulation
        cutoff: 40 % allele freq for rdl and 80% for vgsc

        
        genome_length: length of genome (in SLiM simulation)             ##can loop?
        ht : haplotypes (what variable structure?)

        window: length of sliding window
        threshold: threshold above which troughs are ignored
        points: number of points to use for 1D-gaussian filter (see scipy documentation)
        
    Returns:
        Tij: Time to Common Ancestor (TMRCA)
  
    '''
    import numpy as np
    
    
    ## read in population size, mu, r from population parameters csv
    parameters = pd.read_csv('parameter_combinations.csv')
    index = array_index +1
    global pop_size
    pop_size = parameters.iloc[index]['N']
    global mu
    mu = parameters.iloc[index]['Mutation Rate']
    global r
    r = parameters.iloc[index]['Recombination Rate']


    # for array number:
        #read in vcf file
    file =  str(array_index) + "_"+ str(seed) +"_"+ str(cutoff)  #".vcf" added by convert()
    # Extract haplotype sequences from .vcf file
    ht, pos, samp_freq, cols, sweep = convert(file)

    
    # Calculate sliding homozygosity for all pairs of haplotype sequences
    gts = int((no_haplotypes*(no_haplotypes-1))/2)
    homozygosities = sliding_homozygosity(ht, pos, gts)

    
    # Find SHL for all pairs of haplotype sequences 
    hom_dask = dask.array.from_array(homozygosities, chunks=(genome_length,1)) # type: ignore # creates a dask array
    homozygosities = []
    results = dask.array.apply_along_axis(find_breakpoint, 0, hom_dask) # type: ignore #applies find_breakpoint() along the array
    results_computed = results.compute()

    # Manipulating the dataframe to make it easier to process
    results_computed = np.transpose(results_computed)
    index = np.asarray(range(0,gts))
    index = np.expand_dims(index, axis=0)
    results_computed_1 = np.concatenate((index.T, results_computed), axis=1)
    
    
    # Calculate the TMRCA from the SHLs and number of SNPs
    recombination_rate = r/(2*pop_size)
    mu = mu/(100*pop_size)
    shls = results_computed_1[:,3]   # SHLs for all pairs of haplotype sequences 
    shls[shls<=0] = genome_length
    diffs = calculating_kij(gts, ht, results_computed_1, pos)  # SNPs for all pairs of haplotype sequences 
    Tij = (1+(diffs*shls))/(2*shls*(recombination_rate + mu)) # TMRCA metric for all pairs of haplotype sequences 

    
    # Remove negative and non-integer TMRCA values
    impute = np.nanmean(Tij)        #impute is the mean of SNP array without any NAN values
    x = np.isfinite(Tij)            #x is a boolean mask array of only finite values (cannot be infinite or NAN)
    for i in np.where(x == 0)[0]:   #for all indices where there is a non-finite number:
        Tij[i] = impute             #replace NaN with inpute value
    Tij[Tij<=0] = impute            # replace all negative numbers wih inpute

    # checkpoint for analysis()
    print(" TIj calculated:"+ Tij)
    return Tij, cols, pop_size, mu, r
    

# %% [markdown]
# Step 7. Plotting TMRCA dendrogram 
# - prev student ran into problems here with generating the dendrogram coloured tips
# - Untested to see if I have resolved previous student problem
# 

# %%

def analysis(array_index, seed, cutoff): 

    '''
    This function plots a dendrogram and colours red the tips that have the sweep mutations. 
    It uses calculating_Tij().
    Only the output vcf from the SLIM simulation is input.
    global variables genome_length, window, threshold, points being used

    Arguments:
    array_index: array index or combination number of simulation
    seed: seed number of simulation
    cutoff: 40 % allele freq for rdl and 80% for vgsc
    
    global variables/ variables from sub functions:
    window: length of sliding window
    threshold: threshold above which troughs are ignored
    points: number of points to use for 1D-gaussian filter (see scipy documentation)
    cols: colours haplotype branches red if they have sweep mutation. From convert().



    Returns:
    output dendrogram in pdf
    '''
    #all convert(), etc etc to end up with tij
    Tij, cols, pop_size, mu, r = calculating_Tij(array_index, seed, cutoff)
    
    # Hierachical Clustering, store in Z
    Z = sch.linkage(Tij, method = 'average') #why do we use the Farthest Point Algorithm? changed to average (UPGMA) , check after
    

    ## Plot dendrogram without colouring branches
    # updating matplotlib font settings
    matplotlib.rcParams.update({'font.size': 24})
    fig = plt.figure(figsize=(30, 12))
    gs = matplotlib.gridspec.GridSpec(2, 1, hspace=0.1, wspace=1, height_ratios=(1,1)) # type: ignore

    ax_dend = fig.add_subplot(gs[0, 0])
    sns.despine(ax=ax_dend, offset=5, bottom=True, top=True)
    dd = sch.dendrogram(Z,color_threshold=0,above_threshold_color='#808080',ax=ax_dend) # if above colour threshold, set colour to grey 

    ls = []
    for leaf, leaf_color in zip(plt.gca().get_xticklabels(), dd["leaves_color_list"]):   #leaves_color_list is A list of color names. The k’th element represents the color of the k’th leaf.
        leaf.set_color(cols[int(leaf.get_text())])
        ls.append(int(leaf.get_text()))

    ax_dend.set_ylabel('Haplotype age/generations',fontsize=24)
    ax_dend.set_title('Haplotype clusters',fontsize=24)



    # Plot dendrogram and colour branches
    ax_dend_2 = fig.add_subplot(gs[1, 0])
    
    dflt_col = "#808080"
    
    link_cols = {}
    for i, i12 in enumerate(Z[:,:2].astype(int)):
        c1, c2 = (link_cols[x] if x > len(Z) else cols[x] for x in i12)
        link_cols[i+1+len(Z)] = c1 if c1 == c2 else dflt_col

    sns.despine(ax=ax_dend_2, offset=5, bottom=True, top=True)
    dd = sch.dendrogram(Z,link_color_func=lambda x: link_cols[x], ax=ax_dend_2)

    ls = []
    for leaf, leaf_color in zip(plt.gca().get_xticklabels(), dd["leaves_color_list"]):
        leaf.set_color(cols[int(leaf.get_text())])
        ls.append(int(leaf.get_text()))

    ax_dend_2.set_ylabel('Haplotype age/generations',fontsize=24)
    
    
    # Save dendrogram
    output_directory = '/dendrograms/' 
    output = output_directory + 'dendrogram_' + str(array_index) + "_"+ str(seed) +"_"+ str(cutoff) +'.pdf' 
    print (output)
    plt.savefig(output)  
    
    return

seed = 1811758731
cutoff = 80
#run analysis
analysis(1, seed, cutoff)
#analysis(2, seed, cutoff)
#analysis(3, seed, cutoff)
analysis(4, seed, cutoff)
analysis(5, seed, cutoff)
analysis(6, seed, cutoff)
analysis(7, seed, cutoff)
analysis(8, seed, cutoff)
analysis(9, seed, cutoff)




