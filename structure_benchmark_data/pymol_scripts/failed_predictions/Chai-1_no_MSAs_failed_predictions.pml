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
set_color Chai-1 (no MSAs), [0.722, 0.596, 0.506]
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7SK4_no_MSAs.pdb, 7SK4_Chai-1_no_MSAs
align 7SK4_Chai-1_no_MSAs, 7SK4_experimental
color grey70, chain A and 7SK4_Chai-1_no_MSAs
color white, chain A and 7SK4_experimental
color Chai-1 (no MSAs), 7SK4_Chai-1_no_MSAs and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_Chai-1_no_MSAs_ligand, 7SK4_Chai-1_no_MSAs and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8GY7_AB.pdb, 8GY7_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/8GY7_no_MSAs.pdb, 8GY7_Chai-1_no_MSAs
align 8GY7_experimental, 7SK4_experimental 
align 8GY7_Chai-1_no_MSAs, 8GY7_experimental
color grey70, chain A and 8GY7_Chai-1_no_MSAs
color white, chain A and 8GY7_experimental
color Chai-1 (no MSAs), 8GY7_Chai-1_no_MSAs and chain B
color experimental_color, 8GY7_experimental and chain B
create 8GY7_exp_ligand, 8GY7_experimental and chain B
create 8GY7_Chai-1_no_MSAs_ligand, 8GY7_Chai-1_no_MSAs and chain B
show cartoon, 8GY7_exp_ligand
show cartoon, 8GY7_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 8GY7_exp_ligand
set cartoon_oval_width, 0.7, 8GY7_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 8GY7_exp_ligand
set cartoon_loop_radius, 0.7, 8GY7_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7WQ4_no_MSAs.pdb, 7WQ4_Chai-1_no_MSAs
align 7WQ4_experimental, 7SK4_experimental 
align 7WQ4_Chai-1_no_MSAs, 7WQ4_experimental
color grey70, chain A and 7WQ4_Chai-1_no_MSAs
color white, chain A and 7WQ4_experimental
color Chai-1 (no MSAs), 7WQ4_Chai-1_no_MSAs and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_Chai-1_no_MSAs_ligand, 7WQ4_Chai-1_no_MSAs and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8DWG_AB.pdb, 8DWG_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/8DWG_no_MSAs.pdb, 8DWG_Chai-1_no_MSAs
align 8DWG_experimental, 7SK4_experimental 
align 8DWG_Chai-1_no_MSAs, 8DWG_experimental
color grey70, chain A and 8DWG_Chai-1_no_MSAs
color white, chain A and 8DWG_experimental
color Chai-1 (no MSAs), 8DWG_Chai-1_no_MSAs and chain B
color experimental_color, 8DWG_experimental and chain B
create 8DWG_exp_ligand, 8DWG_experimental and chain B
create 8DWG_Chai-1_no_MSAs_ligand, 8DWG_Chai-1_no_MSAs and chain B
show cartoon, 8DWG_exp_ligand
show cartoon, 8DWG_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 8DWG_exp_ligand
set cartoon_oval_width, 0.7, 8DWG_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 8DWG_exp_ligand
set cartoon_loop_radius, 0.7, 8DWG_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7W56_no_MSAs.pdb, 7W56_Chai-1_no_MSAs
align 7W56_experimental, 7SK4_experimental 
align 7W56_Chai-1_no_MSAs, 7W56_experimental
color grey70, chain A and 7W56_Chai-1_no_MSAs
color white, chain A and 7W56_experimental
color Chai-1 (no MSAs), 7W56_Chai-1_no_MSAs and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_Chai-1_no_MSAs_ligand, 7W56_Chai-1_no_MSAs and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7W53_no_MSAs.pdb, 7W53_Chai-1_no_MSAs
align 7W53_experimental, 7SK4_experimental 
align 7W53_Chai-1_no_MSAs, 7W53_experimental
color grey70, chain A and 7W53_Chai-1_no_MSAs
color white, chain A and 7W53_experimental
color Chai-1 (no MSAs), 7W53_Chai-1_no_MSAs and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_Chai-1_no_MSAs_ligand, 7W53_Chai-1_no_MSAs and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7W55_no_MSAs.pdb, 7W55_Chai-1_no_MSAs
align 7W55_experimental, 7SK4_experimental 
align 7W55_Chai-1_no_MSAs, 7W55_experimental
color grey70, chain A and 7W55_Chai-1_no_MSAs
color white, chain A and 7W55_experimental
color Chai-1 (no MSAs), 7W55_Chai-1_no_MSAs and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_Chai-1_no_MSAs_ligand, 7W55_Chai-1_no_MSAs and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_Chai-1_no_MSAs_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1_no_MSAs/renamed_chains/7W57_no_MSAs.pdb, 7W57_Chai-1_no_MSAs
align 7W57_experimental, 7SK4_experimental 
align 7W57_Chai-1_no_MSAs, 7W57_experimental
color grey70, chain A and 7W57_Chai-1_no_MSAs
color white, chain A and 7W57_experimental
color Chai-1 (no MSAs), 7W57_Chai-1_no_MSAs and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_Chai-1_no_MSAs_ligand, 7W57_Chai-1_no_MSAs and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_Chai-1_no_MSAs_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_Chai-1_no_MSAs_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_Chai-1_no_MSAs_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_Chai-1_no_MSAs
set grid_slot, 1, 7SK4_Chai-1_no_MSAs_ligand
set grid_slot, 2, 8GY7_experimental
set grid_slot, 2, 8GY7_exp_ligand
set grid_slot, 2, 8GY7_Chai-1_no_MSAs
set grid_slot, 2, 8GY7_Chai-1_no_MSAs_ligand
set grid_slot, 3, 7WQ4_experimental
set grid_slot, 3, 7WQ4_exp_ligand
set grid_slot, 3, 7WQ4_Chai-1_no_MSAs
set grid_slot, 3, 7WQ4_Chai-1_no_MSAs_ligand
set grid_slot, 4, 8DWG_experimental
set grid_slot, 4, 8DWG_exp_ligand
set grid_slot, 4, 8DWG_Chai-1_no_MSAs
set grid_slot, 4, 8DWG_Chai-1_no_MSAs_ligand
set grid_slot, 5, 7W56_experimental
set grid_slot, 5, 7W56_exp_ligand
set grid_slot, 5, 7W56_Chai-1_no_MSAs
set grid_slot, 5, 7W56_Chai-1_no_MSAs_ligand
set grid_slot, 6, 7W53_experimental
set grid_slot, 6, 7W53_exp_ligand
set grid_slot, 6, 7W53_Chai-1_no_MSAs
set grid_slot, 6, 7W53_Chai-1_no_MSAs_ligand
set grid_slot, 7, 7W55_experimental
set grid_slot, 7, 7W55_exp_ligand
set grid_slot, 7, 7W55_Chai-1_no_MSAs
set grid_slot, 7, 7W55_Chai-1_no_MSAs_ligand
set grid_slot, 8, 7W57_experimental
set grid_slot, 8, 7W57_exp_ligand
set grid_slot, 8, 7W57_Chai-1_no_MSAs
set grid_slot, 8, 7W57_Chai-1_no_MSAs_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
