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
set_color AF3 (no templates), [0.043, 0.075, 0.129]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/7SK4_1.pdb, 7SK4_AF3_no_templates
align 7SK4_AF3_no_templates, 7SK4_experimental
color grey70, chain A and 7SK4_AF3_no_templates
color white, chain A and 7SK4_experimental
color AF3 (no templates), 7SK4_AF3_no_templates and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_AF3_no_templates_ligand, 7SK4_AF3_no_templates and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGM_AB.pdb, 8XGM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/8XGM_1.pdb, 8XGM_AF3_no_templates
align 8XGM_experimental, 7SK4_experimental 
align 8XGM_AF3_no_templates, 8XGM_experimental
color grey70, chain A and 8XGM_AF3_no_templates
color white, chain A and 8XGM_experimental
color AF3 (no templates), 8XGM_AF3_no_templates and chain B
color experimental_color, 8XGM_experimental and chain B
create 8XGM_exp_ligand, 8XGM_experimental and chain B
create 8XGM_AF3_no_templates_ligand, 8XGM_AF3_no_templates and chain B
show cartoon, 8XGM_exp_ligand
show cartoon, 8XGM_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 8XGM_exp_ligand
set cartoon_oval_width, 0.7, 8XGM_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 8XGM_exp_ligand
set cartoon_loop_radius, 0.7, 8XGM_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/8WVY_1.pdb, 8WVY_AF3_no_templates
align 8WVY_experimental, 7SK4_experimental 
align 8WVY_AF3_no_templates, 8WVY_experimental
color grey70, chain A and 8WVY_AF3_no_templates
color white, chain A and 8WVY_experimental
color AF3 (no templates), 8WVY_AF3_no_templates and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_AF3_no_templates_ligand, 8WVY_AF3_no_templates and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGF_AB.pdb, 8JGF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/8JGF_1.pdb, 8JGF_AF3_no_templates
align 8JGF_experimental, 7SK4_experimental 
align 8JGF_AF3_no_templates, 8JGF_experimental
color grey70, chain A and 8JGF_AF3_no_templates
color white, chain A and 8JGF_experimental
color AF3 (no templates), 8JGF_AF3_no_templates and chain B
color experimental_color, 8JGF_experimental and chain B
create 8JGF_exp_ligand, 8JGF_experimental and chain B
create 8JGF_AF3_no_templates_ligand, 8JGF_AF3_no_templates and chain B
show cartoon, 8JGF_exp_ligand
show cartoon, 8JGF_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 8JGF_exp_ligand
set cartoon_oval_width, 0.7, 8JGF_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 8JGF_exp_ligand
set cartoon_loop_radius, 0.7, 8JGF_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGB_AB.pdb, 8JGB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/8JGB_1.pdb, 8JGB_AF3_no_templates
align 8JGB_experimental, 7SK4_experimental 
align 8JGB_AF3_no_templates, 8JGB_experimental
color grey70, chain A and 8JGB_AF3_no_templates
color white, chain A and 8JGB_experimental
color AF3 (no templates), 8JGB_AF3_no_templates and chain B
color experimental_color, 8JGB_experimental and chain B
create 8JGB_exp_ligand, 8JGB_experimental and chain B
create 8JGB_AF3_no_templates_ligand, 8JGB_AF3_no_templates and chain B
show cartoon, 8JGB_exp_ligand
show cartoon, 8JGB_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 8JGB_exp_ligand
set cartoon_oval_width, 0.7, 8JGB_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 8JGB_exp_ligand
set cartoon_loop_radius, 0.7, 8JGB_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XWO_AB.pdb, 7XWO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/7XWO_1.pdb, 7XWO_AF3_no_templates
align 7XWO_experimental, 7SK4_experimental 
align 7XWO_AF3_no_templates, 7XWO_experimental
color grey70, chain A and 7XWO_AF3_no_templates
color white, chain A and 7XWO_experimental
color AF3 (no templates), 7XWO_AF3_no_templates and chain B
color experimental_color, 7XWO_experimental and chain B
create 7XWO_exp_ligand, 7XWO_experimental and chain B
create 7XWO_AF3_no_templates_ligand, 7XWO_AF3_no_templates and chain B
show cartoon, 7XWO_exp_ligand
show cartoon, 7XWO_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 7XWO_exp_ligand
set cartoon_oval_width, 0.7, 7XWO_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 7XWO_exp_ligand
set cartoon_loop_radius, 0.7, 7XWO_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/7W57_1.pdb, 7W57_AF3_no_templates
align 7W57_experimental, 7SK4_experimental 
align 7W57_AF3_no_templates, 7W57_experimental
color grey70, chain A and 7W57_AF3_no_templates
color white, chain A and 7W57_experimental
color AF3 (no templates), 7W57_AF3_no_templates and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_AF3_no_templates_ligand, 7W57_AF3_no_templates and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_AF3_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RYC_AB.pdb, 7RYC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/7RYC_1.pdb, 7RYC_AF3_no_templates
align 7RYC_experimental, 7SK4_experimental 
align 7RYC_AF3_no_templates, 7RYC_experimental
color grey70, chain A and 7RYC_AF3_no_templates
color white, chain A and 7RYC_experimental
color AF3 (no templates), 7RYC_AF3_no_templates and chain B
color experimental_color, 7RYC_experimental and chain B
create 7RYC_exp_ligand, 7RYC_experimental and chain B
create 7RYC_AF3_no_templates_ligand, 7RYC_AF3_no_templates and chain B
show cartoon, 7RYC_exp_ligand
show cartoon, 7RYC_AF3_no_templates_ligand
set cartoon_oval_width, 0.7, 7RYC_exp_ligand
set cartoon_oval_width, 0.7, 7RYC_AF3_no_templates_ligand
set cartoon_loop_radius, 0.7, 7RYC_exp_ligand
set cartoon_loop_radius, 0.7, 7RYC_AF3_no_templates_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_AF3_no_templates
set grid_slot, 1, 7SK4_AF3_no_templates_ligand
set grid_slot, 2, 8XGM_experimental
set grid_slot, 2, 8XGM_exp_ligand
set grid_slot, 2, 8XGM_AF3_no_templates
set grid_slot, 2, 8XGM_AF3_no_templates_ligand
set grid_slot, 3, 8WVY_experimental
set grid_slot, 3, 8WVY_exp_ligand
set grid_slot, 3, 8WVY_AF3_no_templates
set grid_slot, 3, 8WVY_AF3_no_templates_ligand
set grid_slot, 4, 8JGF_experimental
set grid_slot, 4, 8JGF_exp_ligand
set grid_slot, 4, 8JGF_AF3_no_templates
set grid_slot, 4, 8JGF_AF3_no_templates_ligand
set grid_slot, 5, 8JGB_experimental
set grid_slot, 5, 8JGB_exp_ligand
set grid_slot, 5, 8JGB_AF3_no_templates
set grid_slot, 5, 8JGB_AF3_no_templates_ligand
set grid_slot, 6, 7XWO_experimental
set grid_slot, 6, 7XWO_exp_ligand
set grid_slot, 6, 7XWO_AF3_no_templates
set grid_slot, 6, 7XWO_AF3_no_templates_ligand
set grid_slot, 7, 7W57_experimental
set grid_slot, 7, 7W57_exp_ligand
set grid_slot, 7, 7W57_AF3_no_templates
set grid_slot, 7, 7W57_AF3_no_templates_ligand
set grid_slot, 8, 7RYC_experimental
set grid_slot, 8, 7RYC_exp_ligand
set grid_slot, 8, 7RYC_AF3_no_templates
set grid_slot, 8, 7RYC_AF3_no_templates_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
