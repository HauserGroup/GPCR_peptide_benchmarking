# Deep learning in GPCR drug discovery: Benchmarking the path to accurate peptide binding

The repository contains the scripts used to analyse results for "Deep learning in GPCR drug discovery: Benchmarking the path to accurate peptide binding". As majority of the benchmarked tools were run using settings described in the publication, the scripts used on the computing cluster to produce e.g. AlphaFold 2 predictions are not provided here. Therefore, this repository contains the scripts that were used to analyse these results, e.g. scripts to run DockQ scoring on the produced structures, parsing datasets for different benchmarks, and producing ROC metrics for the classifier tasks. Specific environment files for, e.g., running AlphaFold 2 and 3 and the raw structural predictions are also not provided here due to repository size constraints, but can be acquired by contacting the corresponding author Alexander S. Hauser (alexander.hauser@sund.ku.dk). 

The repository is organised as follows: 
- **classifier_benchmark** contains the analysis scripts for the agonist-decoy classifier results.
- **classifier_benchmark_data** contains the data query scripts for the agonist interactions, and the input files for the classifier_benchmark.
- **classifier_subanalysis** contains the analysis scripts and results for re-scoring PDBs.
- **grn_analysis contains** the generic residue scripts and ids.
- **plots** contains data and code to produce some of the supplementary and main figures included in the paper. 
- **structure_benchmark** contains the predicted pdbs for the structural benchmark.
- **structure_benchmark_data** contains the query scripts and input data for the structural benchmark.
- **tournament_benchmark** contains the results for the tournament approach.

`colors.py` contains the color scheme used in the current project to produce a consistent coloring throughout the produced figures. 

More documentation is provided in `README.md` files inside each subfolder and in the included scripts. 