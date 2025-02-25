This directory contains the scripts to produce input files for the included computational models to provide structural predictions and analyse these results by comparing them against experimental models of the same inputs. 

Folders: 
- `fastas`: Fastas of the included experimental structures
- `pdbs`: Structures of the included experimental models in the benchmark
- `cifs`: Structures of the included experimental models in the benchmark
- `cleaned_pdbs`: Reformatted experimental structures (chains renamed to be consistently A for receptor and B for peptide ligand)
- `subanalyses`: Subanalyses of structural benchmarking results (Identity vs DockQ, receptor RMSD, performance by GPCR class)
- `plots`: Plots visualing structural benchmarking results
- `pymol_scripts`: Pymol scripts to visualize accurate and inaccurate predictions produced by the included models

Scripts:
- `1_experimental_benchmark.py`: Parsing the dataset from GPCRdb of recently published GPCR–peptide models that have not been studied experimentally before the training date cutoffs of the included models. The produced dataset is saved as `3f_known_structures_benchmark_2021.09-30.csv`
- `2_structure_evaluation.py`: Script to run DockQ scoring on the produced models against the experimental models of the same interactions (run on a computing cluster, DockQ run as described by the authors: https://github.com/bjornwallner/DockQ). Parses dataset to cleaner format (`3f_known_structures_benchmark_2021.09-30_cleaned.csv`) and saves DockQ results to `DockQ_results.csv`. 
- `3_performance_evaluation.py`: Script to analyse DockQ scores and receptor RMSD values by model, results saved under `plots/`
- `4_get_statistical_significance.py`: Script to statistically compare DockQ and RMSD values produced by each model against each other to see which models are statistically better compared to the other models. Results are saved in `wilcoxon_results_{DockQ,rmsd}.csv`
- `cif_to_pdb.py`: Helper script to print command line commands to convert CIF files to PDB format using PyMOL. This was used for large PDB inputs that could not be retrieved from RCSB PDB and AF3 predictions that are by default in CIF format. 