reinit
bg_color white
set ray_trace_mode, 1
set ray_trace_gain, 0.1
set ray_shadows, 1
set ray_trace_fog, 0
set antialias, 2
set ambient, 0.2
set reflect, 0.3
set specular, 0.5
set shininess, 10
set depth_cue, 1
set ray_opaque_background, off
set cartoon_rect_length, 0.75
set cartoon_oval_length, 0.75
set hash_max, 80

# Ambient Occlusion settings
set ray_trace_depth_factor, 0.6
set ray_trace_disco, 1.3

# Light settings - adjusted for a darker effect
set light_count, 8
set light2, [-0.3, 0.5, 1]
set light3, [0.5, -0.5, 0.6]  # Reduced intensity
set light4, [-0.8, 0.3, 0.3]  # Reduced intensity
set light5, [0.5, 0.5, 0.5]   # Reduced intensity
set light6, [0.3, -0.7, 0.3]
set light7, [0.5, 0.5, -0.5]
set light8, [-0.5, -0.5, 0.5]

# settings to make the receptor look more like chimerax
set cartoon_side_chain_helper, 1
set cartoon_tube_radius, 0.4
set orthoscopic, on
set ray_trace_mode, 1
set ray_shadows, 0





set_color experimental_color, [0.976, 0.667, 0.263]
set_color Chai-1, [0.522, 0.369, 0.251]
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7SK4.pdb, 7SK4_Chai-1
align 7SK4_Chai-1, 7SK4_experimental
color grey70, chain A and 7SK4_Chai-1
color white, chain A and 7SK4_experimental
color Chai-1, 7SK4_Chai-1 and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_Chai-1_ligand, 7SK4_Chai-1 and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_Chai-1_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8IA8.pdb, 8IA8_Chai-1
align 8IA8_experimental, 7SK4_experimental 
align 8IA8_Chai-1, 8IA8_experimental
color grey70, chain A and 8IA8_Chai-1
color white, chain A and 8IA8_experimental
color Chai-1, 8IA8_Chai-1 and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_Chai-1_ligand, 8IA8_Chai-1 and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_Chai-1_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ3_AB.pdb, 7WQ3_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7WQ3.pdb, 7WQ3_Chai-1
align 7WQ3_experimental, 7SK4_experimental 
align 7WQ3_Chai-1, 7WQ3_experimental
color grey70, chain A and 7WQ3_Chai-1
color white, chain A and 7WQ3_experimental
color Chai-1, 7WQ3_Chai-1 and chain B
color experimental_color, 7WQ3_experimental and chain B
create 7WQ3_exp_ligand, 7WQ3_experimental and chain B
create 7WQ3_Chai-1_ligand, 7WQ3_Chai-1 and chain B
show cartoon, 7WQ3_exp_ligand
show cartoon, 7WQ3_Chai-1_ligand
set cartoon_oval_width, 0.7, 7WQ3_exp_ligand
set cartoon_oval_width, 0.7, 7WQ3_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7WQ3_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ3_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7WQ4.pdb, 7WQ4_Chai-1
align 7WQ4_experimental, 7SK4_experimental 
align 7WQ4_Chai-1, 7WQ4_experimental
color grey70, chain A and 7WQ4_Chai-1
color white, chain A and 7WQ4_experimental
color Chai-1, 7WQ4_Chai-1 and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_Chai-1_ligand, 7WQ4_Chai-1 and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_Chai-1_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8DWG_AB.pdb, 8DWG_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8DWG.pdb, 8DWG_Chai-1
align 8DWG_experimental, 7SK4_experimental 
align 8DWG_Chai-1, 8DWG_experimental
color grey70, chain A and 8DWG_Chai-1
color white, chain A and 8DWG_experimental
color Chai-1, 8DWG_Chai-1 and chain B
color experimental_color, 8DWG_experimental and chain B
create 8DWG_exp_ligand, 8DWG_experimental and chain B
create 8DWG_Chai-1_ligand, 8DWG_Chai-1 and chain B
show cartoon, 8DWG_exp_ligand
show cartoon, 8DWG_Chai-1_ligand
set cartoon_oval_width, 0.7, 8DWG_exp_ligand
set cartoon_oval_width, 0.7, 8DWG_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8DWG_exp_ligand
set cartoon_loop_radius, 0.7, 8DWG_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8F7X.pdb, 8F7X_Chai-1
align 8F7X_experimental, 7SK4_experimental 
align 8F7X_Chai-1, 8F7X_experimental
color grey70, chain A and 8F7X_Chai-1
color white, chain A and 8F7X_experimental
color Chai-1, 8F7X_Chai-1 and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_Chai-1_ligand, 8F7X_Chai-1 and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_Chai-1_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RYC_AB.pdb, 7RYC_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7RYC.pdb, 7RYC_Chai-1
align 7RYC_experimental, 7SK4_experimental 
align 7RYC_Chai-1, 7RYC_experimental
color grey70, chain A and 7RYC_Chai-1
color white, chain A and 7RYC_experimental
color Chai-1, 7RYC_Chai-1 and chain B
color experimental_color, 7RYC_experimental and chain B
create 7RYC_exp_ligand, 7RYC_experimental and chain B
create 7RYC_Chai-1_ligand, 7RYC_Chai-1 and chain B
show cartoon, 7RYC_exp_ligand
show cartoon, 7RYC_Chai-1_ligand
set cartoon_oval_width, 0.7, 7RYC_exp_ligand
set cartoon_oval_width, 0.7, 7RYC_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7RYC_exp_ligand
set cartoon_loop_radius, 0.7, 7RYC_Chai-1_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_Chai-1
set grid_slot, 1, 7SK4_Chai-1_ligand
set grid_slot, 2, 8IA8_experimental
set grid_slot, 2, 8IA8_exp_ligand
set grid_slot, 2, 8IA8_Chai-1
set grid_slot, 2, 8IA8_Chai-1_ligand
set grid_slot, 3, 7WQ3_experimental
set grid_slot, 3, 7WQ3_exp_ligand
set grid_slot, 3, 7WQ3_Chai-1
set grid_slot, 3, 7WQ3_Chai-1_ligand
set grid_slot, 4, 7WQ4_experimental
set grid_slot, 4, 7WQ4_exp_ligand
set grid_slot, 4, 7WQ4_Chai-1
set grid_slot, 4, 7WQ4_Chai-1_ligand
set grid_slot, 5, 8DWG_experimental
set grid_slot, 5, 8DWG_exp_ligand
set grid_slot, 5, 8DWG_Chai-1
set grid_slot, 5, 8DWG_Chai-1_ligand
set grid_slot, 6, 8F7X_experimental
set grid_slot, 6, 8F7X_exp_ligand
set grid_slot, 6, 8F7X_Chai-1
set grid_slot, 6, 8F7X_Chai-1_ligand
set grid_slot, 7, 7RYC_experimental
set grid_slot, 7, 7RYC_exp_ligand
set grid_slot, 7, 7RYC_Chai-1
set grid_slot, 7, 7RYC_Chai-1_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
