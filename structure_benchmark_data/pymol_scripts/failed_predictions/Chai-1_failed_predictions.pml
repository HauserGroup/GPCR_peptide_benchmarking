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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7SK4_1.pdb, 7SK4_Chai-1
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8GY7_AB.pdb, 8GY7_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/8GY7_1.pdb, 8GY7_Chai-1
align 8GY7_experimental, 7SK4_experimental 
align 8GY7_Chai-1, 8GY7_experimental
color grey70, chain A and 8GY7_Chai-1
color white, chain A and 8GY7_experimental
color Chai-1, 8GY7_Chai-1 and chain B
color experimental_color, 8GY7_experimental and chain B
create 8GY7_exp_ligand, 8GY7_experimental and chain B
create 8GY7_Chai-1_ligand, 8GY7_Chai-1 and chain B
show cartoon, 8GY7_exp_ligand
show cartoon, 8GY7_Chai-1_ligand
set cartoon_oval_width, 0.7, 8GY7_exp_ligand
set cartoon_oval_width, 0.7, 8GY7_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8GY7_exp_ligand
set cartoon_loop_radius, 0.7, 8GY7_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGM_AB.pdb, 8XGM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/8XGM_1.pdb, 8XGM_Chai-1
align 8XGM_experimental, 7SK4_experimental 
align 8XGM_Chai-1, 8XGM_experimental
color grey70, chain A and 8XGM_Chai-1
color white, chain A and 8XGM_experimental
color Chai-1, 8XGM_Chai-1 and chain B
color experimental_color, 8XGM_experimental and chain B
create 8XGM_exp_ligand, 8XGM_experimental and chain B
create 8XGM_Chai-1_ligand, 8XGM_Chai-1 and chain B
show cartoon, 8XGM_exp_ligand
show cartoon, 8XGM_Chai-1_ligand
set cartoon_oval_width, 0.7, 8XGM_exp_ligand
set cartoon_oval_width, 0.7, 8XGM_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8XGM_exp_ligand
set cartoon_loop_radius, 0.7, 8XGM_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7WQ4_1.pdb, 7WQ4_Chai-1
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/8WVY_1.pdb, 8WVY_Chai-1
align 8WVY_experimental, 7SK4_experimental 
align 8WVY_Chai-1, 8WVY_experimental
color grey70, chain A and 8WVY_Chai-1
color white, chain A and 8WVY_experimental
color Chai-1, 8WVY_Chai-1 and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_Chai-1_ligand, 8WVY_Chai-1 and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_Chai-1_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IOC_AB.pdb, 8IOC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/8IOC_1.pdb, 8IOC_Chai-1
align 8IOC_experimental, 7SK4_experimental 
align 8IOC_Chai-1, 8IOC_experimental
color grey70, chain A and 8IOC_Chai-1
color white, chain A and 8IOC_experimental
color Chai-1, 8IOC_Chai-1 and chain B
color experimental_color, 8IOC_experimental and chain B
create 8IOC_exp_ligand, 8IOC_experimental and chain B
create 8IOC_Chai-1_ligand, 8IOC_Chai-1 and chain B
show cartoon, 8IOC_exp_ligand
show cartoon, 8IOC_Chai-1_ligand
set cartoon_oval_width, 0.7, 8IOC_exp_ligand
set cartoon_oval_width, 0.7, 8IOC_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8IOC_exp_ligand
set cartoon_loop_radius, 0.7, 8IOC_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGB_AB.pdb, 8JGB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/8JGB_1.pdb, 8JGB_Chai-1
align 8JGB_experimental, 7SK4_experimental 
align 8JGB_Chai-1, 8JGB_experimental
color grey70, chain A and 8JGB_Chai-1
color white, chain A and 8JGB_experimental
color Chai-1, 8JGB_Chai-1 and chain B
color experimental_color, 8JGB_experimental and chain B
create 8JGB_exp_ligand, 8JGB_experimental and chain B
create 8JGB_Chai-1_ligand, 8JGB_Chai-1 and chain B
show cartoon, 8JGB_exp_ligand
show cartoon, 8JGB_Chai-1_ligand
set cartoon_oval_width, 0.7, 8JGB_exp_ligand
set cartoon_oval_width, 0.7, 8JGB_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8JGB_exp_ligand
set cartoon_loop_radius, 0.7, 8JGB_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7W56_1.pdb, 7W56_Chai-1
align 7W56_experimental, 7SK4_experimental 
align 7W56_Chai-1, 7W56_experimental
color grey70, chain A and 7W56_Chai-1
color white, chain A and 7W56_experimental
color Chai-1, 7W56_Chai-1 and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_Chai-1_ligand, 7W56_Chai-1 and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7W53_1.pdb, 7W53_Chai-1
align 7W53_experimental, 7SK4_experimental 
align 7W53_Chai-1, 7W53_experimental
color grey70, chain A and 7W53_Chai-1
color white, chain A and 7W53_experimental
color Chai-1, 7W53_Chai-1 and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_Chai-1_ligand, 7W53_Chai-1 and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7W55_1.pdb, 7W55_Chai-1
align 7W55_experimental, 7SK4_experimental 
align 7W55_Chai-1, 7W55_experimental
color grey70, chain A and 7W55_Chai-1
color white, chain A and 7W55_experimental
color Chai-1, 7W55_Chai-1 and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_Chai-1_ligand, 7W55_Chai-1 and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7W57_1.pdb, 7W57_Chai-1
align 7W57_experimental, 7SK4_experimental 
align 7W57_Chai-1, 7W57_experimental
color grey70, chain A and 7W57_Chai-1
color white, chain A and 7W57_experimental
color Chai-1, 7W57_Chai-1 and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_Chai-1_ligand, 7W57_Chai-1 and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_Chai-1_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_Chai-1
set grid_slot, 1, 7SK4_Chai-1_ligand
set grid_slot, 2, 8GY7_experimental
set grid_slot, 2, 8GY7_exp_ligand
set grid_slot, 2, 8GY7_Chai-1
set grid_slot, 2, 8GY7_Chai-1_ligand
set grid_slot, 3, 8XGM_experimental
set grid_slot, 3, 8XGM_exp_ligand
set grid_slot, 3, 8XGM_Chai-1
set grid_slot, 3, 8XGM_Chai-1_ligand
set grid_slot, 4, 7WQ4_experimental
set grid_slot, 4, 7WQ4_exp_ligand
set grid_slot, 4, 7WQ4_Chai-1
set grid_slot, 4, 7WQ4_Chai-1_ligand
set grid_slot, 5, 8WVY_experimental
set grid_slot, 5, 8WVY_exp_ligand
set grid_slot, 5, 8WVY_Chai-1
set grid_slot, 5, 8WVY_Chai-1_ligand
set grid_slot, 6, 8IOC_experimental
set grid_slot, 6, 8IOC_exp_ligand
set grid_slot, 6, 8IOC_Chai-1
set grid_slot, 6, 8IOC_Chai-1_ligand
set grid_slot, 7, 8JGB_experimental
set grid_slot, 7, 8JGB_exp_ligand
set grid_slot, 7, 8JGB_Chai-1
set grid_slot, 7, 8JGB_Chai-1_ligand
set grid_slot, 8, 7W56_experimental
set grid_slot, 8, 7W56_exp_ligand
set grid_slot, 8, 7W56_Chai-1
set grid_slot, 8, 7W56_Chai-1_ligand
set grid_slot, 9, 7W53_experimental
set grid_slot, 9, 7W53_exp_ligand
set grid_slot, 9, 7W53_Chai-1
set grid_slot, 9, 7W53_Chai-1_ligand
set grid_slot, 10, 7W55_experimental
set grid_slot, 10, 7W55_exp_ligand
set grid_slot, 10, 7W55_Chai-1
set grid_slot, 10, 7W55_Chai-1_ligand
set grid_slot, 11, 7W57_experimental
set grid_slot, 11, 7W57_exp_ligand
set grid_slot, 11, 7W57_Chai-1
set grid_slot, 11, 7W57_Chai-1_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
