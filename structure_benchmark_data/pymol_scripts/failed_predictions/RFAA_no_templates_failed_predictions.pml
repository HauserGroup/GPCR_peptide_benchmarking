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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7F6I.pdb, 7F6I_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8IA8.pdb, 8IA8_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8HK2.pdb, 8HK2_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7Y66_AB.pdb, 7Y66_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7Y66.pdb, 7Y66_RFAA_no_templates
align 7Y66_experimental, 7F6I_experimental 
align 7Y66_RFAA_no_templates, 7Y66_experimental
color grey70, chain A and 7Y66_RFAA_no_templates
color white, chain A and 7Y66_experimental
color RF-AA (no templates), 7Y66_RFAA_no_templates and chain B
color experimental_color, 7Y66_experimental and chain B
create 7Y66_exp_ligand, 7Y66_experimental and chain B
create 7Y66_RFAA_no_templates_ligand, 7Y66_RFAA_no_templates and chain B
show cartoon, 7Y66_exp_ligand
show cartoon, 7Y66_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7Y66_exp_ligand
set cartoon_oval_width, 0.7, 7Y66_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7Y66_exp_ligand
set cartoon_loop_radius, 0.7, 7Y66_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7Y64_AB.pdb, 7Y64_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7Y64.pdb, 7Y64_RFAA_no_templates
align 7Y64_experimental, 7F6I_experimental 
align 7Y64_RFAA_no_templates, 7Y64_experimental
color grey70, chain A and 7Y64_RFAA_no_templates
color white, chain A and 7Y64_experimental
color RF-AA (no templates), 7Y64_RFAA_no_templates and chain B
color experimental_color, 7Y64_experimental and chain B
create 7Y64_exp_ligand, 7Y64_experimental and chain B
create 7Y64_RFAA_no_templates_ligand, 7Y64_RFAA_no_templates and chain B
show cartoon, 7Y64_exp_ligand
show cartoon, 7Y64_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7Y64_exp_ligand
set cartoon_oval_width, 0.7, 7Y64_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7Y64_exp_ligand
set cartoon_loop_radius, 0.7, 7Y64_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HCQ_AB.pdb, 8HCQ_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8HCQ.pdb, 8HCQ_RFAA_no_templates
align 8HCQ_experimental, 7F6I_experimental 
align 8HCQ_RFAA_no_templates, 8HCQ_experimental
color grey70, chain A and 8HCQ_RFAA_no_templates
color white, chain A and 8HCQ_experimental
color RF-AA (no templates), 8HCQ_RFAA_no_templates and chain B
color experimental_color, 8HCQ_experimental and chain B
create 8HCQ_exp_ligand, 8HCQ_experimental and chain B
create 8HCQ_RFAA_no_templates_ligand, 8HCQ_RFAA_no_templates and chain B
show cartoon, 8HCQ_exp_ligand
show cartoon, 8HCQ_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8HCQ_exp_ligand
set cartoon_oval_width, 0.7, 8HCQ_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8HCQ_exp_ligand
set cartoon_loop_radius, 0.7, 8HCQ_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T6T_AB.pdb, 7T6T_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7T6T.pdb, 7T6T_RFAA_no_templates
align 7T6T_experimental, 7F6I_experimental 
align 7T6T_RFAA_no_templates, 7T6T_experimental
color grey70, chain A and 7T6T_RFAA_no_templates
color white, chain A and 7T6T_experimental
color RF-AA (no templates), 7T6T_RFAA_no_templates and chain B
color experimental_color, 7T6T_experimental and chain B
create 7T6T_exp_ligand, 7T6T_experimental and chain B
create 7T6T_RFAA_no_templates_ligand, 7T6T_RFAA_no_templates and chain B
show cartoon, 7T6T_exp_ligand
show cartoon, 7T6T_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7T6T_exp_ligand
set cartoon_oval_width, 0.7, 7T6T_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7T6T_exp_ligand
set cartoon_loop_radius, 0.7, 7T6T_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ3_AB.pdb, 7WQ3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7WQ3.pdb, 7WQ3_RFAA_no_templates
align 7WQ3_experimental, 7F6I_experimental 
align 7WQ3_RFAA_no_templates, 7WQ3_experimental
color grey70, chain A and 7WQ3_RFAA_no_templates
color white, chain A and 7WQ3_experimental
color RF-AA (no templates), 7WQ3_RFAA_no_templates and chain B
color experimental_color, 7WQ3_experimental and chain B
create 7WQ3_exp_ligand, 7WQ3_experimental and chain B
create 7WQ3_RFAA_no_templates_ligand, 7WQ3_RFAA_no_templates and chain B
show cartoon, 7WQ3_exp_ligand
show cartoon, 7WQ3_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7WQ3_exp_ligand
set cartoon_oval_width, 0.7, 7WQ3_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7WQ3_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ3_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7WQ4.pdb, 7WQ4_RFAA_no_templates
align 7WQ4_experimental, 7F6I_experimental 
align 7WQ4_RFAA_no_templates, 7WQ4_experimental
color grey70, chain A and 7WQ4_RFAA_no_templates
color white, chain A and 7WQ4_experimental
color RF-AA (no templates), 7WQ4_RFAA_no_templates and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_RFAA_no_templates_ligand, 7WQ4_RFAA_no_templates and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W40_AB.pdb, 7W40_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7W40.pdb, 7W40_RFAA_no_templates
align 7W40_experimental, 7F6I_experimental 
align 7W40_RFAA_no_templates, 7W40_experimental
color grey70, chain A and 7W40_RFAA_no_templates
color white, chain A and 7W40_experimental
color RF-AA (no templates), 7W40_RFAA_no_templates and chain B
color experimental_color, 7W40_experimental and chain B
create 7W40_exp_ligand, 7W40_experimental and chain B
create 7W40_RFAA_no_templates_ligand, 7W40_RFAA_no_templates and chain B
show cartoon, 7W40_exp_ligand
show cartoon, 7W40_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 7W40_exp_ligand
set cartoon_oval_width, 0.7, 7W40_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 7W40_exp_ligand
set cartoon_loop_radius, 0.7, 7W40_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7W3Z.pdb, 7W3Z_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8DWG_AB.pdb, 8DWG_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8DWG.pdb, 8DWG_RFAA_no_templates
align 8DWG_experimental, 7F6I_experimental 
align 8DWG_RFAA_no_templates, 8DWG_experimental
color grey70, chain A and 8DWG_RFAA_no_templates
color white, chain A and 8DWG_experimental
color RF-AA (no templates), 8DWG_RFAA_no_templates and chain B
color experimental_color, 8DWG_experimental and chain B
create 8DWG_exp_ligand, 8DWG_experimental and chain B
create 8DWG_RFAA_no_templates_ligand, 8DWG_RFAA_no_templates and chain B
show cartoon, 8DWG_exp_ligand
show cartoon, 8DWG_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8DWG_exp_ligand
set cartoon_oval_width, 0.7, 8DWG_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8DWG_exp_ligand
set cartoon_loop_radius, 0.7, 8DWG_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7S8L.pdb, 7S8L_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7VDM.pdb, 7VDM_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7VV0.pdb, 7VV0_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8IBV.pdb, 8IBV_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7W56.pdb, 7W56_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7W55.pdb, 7W55_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7W57.pdb, 7W57_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8F7W.pdb, 8F7W_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8F7Q.pdb, 8F7Q_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8EFQ_AB.pdb, 8EFQ_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8EFQ.pdb, 8EFQ_RFAA_no_templates
align 8EFQ_experimental, 7F6I_experimental 
align 8EFQ_RFAA_no_templates, 8EFQ_experimental
color grey70, chain A and 8EFQ_RFAA_no_templates
color white, chain A and 8EFQ_experimental
color RF-AA (no templates), 8EFQ_RFAA_no_templates and chain B
color experimental_color, 8EFQ_experimental and chain B
create 8EFQ_exp_ligand, 8EFQ_experimental and chain B
create 8EFQ_RFAA_no_templates_ligand, 8EFQ_RFAA_no_templates and chain B
show cartoon, 8EFQ_exp_ligand
show cartoon, 8EFQ_RFAA_no_templates_ligand
set cartoon_oval_width, 0.7, 8EFQ_exp_ligand
set cartoon_oval_width, 0.7, 8EFQ_RFAA_no_templates_ligand
set cartoon_loop_radius, 0.7, 8EFQ_exp_ligand
set cartoon_loop_radius, 0.7, 8EFQ_RFAA_no_templates_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/8F7X.pdb, 8F7X_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7T10.pdb, 7T10_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7T11.pdb, 7T11_RFAA_no_templates
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain_no_templates/7XMS.pdb, 7XMS_RFAA_no_templates
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



set grid_mode, 1
set grid_slot, 1, 7F6I_experimental
set grid_slot, 1, 7F6I_exp_ligand
set grid_slot, 1, 7F6I_RFAA_no_templates
set grid_slot, 1, 7F6I_RFAA_no_templates_ligand
set grid_slot, 2, 8IA8_experimental
set grid_slot, 2, 8IA8_exp_ligand
set grid_slot, 2, 8IA8_RFAA_no_templates
set grid_slot, 2, 8IA8_RFAA_no_templates_ligand
set grid_slot, 3, 8HK2_experimental
set grid_slot, 3, 8HK2_exp_ligand
set grid_slot, 3, 8HK2_RFAA_no_templates
set grid_slot, 3, 8HK2_RFAA_no_templates_ligand
set grid_slot, 4, 7Y66_experimental
set grid_slot, 4, 7Y66_exp_ligand
set grid_slot, 4, 7Y66_RFAA_no_templates
set grid_slot, 4, 7Y66_RFAA_no_templates_ligand
set grid_slot, 5, 7Y64_experimental
set grid_slot, 5, 7Y64_exp_ligand
set grid_slot, 5, 7Y64_RFAA_no_templates
set grid_slot, 5, 7Y64_RFAA_no_templates_ligand
set grid_slot, 6, 8HCQ_experimental
set grid_slot, 6, 8HCQ_exp_ligand
set grid_slot, 6, 8HCQ_RFAA_no_templates
set grid_slot, 6, 8HCQ_RFAA_no_templates_ligand
set grid_slot, 7, 7T6T_experimental
set grid_slot, 7, 7T6T_exp_ligand
set grid_slot, 7, 7T6T_RFAA_no_templates
set grid_slot, 7, 7T6T_RFAA_no_templates_ligand
set grid_slot, 8, 7WQ3_experimental
set grid_slot, 8, 7WQ3_exp_ligand
set grid_slot, 8, 7WQ3_RFAA_no_templates
set grid_slot, 8, 7WQ3_RFAA_no_templates_ligand
set grid_slot, 9, 7WQ4_experimental
set grid_slot, 9, 7WQ4_exp_ligand
set grid_slot, 9, 7WQ4_RFAA_no_templates
set grid_slot, 9, 7WQ4_RFAA_no_templates_ligand
set grid_slot, 10, 7W40_experimental
set grid_slot, 10, 7W40_exp_ligand
set grid_slot, 10, 7W40_RFAA_no_templates
set grid_slot, 10, 7W40_RFAA_no_templates_ligand
set grid_slot, 11, 7W3Z_experimental
set grid_slot, 11, 7W3Z_exp_ligand
set grid_slot, 11, 7W3Z_RFAA_no_templates
set grid_slot, 11, 7W3Z_RFAA_no_templates_ligand
set grid_slot, 12, 8DWG_experimental
set grid_slot, 12, 8DWG_exp_ligand
set grid_slot, 12, 8DWG_RFAA_no_templates
set grid_slot, 12, 8DWG_RFAA_no_templates_ligand
set grid_slot, 13, 7S8L_experimental
set grid_slot, 13, 7S8L_exp_ligand
set grid_slot, 13, 7S8L_RFAA_no_templates
set grid_slot, 13, 7S8L_RFAA_no_templates_ligand
set grid_slot, 14, 7VDM_experimental
set grid_slot, 14, 7VDM_exp_ligand
set grid_slot, 14, 7VDM_RFAA_no_templates
set grid_slot, 14, 7VDM_RFAA_no_templates_ligand
set grid_slot, 15, 7VV0_experimental
set grid_slot, 15, 7VV0_exp_ligand
set grid_slot, 15, 7VV0_RFAA_no_templates
set grid_slot, 15, 7VV0_RFAA_no_templates_ligand
set grid_slot, 16, 8IBV_experimental
set grid_slot, 16, 8IBV_exp_ligand
set grid_slot, 16, 8IBV_RFAA_no_templates
set grid_slot, 16, 8IBV_RFAA_no_templates_ligand
set grid_slot, 17, 7W56_experimental
set grid_slot, 17, 7W56_exp_ligand
set grid_slot, 17, 7W56_RFAA_no_templates
set grid_slot, 17, 7W56_RFAA_no_templates_ligand
set grid_slot, 18, 7W55_experimental
set grid_slot, 18, 7W55_exp_ligand
set grid_slot, 18, 7W55_RFAA_no_templates
set grid_slot, 18, 7W55_RFAA_no_templates_ligand
set grid_slot, 19, 7W57_experimental
set grid_slot, 19, 7W57_exp_ligand
set grid_slot, 19, 7W57_RFAA_no_templates
set grid_slot, 19, 7W57_RFAA_no_templates_ligand
set grid_slot, 20, 8F7W_experimental
set grid_slot, 20, 8F7W_exp_ligand
set grid_slot, 20, 8F7W_RFAA_no_templates
set grid_slot, 20, 8F7W_RFAA_no_templates_ligand
set grid_slot, 21, 8F7Q_experimental
set grid_slot, 21, 8F7Q_exp_ligand
set grid_slot, 21, 8F7Q_RFAA_no_templates
set grid_slot, 21, 8F7Q_RFAA_no_templates_ligand
set grid_slot, 22, 8EFQ_experimental
set grid_slot, 22, 8EFQ_exp_ligand
set grid_slot, 22, 8EFQ_RFAA_no_templates
set grid_slot, 22, 8EFQ_RFAA_no_templates_ligand
set grid_slot, 23, 8F7X_experimental
set grid_slot, 23, 8F7X_exp_ligand
set grid_slot, 23, 8F7X_RFAA_no_templates
set grid_slot, 23, 8F7X_RFAA_no_templates_ligand
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
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
