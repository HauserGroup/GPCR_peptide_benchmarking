# SETTINGS
# ====================
# location of repo
endogenous_benchmark_dir="/Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking"
classifier_benchmark_dir=$endogenous_benchmark_dir/classifier_benchmark_data
conda_env_path="/Users/kcd635/Documents/GitHub/RoseTTAFold-All-Atom/test_env/"
# location of input files
endogenous_ligands_csv=$classifier_benchmark_dir/input/endogenous_ligand_detailed.csv
# output dir
output_dir=$classifier_benchmark_dir/output
mkdir -p $output_dir
# ====================
conda activate $conda_env_path

# Get interaction pairs, this INCLUDES EXPERIMENTAL DUPLICATES. Takes ~10 mins
valid_interactions_csv=$classifier_benchmark_dir/output/1_valid_hormone_interactions.csv
python3 $classifier_benchmark_dir/step1_get_valid_interactions.py --endogenous_ligand_csv $endogenous_ligands_csv --output_file $valid_interactions_csv

# # Get the positive dataset
hormone_interactions_csv=$classifier_benchmark_dir/output/2_hormone_interactions.csv
python3 $classifier_benchmark_dir/step2_annotate_interactions.py --valid_interactions_csv $valid_interactions_csv --output_file $hormone_interactions_csv

# plot the peptide distributions
python3 $classifier_benchmark_dir/step3a_plot_peptide_distributions.py --interactions_path $hormone_interactions_csv --plot_path $output_dir/3a_peptide_distributions.png
python3 $classifier_benchmark_dir/step3b_read_experimental_values.py --interactions_path $hormone_interactions_csv --endo_detailed_path $endogenous_ligands_csv --save_activity_path $output_dir/3b_experimental_values.csv
# Get the similarity matrices
similarity_df_path=$output_dir/3c_similarity_matrix_binding_pocket.csv
python3 $classifier_benchmark_dir/step3c_get_similarity_matrix.py --metric "similarity" --mode "binding_pocket" --interactions_path $hormone_interactions_csv --out_matrix_path $similarity_df_path
identity_df_path=$output_dir/3c_identity_matrix_binding_pocket.csv
python3 $classifier_benchmark_dir/step3c_get_similarity_matrix.py --metric "identity" --mode "binding_pocket" --interactions_path $hormone_interactions_csv --out_matrix_path $identity_df_path
generic_residue_df_path=$output_dir/3d_generic_residues_binding_pocket.csv
python3 $classifier_benchmark_dir/step3d_get_generic_residues.py --interactions_path $hormone_interactions_csv --out_path $generic_residue_df_path

# Get principal agonists
principal_agonist_interactions_csv=$output_dir/4_principal_agonists_interactions.csv
python3 $classifier_benchmark_dir/step4_get_principal_agonists.py --interactions_path $hormone_interactions_csv --activity_interactions_path $output_dir/3b_experimental_values.csv --output_path $principal_agonist_interactions_csv

# get node graph
python3 $classifier_benchmark_dir/step5_get_node_graph.py --interactions_with_principal_agonists_path $principal_agonist_interactions_csv --network_plot_path $output_dir/5_network_plot.png

# get decoys
interactions_with_decoys_csv=$output_dir/6_interactions_with_decoys.csv
python3 $classifier_benchmark_dir/step6_get_decoys.py --similarity_df_path $similarity_df_path --identity_df_path $identity_df_path --interactions_df_path $principal_agonist_interactions_csv --out_path $interactions_with_decoys_csv

# plot decoys
decoy_plot_dir=$output_dir/7_decoy_plots
mkdir -p $decoy_plot_dir
python3 $classifier_benchmark_dir/step7_plot_decoys.py --interactions_path $principal_agonist_interactions_csv --decoy_dataset_path $interactions_with_decoys_csv --plot_dir $decoy_plot_dir
