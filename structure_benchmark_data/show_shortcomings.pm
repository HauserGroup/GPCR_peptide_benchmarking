reinitialize
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/structure_benchmark/ESMFold/7VV0.pdb, EF
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/structure_benchmark/RFAA_chain/7VV0.pdb, RF
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/structure_benchmark/neuralplexer_chain/7VV0.pdb, NP

# color chain a white
color white, chain A
# color chain b orange
color orange, chain B
@/Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/ray.pm
# white background
bg_color white

# set grid mode
set grid_mode, 1

# align all to EF on chain A
align RF and chain A, EF and chain A
align NP and chain A, EF and chain A
