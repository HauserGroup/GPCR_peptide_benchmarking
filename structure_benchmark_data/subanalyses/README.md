# Subanalyses of structural benchmark results

This folder contains scripts to perform subanalyses on the structural benchmark. These analyses cover:
- Identity vs DockQ analyses (scripts: `get_mmseqs2_evalue.py`, `get_training_pdb_seqres.py`, results: `mmseqs2_results/`) were conducted to see whether structural accuracy of the predictions was driven by existence of highly similar training structures
- Class analyses (script: `class_differences.py`, results: `class_{DockQ,rmsd}_comparison_results`) cover the analyses of structural predictions by class to see whether GPCR class differences in modelling performance exist
- LIS vs DockQ (script: `dockq_vs_lis.py`, results: `AF_LIS_results/`): the rescoring metric of protein-protein interactions (LIS) that was proven to be the most accurate in the classifier benchmark was correlated against DockQ to see whether the rescoring metric also correlates with structural accuracy 
- Receptor RMSD (script: `calculate_receptor_rmsd.py`, results: `receptor_rmsds.csv`) was used to analyse the receptor RMSD of the predicted structures to see how different models perform on modelling the GPCR backbone