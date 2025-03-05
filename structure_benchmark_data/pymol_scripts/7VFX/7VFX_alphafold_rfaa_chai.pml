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


set_color 7VFX_af2_color, [0.067, 0.318, 0.522]
set_color 7VFX_af3_color, [0.024, 0.122, 0.290]
set_color 7VFX_af3_nt_color, [0.043, 0.075, 0.129]
set_color 7VFX_af3_server_color, [0.031, 0.055, 0.090]
set_color 7VFX_af2_nt_color, [0.000, 0.561, 0.843]
set_color 7VFX_experimental_color, [0.976, 0.667, 0.263]
set_color 7VFX_rfaa_color, [0.651, 0.463, 0.839]
set_color 7VFX_rfaa_nt_color, [0.451, 0.322, 0.749]
set_color 7VFX_chai_color, [0.522, 0.369, 0.251]
set grid_mode, 1



load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VFX_AB.pdb, 7VFX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF2/7VFX_1.pdb, 7VFX_af2
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF2_no_templates/7VFX_1.pdb, 7VFX_af2_no_templates
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3/7VFX_1.pdb, 7VFX_af3
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_no_templates/7VFX_1.pdb, 7VFX_af3_no_templates
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/AF3_server/7VFX.pdb, 7VFX_af3_server
color 7VFX_af2_color, 7VFX_af2 and chain B
color 7VFX_af2_nt_color, 7VFX_af2_no_templates and chain B
color 7VFX_af3_color, 7VFX_af3 and chain B
color 7VFX_af3_nt_color, 7VFX_af3_no_templates and chain B
color 7VFX_af3_server_color, 7VFX_af3_server and chain B



load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7VFX.pdb, 7VFX_rfaa
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7VFX_no_templates.pdb, 7VFX_rfaa_no_templates
color white, chain A
color 7VFX_rfaa_color, 7VFX_rfaa and chain B
color 7VFX_rfaa_nt_color, 7VFX_rfaa_no_templates and chain B



load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/Chai-1/7VFX_1.pdb, 7VFX_chai
color white, chain A
color 7VFX_chai_color, 7VFX_chai and chain B
color 7VFX_experimental_color, 7VFX_experimental and chain B
color grey60, 7VFX_experimental and chain A
alignto 7VFX_experimental
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
hide everything, chain B
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
create 7VFX_exp_ligand, 7VFX_experimental and chain B
create 7VFX_rfaa_ligand, 7VFX_rfaa and chain B
create 7VFX_rfaa_nt_ligand, 7VFX_rfaa_no_templates and chain B
create 7VFX_af2_ligand, 7VFX_af2 and chain B
create 7VFX_af2_nt_ligand, 7VFX_af2_no_templates and chain B
create 7VFX_af3_ligand, 7VFX_af3 and chain B
create 7VFX_af3_nt_ligand, 7VFX_af3_no_templates and chain B
create 7VFX_af3_server_ligand, 7VFX_af3_server and chain B
create 7VFX_chai_ligand, 7VFX_chai and chain B
show cartoon, 7VFX_exp_ligand
show cartoon, 7VFX_rfaa_ligand
show cartoon, 7VFX_rfaa_nt_ligand
show cartoon, 7VFX_af3_ligand
show cartoon, 7VFX_af3_nt_ligand
show cartoon, 7VFX_af3_server_ligand
show cartoon, 7VFX_af2_nt_ligand
show cartoon, 7VFX_af2_ligand
show cartoon, 7VFX_chai_ligand
set cartoon_oval_width, 0.7, 7VFX_exp_ligand
set cartoon_oval_width, 0.7, 7VFX_af2_ligand
set cartoon_oval_width, 0.7, 7VFX_af2_nt_ligand
set cartoon_oval_width, 0.7, 7VFX_rfaa_ligand
set cartoon_oval_width, 0.7, 7VFX_rfaa_nt_ligand
set cartoon_oval_width, 0.7, 7VFX_af3_ligand
set cartoon_oval_width, 0.7, 7VFX_af3_nt_ligand
set cartoon_oval_width, 0.7, 7VFX_af3_server_ligand
set cartoon_loop_radius, 0.7, 7VFX_exp_ligand
set cartoon_loop_radius, 0.7, 7VFX_af2_ligand
set cartoon_loop_radius, 0.7, 7VFX_af2_nt_ligand
set cartoon_loop_radius, 0.7, 7VFX_rfaa_ligand
set cartoon_loop_radius, 0.7, 7VFX_rfaa_nt_ligand
set cartoon_loop_radius, 0.7, 7VFX_af3_ligand
set cartoon_loop_radius, 0.7, 7VFX_af3_nt_ligand
set cartoon_loop_radius, 0.7, 7VFX_af3_server_ligand
set cartoon_loop_radius, 0.7, 7VFX_chai_ligand
set grid_slot, 1, 7VFX_experimental
set grid_slot, 1, 7VFX_exp_ligand
set grid_slot, 2, 7VFX_rfaa
set grid_slot, 2, 7VFX_rfaa_no_templates
set grid_slot, 2, 7VFX_rfaa_ligand
set grid_slot, 2, 7VFX_rfaa_nt_ligand
set grid_slot, 3, 7VFX_chai
set grid_slot, 3, 7VFX_chai_ligand
set grid_slot, 4, 7VFX_af2
set grid_slot, 4, 7VFX_af2_ligand
set grid_slot, 4, 7VFX_af2_no_templates
set grid_slot, 4, 7VFX_af2_nt_ligand
set grid_slot, 4, 7VFX_af3
set grid_slot, 4, 7VFX_af3_ligand
set grid_slot, 4, 7VFX_af3_no_templates
set grid_slot, 4, 7VFX_af3_nt_ligand
set grid_slot, 4, 7VFX_af3_server
set grid_slot, 4, 7VFX_af3_server_ligand
center 7VFX_experimental
zoom
