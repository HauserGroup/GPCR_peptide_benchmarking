reinit
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


set_color receptor_color, [11.000, 61.000, 145.000]
set_color ligand_color, [249.000, 170.000, 67.000]
load '/Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb'
select 7W53_AB_selection, 7W53_AB
select 7W53_AB_ligand, 7W53_AB_selection and chain B
select 7W53_AB_receptor, 7W53_AB_selection and chain A
sel binding_site_7W53, 7W53_AB_selection and chain A and resi 60+141+196+220+317+338+342
color white, 7W53_AB_selection and chain A
color ligand_color, 7W53_AB_ligand 
color receptor_color, binding_site_7W53 
show cartoon, 7W53_AB_selection
show sticks, binding_site_7W53
deselect 
create 7W53_ligand, 7W53_AB_selection and chain B
hide cartoon, 7W53_AB_ligand
show cartoon, 7W53_ligand
set cartoon_oval_width, 0.5, 7W53_ligand
set cartoon_loop_radius, 0.5, 7W53_ligand
center 7W53_AB_selection
zoom
