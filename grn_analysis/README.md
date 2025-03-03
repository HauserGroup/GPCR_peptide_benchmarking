# Generic residue numbering (GRN) analysis

This subdirectory contains the scripts that were used to analyse experimental models of GPCR–peptide interactions to find out which conserved GRNs are most often involved in GPCR–peptide interactions. 

- `1_parse_gpcrdb_interactions.py` parses data from GPCR–peptide interactions. This script produces two files `interactions.csv` and `grn_frequencies.csv`. `interactions.csv` contains data on the GPCR backbone residues that are involved in GPCR–peptide interactions, while `grn_frequencies.csv` contains the frequencies of each annotated GRN among these reported GPCR–peptide interactions. This script also uses a file `mapping_gpcrdbb.txt` retrieved from https://github.com/protwis/gpcrdb_data to map class B GRNs to class A GRNs. 

- `2_get_chosen_grns.py` was used to parse the minimum number of GRNs required to cover all GPCR–peptide interactions included in the experimental dataset covered in `interactions.csv`. This script also produces a figure, `plots/pdbs_covered.svg` showing the amount of PDB files covered by including each chosen GRNs. These GRNs were later used in the tournament benchmark to define the orthosteric binding pocket of the included GPCRs. 

- `3_interactions_per_region_plot.py` generates a bar plot of reported interactions per GPCR domain, highlighting the domains in which the chosen GRNs are located. The plot is saved in `plots/interacting_residues_per_domain_chosen_residues.svg`.

- `4_pymol_grn_visualization.py` was used to create a PyMOL script to showcase an example of an experimental GPCR-peptide model (PDB code: 7W53) where the chosen GRNs are highlighted. 