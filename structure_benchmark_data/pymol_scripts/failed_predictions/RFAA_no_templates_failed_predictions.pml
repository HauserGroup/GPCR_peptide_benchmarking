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
set_color RF-AA (no templates), [0.451, 0.322, 0.749]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7F6I_no_templates.pdb, 7F6I_RFAA_no_templates
align 7F6I_RFAA_no_templates, 7F6I_experimental
color grey70, chain A and 7F6I_RFAA_no_templates
color white, chain A and 7F6I_experimental
color RF-AA (no templates), 7F6I_RFAA_no_templates and chain B
color experimental_color, 7F6I_experimental and chain B
create 7F6I_exp_ligand, 7F6I_experimental and chain B
create 7F6I_RFAA_no_templates_ligand, 7F6I_RFAA_no_templates and chain B
show cartoon, 7F6I_exp_ligand
show cartoon, 7F6I_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7F6I_exp_ligand
set cartoon_oval_width, 0.7, 7F6I_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7F6I_exp_ligand
set cartoon_loop_radius, 0.7, 7F6I_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8IA8_no_templates.pdb, 8IA8_RFAA_no_templates
align 8IA8_experimental, 7F6I_experimental 
align 8IA8_RFAA_no_templates, 8IA8_experimental
color grey70, chain A and 8IA8_RFAA_no_templates
color white, chain A and 8IA8_experimental
color RF-AA (no templates), 8IA8_RFAA_no_templates and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_RFAA_no_templates_ligand, 8IA8_RFAA_no_templates and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8I95_AB.pdb, 8I95_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8I95_no_templates.pdb, 8I95_RFAA_no_templates
align 8I95_experimental, 7F6I_experimental 
align 8I95_RFAA_no_templates, 8I95_experimental
color grey70, chain A and 8I95_RFAA_no_templates
color white, chain A and 8I95_experimental
color RF-AA (no templates), 8I95_RFAA_no_templates and chain B
color experimental_color, 8I95_experimental and chain B
create 8I95_exp_ligand, 8I95_experimental and chain B
create 8I95_RFAA_no_templates_ligand, 8I95_RFAA_no_templates and chain B
show cartoon, 8I95_exp_ligand
show cartoon, 8I95_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8I95_exp_ligand
set cartoon_oval_width, 0.7, 8I95_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8I95_exp_ligand
set cartoon_loop_radius, 0.7, 8I95_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8HK2_no_templates.pdb, 8HK2_RFAA_no_templates
align 8HK2_experimental, 7F6I_experimental 
align 8HK2_RFAA_no_templates, 8HK2_experimental
color grey70, chain A and 8HK2_RFAA_no_templates
color white, chain A and 8HK2_experimental
color RF-AA (no templates), 8HK2_RFAA_no_templates and chain B
color experimental_color, 8HK2_experimental and chain B
create 8HK2_exp_ligand, 8HK2_experimental and chain B
create 8HK2_RFAA_no_templates_ligand, 8HK2_RFAA_no_templates and chain B
show cartoon, 8HK2_exp_ligand
show cartoon, 8HK2_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8HK2_exp_ligand
set cartoon_oval_width, 0.7, 8HK2_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8HK2_exp_ligand
set cartoon_loop_radius, 0.7, 8HK2_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGM_AB.pdb, 8XGM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8XGM_no_templates.pdb, 8XGM_RFAA_no_templates
align 8XGM_experimental, 7F6I_experimental 
align 8XGM_RFAA_no_templates, 8XGM_experimental
color grey70, chain A and 8XGM_RFAA_no_templates
color white, chain A and 8XGM_experimental
color RF-AA (no templates), 8XGM_RFAA_no_templates and chain B
color experimental_color, 8XGM_experimental and chain B
create 8XGM_exp_ligand, 8XGM_experimental and chain B
create 8XGM_RFAA_no_templates_ligand, 8XGM_RFAA_no_templates and chain B
show cartoon, 8XGM_exp_ligand
show cartoon, 8XGM_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8XGM_exp_ligand
set cartoon_oval_width, 0.7, 8XGM_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8XGM_exp_ligand
set cartoon_loop_radius, 0.7, 8XGM_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7W3Z_no_templates.pdb, 7W3Z_RFAA_no_templates
align 7W3Z_experimental, 7F6I_experimental 
align 7W3Z_RFAA_no_templates, 7W3Z_experimental
color grey70, chain A and 7W3Z_RFAA_no_templates
color white, chain A and 7W3Z_experimental
color RF-AA (no templates), 7W3Z_RFAA_no_templates and chain B
color experimental_color, 7W3Z_experimental and chain B
create 7W3Z_exp_ligand, 7W3Z_experimental and chain B
create 7W3Z_RFAA_no_templates_ligand, 7W3Z_RFAA_no_templates and chain B
show cartoon, 7W3Z_exp_ligand
show cartoon, 7W3Z_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W3Z_exp_ligand
set cartoon_oval_width, 0.7, 7W3Z_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W3Z_exp_ligand
set cartoon_loop_radius, 0.7, 7W3Z_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8WVY_no_templates.pdb, 8WVY_RFAA_no_templates
align 8WVY_experimental, 7F6I_experimental 
align 8WVY_RFAA_no_templates, 8WVY_experimental
color grey70, chain A and 8WVY_RFAA_no_templates
color white, chain A and 8WVY_experimental
color RF-AA (no templates), 8WVY_RFAA_no_templates and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_RFAA_no_templates_ligand, 8WVY_RFAA_no_templates and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGF_AB.pdb, 8JGF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8JGF_no_templates.pdb, 8JGF_RFAA_no_templates
align 8JGF_experimental, 7F6I_experimental 
align 8JGF_RFAA_no_templates, 8JGF_experimental
color grey70, chain A and 8JGF_RFAA_no_templates
color white, chain A and 8JGF_experimental
color RF-AA (no templates), 8JGF_RFAA_no_templates and chain B
color experimental_color, 8JGF_experimental and chain B
create 8JGF_exp_ligand, 8JGF_experimental and chain B
create 8JGF_RFAA_no_templates_ligand, 8JGF_RFAA_no_templates and chain B
show cartoon, 8JGF_exp_ligand
show cartoon, 8JGF_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8JGF_exp_ligand
set cartoon_oval_width, 0.7, 8JGF_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8JGF_exp_ligand
set cartoon_loop_radius, 0.7, 8JGF_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7S8L_no_templates.pdb, 7S8L_RFAA_no_templates
align 7S8L_experimental, 7F6I_experimental 
align 7S8L_RFAA_no_templates, 7S8L_experimental
color grey70, chain A and 7S8L_RFAA_no_templates
color white, chain A and 7S8L_experimental
color RF-AA (no templates), 7S8L_RFAA_no_templates and chain B
color experimental_color, 7S8L_experimental and chain B
create 7S8L_exp_ligand, 7S8L_experimental and chain B
create 7S8L_RFAA_no_templates_ligand, 7S8L_RFAA_no_templates and chain B
show cartoon, 7S8L_exp_ligand
show cartoon, 7S8L_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7S8L_exp_ligand
set cartoon_oval_width, 0.7, 7S8L_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7S8L_exp_ligand
set cartoon_loop_radius, 0.7, 7S8L_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VDM_AB.pdb, 7VDM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7VDM_no_templates.pdb, 7VDM_RFAA_no_templates
align 7VDM_experimental, 7F6I_experimental 
align 7VDM_RFAA_no_templates, 7VDM_experimental
color grey70, chain A and 7VDM_RFAA_no_templates
color white, chain A and 7VDM_experimental
color RF-AA (no templates), 7VDM_RFAA_no_templates and chain B
color experimental_color, 7VDM_experimental and chain B
create 7VDM_exp_ligand, 7VDM_experimental and chain B
create 7VDM_RFAA_no_templates_ligand, 7VDM_RFAA_no_templates and chain B
show cartoon, 7VDM_exp_ligand
show cartoon, 7VDM_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7VDM_exp_ligand
set cartoon_oval_width, 0.7, 7VDM_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7VDM_exp_ligand
set cartoon_loop_radius, 0.7, 7VDM_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VV0_AB.pdb, 7VV0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7VV0_no_templates.pdb, 7VV0_RFAA_no_templates
align 7VV0_experimental, 7F6I_experimental 
align 7VV0_RFAA_no_templates, 7VV0_experimental
color grey70, chain A and 7VV0_RFAA_no_templates
color white, chain A and 7VV0_experimental
color RF-AA (no templates), 7VV0_RFAA_no_templates and chain B
color experimental_color, 7VV0_experimental and chain B
create 7VV0_exp_ligand, 7VV0_experimental and chain B
create 7VV0_RFAA_no_templates_ligand, 7VV0_RFAA_no_templates and chain B
show cartoon, 7VV0_exp_ligand
show cartoon, 7VV0_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7VV0_exp_ligand
set cartoon_oval_width, 0.7, 7VV0_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7VV0_exp_ligand
set cartoon_loop_radius, 0.7, 7VV0_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IBV_AB.pdb, 8IBV_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8IBV_no_templates.pdb, 8IBV_RFAA_no_templates
align 8IBV_experimental, 7F6I_experimental 
align 8IBV_RFAA_no_templates, 8IBV_experimental
color grey70, chain A and 8IBV_RFAA_no_templates
color white, chain A and 8IBV_experimental
color RF-AA (no templates), 8IBV_RFAA_no_templates and chain B
color experimental_color, 8IBV_experimental and chain B
create 8IBV_exp_ligand, 8IBV_experimental and chain B
create 8IBV_RFAA_no_templates_ligand, 8IBV_RFAA_no_templates and chain B
show cartoon, 8IBV_exp_ligand
show cartoon, 8IBV_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8IBV_exp_ligand
set cartoon_oval_width, 0.7, 8IBV_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8IBV_exp_ligand
set cartoon_loop_radius, 0.7, 8IBV_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XWO_AB.pdb, 7XWO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7XWO_no_templates.pdb, 7XWO_RFAA_no_templates
align 7XWO_experimental, 7F6I_experimental 
align 7XWO_RFAA_no_templates, 7XWO_experimental
color grey70, chain A and 7XWO_RFAA_no_templates
color white, chain A and 7XWO_experimental
color RF-AA (no templates), 7XWO_RFAA_no_templates and chain B
color experimental_color, 7XWO_experimental and chain B
create 7XWO_exp_ligand, 7XWO_experimental and chain B
create 7XWO_RFAA_no_templates_ligand, 7XWO_RFAA_no_templates and chain B
show cartoon, 7XWO_exp_ligand
show cartoon, 7XWO_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7XWO_exp_ligand
set cartoon_oval_width, 0.7, 7XWO_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7XWO_exp_ligand
set cartoon_loop_radius, 0.7, 7XWO_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8H0P_AB.pdb, 8H0P_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8H0P_no_templates.pdb, 8H0P_RFAA_no_templates
align 8H0P_experimental, 7F6I_experimental 
align 8H0P_RFAA_no_templates, 8H0P_experimental
color grey70, chain A and 8H0P_RFAA_no_templates
color white, chain A and 8H0P_experimental
color RF-AA (no templates), 8H0P_RFAA_no_templates and chain B
color experimental_color, 8H0P_experimental and chain B
create 8H0P_exp_ligand, 8H0P_experimental and chain B
create 8H0P_RFAA_no_templates_ligand, 8H0P_RFAA_no_templates and chain B
show cartoon, 8H0P_exp_ligand
show cartoon, 8H0P_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8H0P_exp_ligand
set cartoon_oval_width, 0.7, 8H0P_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8H0P_exp_ligand
set cartoon_loop_radius, 0.7, 8H0P_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7W56_no_templates.pdb, 7W56_RFAA_no_templates
align 7W56_experimental, 7F6I_experimental 
align 7W56_RFAA_no_templates, 7W56_experimental
color grey70, chain A and 7W56_RFAA_no_templates
color white, chain A and 7W56_experimental
color RF-AA (no templates), 7W56_RFAA_no_templates and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_RFAA_no_templates_ligand, 7W56_RFAA_no_templates and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7W53_no_templates.pdb, 7W53_RFAA_no_templates
align 7W53_experimental, 7F6I_experimental 
align 7W53_RFAA_no_templates, 7W53_experimental
color grey70, chain A and 7W53_RFAA_no_templates
color white, chain A and 7W53_experimental
color RF-AA (no templates), 7W53_RFAA_no_templates and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_RFAA_no_templates_ligand, 7W53_RFAA_no_templates and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7W55_no_templates.pdb, 7W55_RFAA_no_templates
align 7W55_experimental, 7F6I_experimental 
align 7W55_RFAA_no_templates, 7W55_experimental
color grey70, chain A and 7W55_RFAA_no_templates
color white, chain A and 7W55_experimental
color RF-AA (no templates), 7W55_RFAA_no_templates and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_RFAA_no_templates_ligand, 7W55_RFAA_no_templates and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7W57_no_templates.pdb, 7W57_RFAA_no_templates
align 7W57_experimental, 7F6I_experimental 
align 7W57_RFAA_no_templates, 7W57_experimental
color grey70, chain A and 7W57_RFAA_no_templates
color white, chain A and 7W57_experimental
color RF-AA (no templates), 7W57_RFAA_no_templates and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_RFAA_no_templates_ligand, 7W57_RFAA_no_templates and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8F7W_no_templates.pdb, 8F7W_RFAA_no_templates
align 8F7W_experimental, 7F6I_experimental 
align 8F7W_RFAA_no_templates, 8F7W_experimental
color grey70, chain A and 8F7W_RFAA_no_templates
color white, chain A and 8F7W_experimental
color RF-AA (no templates), 8F7W_RFAA_no_templates and chain B
color experimental_color, 8F7W_experimental and chain B
create 8F7W_exp_ligand, 8F7W_experimental and chain B
create 8F7W_RFAA_no_templates_ligand, 8F7W_RFAA_no_templates and chain B
show cartoon, 8F7W_exp_ligand
show cartoon, 8F7W_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8F7W_exp_ligand
set cartoon_oval_width, 0.7, 8F7W_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8F7W_exp_ligand
set cartoon_loop_radius, 0.7, 8F7W_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7Q_AB.pdb, 8F7Q_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8F7Q_no_templates.pdb, 8F7Q_RFAA_no_templates
align 8F7Q_experimental, 7F6I_experimental 
align 8F7Q_RFAA_no_templates, 8F7Q_experimental
color grey70, chain A and 8F7Q_RFAA_no_templates
color white, chain A and 8F7Q_experimental
color RF-AA (no templates), 8F7Q_RFAA_no_templates and chain B
color experimental_color, 8F7Q_experimental and chain B
create 8F7Q_exp_ligand, 8F7Q_experimental and chain B
create 8F7Q_RFAA_no_templates_ligand, 8F7Q_RFAA_no_templates and chain B
show cartoon, 8F7Q_exp_ligand
show cartoon, 8F7Q_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8F7Q_exp_ligand
set cartoon_oval_width, 0.7, 8F7Q_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8F7Q_exp_ligand
set cartoon_loop_radius, 0.7, 8F7Q_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8F7X_no_templates.pdb, 8F7X_RFAA_no_templates
align 8F7X_experimental, 7F6I_experimental 
align 8F7X_RFAA_no_templates, 8F7X_experimental
color grey70, chain A and 8F7X_RFAA_no_templates
color white, chain A and 8F7X_experimental
color RF-AA (no templates), 8F7X_RFAA_no_templates and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_RFAA_no_templates_ligand, 8F7X_RFAA_no_templates and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8ZPT_AB.pdb, 8ZPT_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8ZPT_no_templates.pdb, 8ZPT_RFAA_no_templates
align 8ZPT_experimental, 7F6I_experimental 
align 8ZPT_RFAA_no_templates, 8ZPT_experimental
color grey70, chain A and 8ZPT_RFAA_no_templates
color white, chain A and 8ZPT_experimental
color RF-AA (no templates), 8ZPT_RFAA_no_templates and chain B
color experimental_color, 8ZPT_experimental and chain B
create 8ZPT_exp_ligand, 8ZPT_experimental and chain B
create 8ZPT_RFAA_no_templates_ligand, 8ZPT_RFAA_no_templates and chain B
show cartoon, 8ZPT_exp_ligand
show cartoon, 8ZPT_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8ZPT_exp_ligand
set cartoon_oval_width, 0.7, 8ZPT_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8ZPT_exp_ligand
set cartoon_loop_radius, 0.7, 8ZPT_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WZ2_AB.pdb, 8WZ2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8WZ2_no_templates.pdb, 8WZ2_RFAA_no_templates
align 8WZ2_experimental, 7F6I_experimental 
align 8WZ2_RFAA_no_templates, 8WZ2_experimental
color grey70, chain A and 8WZ2_RFAA_no_templates
color white, chain A and 8WZ2_experimental
color RF-AA (no templates), 8WZ2_RFAA_no_templates and chain B
color experimental_color, 8WZ2_experimental and chain B
create 8WZ2_exp_ligand, 8WZ2_experimental and chain B
create 8WZ2_RFAA_no_templates_ligand, 8WZ2_RFAA_no_templates and chain B
show cartoon, 8WZ2_exp_ligand
show cartoon, 8WZ2_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8WZ2_exp_ligand
set cartoon_oval_width, 0.7, 8WZ2_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8WZ2_exp_ligand
set cartoon_loop_radius, 0.7, 8WZ2_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7T10_no_templates.pdb, 7T10_RFAA_no_templates
align 7T10_experimental, 7F6I_experimental 
align 7T10_RFAA_no_templates, 7T10_experimental
color grey70, chain A and 7T10_RFAA_no_templates
color white, chain A and 7T10_experimental
color RF-AA (no templates), 7T10_RFAA_no_templates and chain B
color experimental_color, 7T10_experimental and chain B
create 7T10_exp_ligand, 7T10_experimental and chain B
create 7T10_RFAA_no_templates_ligand, 7T10_RFAA_no_templates and chain B
show cartoon, 7T10_exp_ligand
show cartoon, 7T10_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7T10_exp_ligand
set cartoon_oval_width, 0.7, 7T10_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7T10_exp_ligand
set cartoon_loop_radius, 0.7, 7T10_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T11_AB.pdb, 7T11_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7T11_no_templates.pdb, 7T11_RFAA_no_templates
align 7T11_experimental, 7F6I_experimental 
align 7T11_RFAA_no_templates, 7T11_experimental
color grey70, chain A and 7T11_RFAA_no_templates
color white, chain A and 7T11_experimental
color RF-AA (no templates), 7T11_RFAA_no_templates and chain B
color experimental_color, 7T11_experimental and chain B
create 7T11_exp_ligand, 7T11_experimental and chain B
create 7T11_RFAA_no_templates_ligand, 7T11_RFAA_no_templates and chain B
show cartoon, 7T11_exp_ligand
show cartoon, 7T11_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7T11_exp_ligand
set cartoon_oval_width, 0.7, 7T11_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7T11_exp_ligand
set cartoon_loop_radius, 0.7, 7T11_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XMS_AB.pdb, 7XMS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/7XMS_no_templates.pdb, 7XMS_RFAA_no_templates
align 7XMS_experimental, 7F6I_experimental 
align 7XMS_RFAA_no_templates, 7XMS_experimental
color grey70, chain A and 7XMS_RFAA_no_templates
color white, chain A and 7XMS_experimental
color RF-AA (no templates), 7XMS_RFAA_no_templates and chain B
color experimental_color, 7XMS_experimental and chain B
create 7XMS_exp_ligand, 7XMS_experimental and chain B
create 7XMS_RFAA_no_templates_ligand, 7XMS_RFAA_no_templates and chain B
show cartoon, 7XMS_exp_ligand
show cartoon, 7XMS_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7XMS_exp_ligand
set cartoon_oval_width, 0.7, 7XMS_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7XMS_exp_ligand
set cartoon_loop_radius, 0.7, 7XMS_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8L_AB.pdb, 8X8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8X8L_no_templates.pdb, 8X8L_RFAA_no_templates
align 8X8L_experimental, 7F6I_experimental 
align 8X8L_RFAA_no_templates, 8X8L_experimental
color grey70, chain A and 8X8L_RFAA_no_templates
color white, chain A and 8X8L_experimental
color RF-AA (no templates), 8X8L_RFAA_no_templates and chain B
color experimental_color, 8X8L_experimental and chain B
create 8X8L_exp_ligand, 8X8L_experimental and chain B
create 8X8L_RFAA_no_templates_ligand, 8X8L_RFAA_no_templates and chain B
show cartoon, 8X8L_exp_ligand
show cartoon, 8X8L_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8X8L_exp_ligand
set cartoon_oval_width, 0.7, 8X8L_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8X8L_exp_ligand
set cartoon_loop_radius, 0.7, 8X8L_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8N_AB.pdb, 8X8N_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_no_templates/8X8N_no_templates.pdb, 8X8N_RFAA_no_templates
align 8X8N_experimental, 7F6I_experimental 
align 8X8N_RFAA_no_templates, 8X8N_experimental
color grey70, chain A and 8X8N_RFAA_no_templates
color white, chain A and 8X8N_experimental
color RF-AA (no templates), 8X8N_RFAA_no_templates and chain B
color experimental_color, 8X8N_experimental and chain B
create 8X8N_exp_ligand, 8X8N_experimental and chain B
create 8X8N_RFAA_no_templates_ligand, 8X8N_RFAA_no_templates and chain B
show cartoon, 8X8N_exp_ligand
show cartoon, 8X8N_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8X8N_exp_ligand
set cartoon_oval_width, 0.7, 8X8N_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8X8N_exp_ligand
set cartoon_loop_radius, 0.7, 8X8N_RFAA_no_templates_ligand



set grid_mode, 1
set grid_slot, 1, 7F6I_experimental
set grid_slot, 1, 7F6I_exp_ligand
set grid_slot, 1, 7F6I_RFAA_no_templates
set grid_slot, 1, 7F6I_RFAA_no_templates_ligand
set grid_slot, 2, 8IA8_experimental
set grid_slot, 2, 8IA8_exp_ligand
set grid_slot, 2, 8IA8_RFAA_no_templates
set grid_slot, 2, 8IA8_RFAA_no_templates_ligand
set grid_slot, 3, 8I95_experimental
set grid_slot, 3, 8I95_exp_ligand
set grid_slot, 3, 8I95_RFAA_no_templates
set grid_slot, 3, 8I95_RFAA_no_templates_ligand
set grid_slot, 4, 8HK2_experimental
set grid_slot, 4, 8HK2_exp_ligand
set grid_slot, 4, 8HK2_RFAA_no_templates
set grid_slot, 4, 8HK2_RFAA_no_templates_ligand
set grid_slot, 5, 8XGM_experimental
set grid_slot, 5, 8XGM_exp_ligand
set grid_slot, 5, 8XGM_RFAA_no_templates
set grid_slot, 5, 8XGM_RFAA_no_templates_ligand
set grid_slot, 6, 7W3Z_experimental
set grid_slot, 6, 7W3Z_exp_ligand
set grid_slot, 6, 7W3Z_RFAA_no_templates
set grid_slot, 6, 7W3Z_RFAA_no_templates_ligand
set grid_slot, 7, 8WVY_experimental
set grid_slot, 7, 8WVY_exp_ligand
set grid_slot, 7, 8WVY_RFAA_no_templates
set grid_slot, 7, 8WVY_RFAA_no_templates_ligand
set grid_slot, 8, 8JGF_experimental
set grid_slot, 8, 8JGF_exp_ligand
set grid_slot, 8, 8JGF_RFAA_no_templates
set grid_slot, 8, 8JGF_RFAA_no_templates_ligand
set grid_slot, 9, 7S8L_experimental
set grid_slot, 9, 7S8L_exp_ligand
set grid_slot, 9, 7S8L_RFAA_no_templates
set grid_slot, 9, 7S8L_RFAA_no_templates_ligand
set grid_slot, 10, 7VDM_experimental
set grid_slot, 10, 7VDM_exp_ligand
set grid_slot, 10, 7VDM_RFAA_no_templates
set grid_slot, 10, 7VDM_RFAA_no_templates_ligand
set grid_slot, 11, 7VV0_experimental
set grid_slot, 11, 7VV0_exp_ligand
set grid_slot, 11, 7VV0_RFAA_no_templates
set grid_slot, 11, 7VV0_RFAA_no_templates_ligand
set grid_slot, 12, 8IBV_experimental
set grid_slot, 12, 8IBV_exp_ligand
set grid_slot, 12, 8IBV_RFAA_no_templates
set grid_slot, 12, 8IBV_RFAA_no_templates_ligand
set grid_slot, 13, 7XWO_experimental
set grid_slot, 13, 7XWO_exp_ligand
set grid_slot, 13, 7XWO_RFAA_no_templates
set grid_slot, 13, 7XWO_RFAA_no_templates_ligand
set grid_slot, 14, 8H0P_experimental
set grid_slot, 14, 8H0P_exp_ligand
set grid_slot, 14, 8H0P_RFAA_no_templates
set grid_slot, 14, 8H0P_RFAA_no_templates_ligand
set grid_slot, 15, 7W56_experimental
set grid_slot, 15, 7W56_exp_ligand
set grid_slot, 15, 7W56_RFAA_no_templates
set grid_slot, 15, 7W56_RFAA_no_templates_ligand
set grid_slot, 16, 7W53_experimental
set grid_slot, 16, 7W53_exp_ligand
set grid_slot, 16, 7W53_RFAA_no_templates
set grid_slot, 16, 7W53_RFAA_no_templates_ligand
set grid_slot, 17, 7W55_experimental
set grid_slot, 17, 7W55_exp_ligand
set grid_slot, 17, 7W55_RFAA_no_templates
set grid_slot, 17, 7W55_RFAA_no_templates_ligand
set grid_slot, 18, 7W57_experimental
set grid_slot, 18, 7W57_exp_ligand
set grid_slot, 18, 7W57_RFAA_no_templates
set grid_slot, 18, 7W57_RFAA_no_templates_ligand
set grid_slot, 19, 8F7W_experimental
set grid_slot, 19, 8F7W_exp_ligand
set grid_slot, 19, 8F7W_RFAA_no_templates
set grid_slot, 19, 8F7W_RFAA_no_templates_ligand
set grid_slot, 20, 8F7Q_experimental
set grid_slot, 20, 8F7Q_exp_ligand
set grid_slot, 20, 8F7Q_RFAA_no_templates
set grid_slot, 20, 8F7Q_RFAA_no_templates_ligand
set grid_slot, 21, 8F7X_experimental
set grid_slot, 21, 8F7X_exp_ligand
set grid_slot, 21, 8F7X_RFAA_no_templates
set grid_slot, 21, 8F7X_RFAA_no_templates_ligand
set grid_slot, 22, 8ZPT_experimental
set grid_slot, 22, 8ZPT_exp_ligand
set grid_slot, 22, 8ZPT_RFAA_no_templates
set grid_slot, 22, 8ZPT_RFAA_no_templates_ligand
set grid_slot, 23, 8WZ2_experimental
set grid_slot, 23, 8WZ2_exp_ligand
set grid_slot, 23, 8WZ2_RFAA_no_templates
set grid_slot, 23, 8WZ2_RFAA_no_templates_ligand
set grid_slot, 24, 7T10_experimental
set grid_slot, 24, 7T10_exp_ligand
set grid_slot, 24, 7T10_RFAA_no_templates
set grid_slot, 24, 7T10_RFAA_no_templates_ligand
set grid_slot, 25, 7T11_experimental
set grid_slot, 25, 7T11_exp_ligand
set grid_slot, 25, 7T11_RFAA_no_templates
set grid_slot, 25, 7T11_RFAA_no_templates_ligand
set grid_slot, 26, 7XMS_experimental
set grid_slot, 26, 7XMS_exp_ligand
set grid_slot, 26, 7XMS_RFAA_no_templates
set grid_slot, 26, 7XMS_RFAA_no_templates_ligand
set grid_slot, 27, 8X8L_experimental
set grid_slot, 27, 8X8L_exp_ligand
set grid_slot, 27, 8X8L_RFAA_no_templates
set grid_slot, 27, 8X8L_RFAA_no_templates_ligand
set grid_slot, 28, 8X8N_experimental
set grid_slot, 28, 8X8N_exp_ligand
set grid_slot, 28, 8X8N_RFAA_no_templates
set grid_slot, 28, 8X8N_RFAA_no_templates_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
