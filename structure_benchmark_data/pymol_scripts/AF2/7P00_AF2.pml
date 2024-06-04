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


load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/AF2/7P00.pdb, 7P00_prediction
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7P00_AB.pdb, 7P00_experimental
alignto 7P00_experimental
center
set_color 7P00_prediction_color, [0.067, 0.318, 0.522]
color white, chain A
color 7P00_prediction_color, 7P00_prediction and chain B
color grey70, 7P00_experimental
set cartoon_transparency, 0.25, 7P00_experimental and chain A
set cartoon_transparency, 0.25, 7P00_prediction and chain A
create 7P00_exp_ligand, 7P00_experimental and chain B
create 7P00_pred_ligand, 7P00_prediction and chain B
set cartoon_loop_radius, 0.7, 7P00_exp_ligand
set cartoon_loop_radius, 0.7, 7P00_pred_ligand
hide (hydro)
hide everything, not polymer
