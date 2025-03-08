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
set_color AF3_server, [0.008, 0.749, 0.906]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGF_AB.pdb, 8JGF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/8JGF.pdb, 8JGF_AF3_server
align 8JGF_AF3_server, 8JGF_experimental
color grey70, chain A and 8JGF_AF3_server
color white, chain A and 8JGF_experimental
color AF3_server, 8JGF_AF3_server and chain B
color experimental_color, 8JGF_experimental and chain B
create 8JGF_exp_ligand, 8JGF_experimental and chain B
create 8JGF_AF3_server_ligand, 8JGF_AF3_server and chain B
show cartoon, 8JGF_exp_ligand
show cartoon, 8JGF_AF3_server_ligand
set cartoon_oval_width, 0.7, 8JGF_exp_ligand
set cartoon_oval_width, 0.7, 8JGF_AF3_server_ligand
set cartoon_loop_radius, 0.7, 8JGF_exp_ligand
set cartoon_loop_radius, 0.7, 8JGF_AF3_server_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGB_AB.pdb, 8JGB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/8JGB.pdb, 8JGB_AF3_server
align 8JGB_experimental, 8JGF_experimental 
align 8JGB_AF3_server, 8JGB_experimental
color grey70, chain A and 8JGB_AF3_server
color white, chain A and 8JGB_experimental
color AF3_server, 8JGB_AF3_server and chain B
color experimental_color, 8JGB_experimental and chain B
create 8JGB_exp_ligand, 8JGB_experimental and chain B
create 8JGB_AF3_server_ligand, 8JGB_AF3_server and chain B
show cartoon, 8JGB_exp_ligand
show cartoon, 8JGB_AF3_server_ligand
set cartoon_oval_width, 0.7, 8JGB_exp_ligand
set cartoon_oval_width, 0.7, 8JGB_AF3_server_ligand
set cartoon_loop_radius, 0.7, 8JGB_exp_ligand
set cartoon_loop_radius, 0.7, 8JGB_AF3_server_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8U26_AB.pdb, 8U26_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/8U26.pdb, 8U26_AF3_server
align 8U26_experimental, 8JGF_experimental 
align 8U26_AF3_server, 8U26_experimental
color grey70, chain A and 8U26_AF3_server
color white, chain A and 8U26_experimental
color AF3_server, 8U26_AF3_server and chain B
color experimental_color, 8U26_experimental and chain B
create 8U26_exp_ligand, 8U26_experimental and chain B
create 8U26_AF3_server_ligand, 8U26_AF3_server and chain B
show cartoon, 8U26_exp_ligand
show cartoon, 8U26_AF3_server_ligand
set cartoon_oval_width, 0.7, 8U26_exp_ligand
set cartoon_oval_width, 0.7, 8U26_AF3_server_ligand
set cartoon_loop_radius, 0.7, 8U26_exp_ligand
set cartoon_loop_radius, 0.7, 8U26_AF3_server_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XWO_AB.pdb, 7XWO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/7XWO.pdb, 7XWO_AF3_server
align 7XWO_experimental, 8JGF_experimental 
align 7XWO_AF3_server, 7XWO_experimental
color grey70, chain A and 7XWO_AF3_server
color white, chain A and 7XWO_experimental
color AF3_server, 7XWO_AF3_server and chain B
color experimental_color, 7XWO_experimental and chain B
create 7XWO_exp_ligand, 7XWO_experimental and chain B
create 7XWO_AF3_server_ligand, 7XWO_AF3_server and chain B
show cartoon, 7XWO_exp_ligand
show cartoon, 7XWO_AF3_server_ligand
set cartoon_oval_width, 0.7, 7XWO_exp_ligand
set cartoon_oval_width, 0.7, 7XWO_AF3_server_ligand
set cartoon_loop_radius, 0.7, 7XWO_exp_ligand
set cartoon_loop_radius, 0.7, 7XWO_AF3_server_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/7W56.pdb, 7W56_AF3_server
align 7W56_experimental, 8JGF_experimental 
align 7W56_AF3_server, 7W56_experimental
color grey70, chain A and 7W56_AF3_server
color white, chain A and 7W56_experimental
color AF3_server, 7W56_AF3_server and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_AF3_server_ligand, 7W56_AF3_server and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_AF3_server_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_AF3_server_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_AF3_server_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RYC_AB.pdb, 7RYC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/7RYC.pdb, 7RYC_AF3_server
align 7RYC_experimental, 8JGF_experimental 
align 7RYC_AF3_server, 7RYC_experimental
color grey70, chain A and 7RYC_AF3_server
color white, chain A and 7RYC_experimental
color AF3_server, 7RYC_AF3_server and chain B
color experimental_color, 7RYC_experimental and chain B
create 7RYC_exp_ligand, 7RYC_experimental and chain B
create 7RYC_AF3_server_ligand, 7RYC_AF3_server and chain B
show cartoon, 7RYC_exp_ligand
show cartoon, 7RYC_AF3_server_ligand
set cartoon_oval_width, 0.7, 7RYC_exp_ligand
set cartoon_oval_width, 0.7, 7RYC_AF3_server_ligand
set cartoon_loop_radius, 0.7, 7RYC_exp_ligand
set cartoon_loop_radius, 0.7, 7RYC_AF3_server_ligand



set grid_mode, 1
set grid_slot, 1, 8JGF_experimental
set grid_slot, 1, 8JGF_exp_ligand
set grid_slot, 1, 8JGF_AF3_server
set grid_slot, 1, 8JGF_AF3_server_ligand
set grid_slot, 2, 8JGB_experimental
set grid_slot, 2, 8JGB_exp_ligand
set grid_slot, 2, 8JGB_AF3_server
set grid_slot, 2, 8JGB_AF3_server_ligand
set grid_slot, 3, 8U26_experimental
set grid_slot, 3, 8U26_exp_ligand
set grid_slot, 3, 8U26_AF3_server
set grid_slot, 3, 8U26_AF3_server_ligand
set grid_slot, 4, 7XWO_experimental
set grid_slot, 4, 7XWO_exp_ligand
set grid_slot, 4, 7XWO_AF3_server
set grid_slot, 4, 7XWO_AF3_server_ligand
set grid_slot, 5, 7W56_experimental
set grid_slot, 5, 7W56_exp_ligand
set grid_slot, 5, 7W56_AF3_server
set grid_slot, 5, 7W56_AF3_server_ligand
set grid_slot, 6, 7RYC_experimental
set grid_slot, 6, 7RYC_exp_ligand
set grid_slot, 6, 7RYC_AF3_server
set grid_slot, 6, 7RYC_AF3_server_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
