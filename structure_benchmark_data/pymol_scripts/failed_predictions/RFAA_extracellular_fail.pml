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
set_color RF-AA, [0.651, 0.463, 0.839]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7F6I.pdb, 7F6I_RFAA
align 7F6I_RFAA, 7F6I_experimental
color grey70, chain A and 7F6I_RFAA
color white, chain A and 7F6I_experimental
color RF-AA, 7F6I_RFAA and chain B
color experimental_color, 7F6I_experimental and chain B
create 7F6I_exp_ligand, 7F6I_experimental and chain B
create 7F6I_RFAA_ligand, 7F6I_RFAA and chain B
show cartoon, 7F6I_exp_ligand
show cartoon, 7F6I_RFAA_ligand
set cartoon_oval_width, 0.7, 7F6I_exp_ligand
set cartoon_oval_width, 0.7, 7F6I_RFAA_ligand
set cartoon_loop_radius, 0.7, 7F6I_exp_ligand
set cartoon_loop_radius, 0.7, 7F6I_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HCQ_AB.pdb, 8HCQ_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8HCQ.pdb, 8HCQ_RFAA
align 8HCQ_experimental, 7F6I_experimental 
align 8HCQ_RFAA, 8HCQ_experimental
color grey70, chain A and 8HCQ_RFAA
color white, chain A and 8HCQ_experimental
color RF-AA, 8HCQ_RFAA and chain B
color experimental_color, 8HCQ_experimental and chain B
create 8HCQ_exp_ligand, 8HCQ_experimental and chain B
create 8HCQ_RFAA_ligand, 8HCQ_RFAA and chain B
show cartoon, 8HCQ_exp_ligand
show cartoon, 8HCQ_RFAA_ligand
set cartoon_oval_width, 0.7, 8HCQ_exp_ligand
set cartoon_oval_width, 0.7, 8HCQ_RFAA_ligand
set cartoon_loop_radius, 0.7, 8HCQ_exp_ligand
set cartoon_loop_radius, 0.7, 8HCQ_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8YW4_AB.pdb, 8YW4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8YW4.pdb, 8YW4_RFAA
align 8YW4_experimental, 7F6I_experimental 
align 8YW4_RFAA, 8YW4_experimental
color grey70, chain A and 8YW4_RFAA
color white, chain A and 8YW4_experimental
color RF-AA, 8YW4_RFAA and chain B
color experimental_color, 8YW4_experimental and chain B
create 8YW4_exp_ligand, 8YW4_experimental and chain B
create 8YW4_RFAA_ligand, 8YW4_RFAA and chain B
show cartoon, 8YW4_exp_ligand
show cartoon, 8YW4_RFAA_ligand
set cartoon_oval_width, 0.7, 8YW4_exp_ligand
set cartoon_oval_width, 0.7, 8YW4_RFAA_ligand
set cartoon_loop_radius, 0.7, 8YW4_exp_ligand
set cartoon_loop_radius, 0.7, 8YW4_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7W3Z.pdb, 7W3Z_RFAA
align 7W3Z_experimental, 7F6I_experimental 
align 7W3Z_RFAA, 7W3Z_experimental
color grey70, chain A and 7W3Z_RFAA
color white, chain A and 7W3Z_experimental
color RF-AA, 7W3Z_RFAA and chain B
color experimental_color, 7W3Z_experimental and chain B
create 7W3Z_exp_ligand, 7W3Z_experimental and chain B
create 7W3Z_RFAA_ligand, 7W3Z_RFAA and chain B
show cartoon, 7W3Z_exp_ligand
show cartoon, 7W3Z_RFAA_ligand
set cartoon_oval_width, 0.7, 7W3Z_exp_ligand
set cartoon_oval_width, 0.7, 7W3Z_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W3Z_exp_ligand
set cartoon_loop_radius, 0.7, 7W3Z_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8WVY.pdb, 8WVY_RFAA
align 8WVY_experimental, 7F6I_experimental 
align 8WVY_RFAA, 8WVY_experimental
color grey70, chain A and 8WVY_RFAA
color white, chain A and 8WVY_experimental
color RF-AA, 8WVY_RFAA and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_RFAA_ligand, 8WVY_RFAA and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_RFAA_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_RFAA_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8INR_AB.pdb, 8INR_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8INR.pdb, 8INR_RFAA
align 8INR_experimental, 7F6I_experimental 
align 8INR_RFAA, 8INR_experimental
color grey70, chain A and 8INR_RFAA
color white, chain A and 8INR_experimental
color RF-AA, 8INR_RFAA and chain B
color experimental_color, 8INR_experimental and chain B
create 8INR_exp_ligand, 8INR_experimental and chain B
create 8INR_RFAA_ligand, 8INR_RFAA and chain B
show cartoon, 8INR_exp_ligand
show cartoon, 8INR_RFAA_ligand
set cartoon_oval_width, 0.7, 8INR_exp_ligand
set cartoon_oval_width, 0.7, 8INR_RFAA_ligand
set cartoon_loop_radius, 0.7, 8INR_exp_ligand
set cartoon_loop_radius, 0.7, 8INR_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7W56.pdb, 7W56_RFAA
align 7W56_experimental, 7F6I_experimental 
align 7W56_RFAA, 7W56_experimental
color grey70, chain A and 7W56_RFAA
color white, chain A and 7W56_experimental
color RF-AA, 7W56_RFAA and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_RFAA_ligand, 7W56_RFAA and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_RFAA_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_RFAA_ligand



set grid_mode, 1
set grid_slot, 1, 7F6I_experimental
set grid_slot, 1, 7F6I_exp_ligand
set grid_slot, 1, 7F6I_RFAA
set grid_slot, 1, 7F6I_RFAA_ligand
set grid_slot, 2, 8HCQ_experimental
set grid_slot, 2, 8HCQ_exp_ligand
set grid_slot, 2, 8HCQ_RFAA
set grid_slot, 2, 8HCQ_RFAA_ligand
set grid_slot, 3, 8YW4_experimental
set grid_slot, 3, 8YW4_exp_ligand
set grid_slot, 3, 8YW4_RFAA
set grid_slot, 3, 8YW4_RFAA_ligand
set grid_slot, 4, 7W3Z_experimental
set grid_slot, 4, 7W3Z_exp_ligand
set grid_slot, 4, 7W3Z_RFAA
set grid_slot, 4, 7W3Z_RFAA_ligand
set grid_slot, 5, 8WVY_experimental
set grid_slot, 5, 8WVY_exp_ligand
set grid_slot, 5, 8WVY_RFAA
set grid_slot, 5, 8WVY_RFAA_ligand
set grid_slot, 6, 8INR_experimental
set grid_slot, 6, 8INR_exp_ligand
set grid_slot, 6, 8INR_RFAA
set grid_slot, 6, 8INR_RFAA_ligand
set grid_slot, 7, 7W56_experimental
set grid_slot, 7, 7W56_exp_ligand
set grid_slot, 7, 7W56_RFAA
set grid_slot, 7, 7W56_RFAA_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
