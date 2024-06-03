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


set_color 7P00_af2_color, [0.067, 0.318, 0.522]
set_color 7P00_af3_color, [0.024, 0.122, 0.290]
set_color 7P00_af2_nt_color, [0.000, 0.561, 0.843]
set_color 7P00_experimental_color, [0.976, 0.667, 0.263]
set_color 7P00_rfaa_color, [0.651, 0.463, 0.839]
set_color 7P00_rfaa_nt_color, [0.451, 0.322, 0.749]
set grid_mode, 1



load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/AF2/7P00.pdb, 7P00_af2
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/AF2_no_templates/7P00.pdb, 7P00_af2_no_templates
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/AF3/7P00.pdb, 7P00_af3
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7P00_AB.pdb, 7P00_experimental
color 7P00_af2_color, 7P00_af2 and chain B
color 7P00_af2_nt_color, 7P00_af2_no_templates and chain B
color 7P00_af3_color, 7P00_af3 and chain B



load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/RFAA_chain/7P00.pdb, 7P00_rfaa
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7P00_no_templates.pdb, 7P00_rfaa_no_templates
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7P00_AB.pdb, 7P00_experimental_2
color white, chain A
color 7P00_rfaa_color, 7P00_rfaa and chain B
color 7P00_rfaa_nt_color, 7P00_rfaa_no_templates and chain B
color 7P00_experimental_color, 7P00_experimental_2 and chain B
color 7P00_experimental_color, 7P00_experimental and chain B
color grey60, 7P00_experimental_2 and chain A
color grey60, 7P00_experimental and chain A
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
alignto 7P00_experimental
center
set grid_slot, 1, 7P00_experimental
set grid_slot, 2, 7P00_af2
set grid_slot, 2, 7P00_af2_no_templates
set grid_slot, 2, 7P00_af3
set grid_slot, 3, 7P00_rfaa
set grid_slot, 3, 7P00_rfaa_no_templates
set grid_slot, 1, 7P00_experimental_2
