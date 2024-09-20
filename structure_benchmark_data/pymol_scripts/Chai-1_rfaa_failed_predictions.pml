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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7SK4.pdb, 7SK4_Chai-1
align 7SK4_Chai-1, 7SK4_experimental
color white, chain A
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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7F6I.pdb, 7F6I_Chai-1
align 7F6I_experimental, 7SK4_experimental 
align 7F6I_Chai-1, 7F6I_experimental
color white, chain A
color Chai-1, 7F6I_Chai-1 and chain B
color experimental_color, 7F6I_experimental and chain B
create 7F6I_exp_ligand, 7F6I_experimental and chain B
create 7F6I_Chai-1_ligand, 7F6I_Chai-1 and chain B
show cartoon, 7F6I_exp_ligand
show cartoon, 7F6I_Chai-1_ligand
set cartoon_oval_width, 0.7, 7F6I_exp_ligand
set cartoon_oval_width, 0.7, 7F6I_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7F6I_exp_ligand
set cartoon_loop_radius, 0.7, 7F6I_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8IA8.pdb, 8IA8_Chai-1
align 8IA8_experimental, 7SK4_experimental 
align 8IA8_Chai-1, 8IA8_experimental
color white, chain A
color Chai-1, 8IA8_Chai-1 and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_Chai-1_ligand, 8IA8_Chai-1 and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_Chai-1_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8HK2.pdb, 8HK2_Chai-1
align 8HK2_experimental, 7SK4_experimental 
align 8HK2_Chai-1, 8HK2_experimental
color white, chain A
color Chai-1, 8HK2_Chai-1 and chain B
color experimental_color, 8HK2_experimental and chain B
create 8HK2_exp_ligand, 8HK2_experimental and chain B
create 8HK2_Chai-1_ligand, 8HK2_Chai-1 and chain B
show cartoon, 8HK2_exp_ligand
show cartoon, 8HK2_Chai-1_ligand
set cartoon_oval_width, 0.7, 8HK2_exp_ligand
set cartoon_oval_width, 0.7, 8HK2_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8HK2_exp_ligand
set cartoon_loop_radius, 0.7, 8HK2_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7Y64_AB.pdb, 7Y64_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7Y64.pdb, 7Y64_Chai-1
align 7Y64_experimental, 7SK4_experimental 
align 7Y64_Chai-1, 7Y64_experimental
color white, chain A
color Chai-1, 7Y64_Chai-1 and chain B
color experimental_color, 7Y64_experimental and chain B
create 7Y64_exp_ligand, 7Y64_experimental and chain B
create 7Y64_Chai-1_ligand, 7Y64_Chai-1 and chain B
show cartoon, 7Y64_exp_ligand
show cartoon, 7Y64_Chai-1_ligand
set cartoon_oval_width, 0.7, 7Y64_exp_ligand
set cartoon_oval_width, 0.7, 7Y64_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7Y64_exp_ligand
set cartoon_loop_radius, 0.7, 7Y64_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W40_AB.pdb, 7W40_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W40.pdb, 7W40_Chai-1
align 7W40_experimental, 7SK4_experimental 
align 7W40_Chai-1, 7W40_experimental
color white, chain A
color Chai-1, 7W40_Chai-1 and chain B
color experimental_color, 7W40_experimental and chain B
create 7W40_exp_ligand, 7W40_experimental and chain B
create 7W40_Chai-1_ligand, 7W40_Chai-1 and chain B
show cartoon, 7W40_exp_ligand
show cartoon, 7W40_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W40_exp_ligand
set cartoon_oval_width, 0.7, 7W40_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W40_exp_ligand
set cartoon_loop_radius, 0.7, 7W40_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W3Z.pdb, 7W3Z_Chai-1
align 7W3Z_experimental, 7SK4_experimental 
align 7W3Z_Chai-1, 7W3Z_experimental
color white, chain A
color Chai-1, 7W3Z_Chai-1 and chain B
color experimental_color, 7W3Z_experimental and chain B
create 7W3Z_exp_ligand, 7W3Z_experimental and chain B
create 7W3Z_Chai-1_ligand, 7W3Z_Chai-1 and chain B
show cartoon, 7W3Z_exp_ligand
show cartoon, 7W3Z_Chai-1_ligand
set cartoon_oval_width, 0.7, 7W3Z_exp_ligand
set cartoon_oval_width, 0.7, 7W3Z_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7W3Z_exp_ligand
set cartoon_loop_radius, 0.7, 7W3Z_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8DWG_AB.pdb, 8DWG_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8DWG.pdb, 8DWG_Chai-1
align 8DWG_experimental, 7SK4_experimental 
align 8DWG_Chai-1, 8DWG_experimental
color white, chain A
color Chai-1, 8DWG_Chai-1 and chain B
color experimental_color, 8DWG_experimental and chain B
create 8DWG_exp_ligand, 8DWG_experimental and chain B
create 8DWG_Chai-1_ligand, 8DWG_Chai-1 and chain B
show cartoon, 8DWG_exp_ligand
show cartoon, 8DWG_Chai-1_ligand
set cartoon_oval_width, 0.7, 8DWG_exp_ligand
set cartoon_oval_width, 0.7, 8DWG_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8DWG_exp_ligand
set cartoon_loop_radius, 0.7, 8DWG_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7S8L.pdb, 7S8L_Chai-1
align 7S8L_experimental, 7SK4_experimental 
align 7S8L_Chai-1, 7S8L_experimental
color white, chain A
color Chai-1, 7S8L_Chai-1 and chain B
color experimental_color, 7S8L_experimental and chain B
create 7S8L_exp_ligand, 7S8L_experimental and chain B
create 7S8L_Chai-1_ligand, 7S8L_Chai-1 and chain B
show cartoon, 7S8L_exp_ligand
show cartoon, 7S8L_Chai-1_ligand
set cartoon_oval_width, 0.7, 7S8L_exp_ligand
set cartoon_oval_width, 0.7, 7S8L_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7S8L_exp_ligand
set cartoon_loop_radius, 0.7, 7S8L_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VDM_AB.pdb, 7VDM_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7VDM.pdb, 7VDM_Chai-1
align 7VDM_experimental, 7SK4_experimental 
align 7VDM_Chai-1, 7VDM_experimental
color white, chain A
color Chai-1, 7VDM_Chai-1 and chain B
color experimental_color, 7VDM_experimental and chain B
create 7VDM_exp_ligand, 7VDM_experimental and chain B
create 7VDM_Chai-1_ligand, 7VDM_Chai-1 and chain B
show cartoon, 7VDM_exp_ligand
show cartoon, 7VDM_Chai-1_ligand
set cartoon_oval_width, 0.7, 7VDM_exp_ligand
set cartoon_oval_width, 0.7, 7VDM_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7VDM_exp_ligand
set cartoon_loop_radius, 0.7, 7VDM_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VV0_AB.pdb, 7VV0_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7VV0.pdb, 7VV0_Chai-1
align 7VV0_experimental, 7SK4_experimental 
align 7VV0_Chai-1, 7VV0_experimental
color white, chain A
color Chai-1, 7VV0_Chai-1 and chain B
color experimental_color, 7VV0_experimental and chain B
create 7VV0_exp_ligand, 7VV0_experimental and chain B
create 7VV0_Chai-1_ligand, 7VV0_Chai-1 and chain B
show cartoon, 7VV0_exp_ligand
show cartoon, 7VV0_Chai-1_ligand
set cartoon_oval_width, 0.7, 7VV0_exp_ligand
set cartoon_oval_width, 0.7, 7VV0_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7VV0_exp_ligand
set cartoon_loop_radius, 0.7, 7VV0_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7P00_AB.pdb, 7P00_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7P00.pdb, 7P00_Chai-1
align 7P00_experimental, 7SK4_experimental 
align 7P00_Chai-1, 7P00_experimental
color white, chain A
color Chai-1, 7P00_Chai-1 and chain B
color experimental_color, 7P00_experimental and chain B
create 7P00_exp_ligand, 7P00_experimental and chain B
create 7P00_Chai-1_ligand, 7P00_Chai-1 and chain B
show cartoon, 7P00_exp_ligand
show cartoon, 7P00_Chai-1_ligand
set cartoon_oval_width, 0.7, 7P00_exp_ligand
set cartoon_oval_width, 0.7, 7P00_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7P00_exp_ligand
set cartoon_loop_radius, 0.7, 7P00_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W56.pdb, 7W56_Chai-1
align 7W56_experimental, 7SK4_experimental 
align 7W56_Chai-1, 7W56_experimental
color white, chain A
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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W53.pdb, 7W53_Chai-1
align 7W53_experimental, 7SK4_experimental 
align 7W53_Chai-1, 7W53_experimental
color white, chain A
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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W55.pdb, 7W55_Chai-1
align 7W55_experimental, 7SK4_experimental 
align 7W55_Chai-1, 7W55_experimental
color white, chain A
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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7W57.pdb, 7W57_Chai-1
align 7W57_experimental, 7SK4_experimental 
align 7W57_Chai-1, 7W57_experimental
color white, chain A
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
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VGX_AB.pdb, 7VGX_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7VGX.pdb, 7VGX_Chai-1
align 7VGX_experimental, 7SK4_experimental 
align 7VGX_Chai-1, 7VGX_experimental
color white, chain A
color Chai-1, 7VGX_Chai-1 and chain B
color experimental_color, 7VGX_experimental and chain B
create 7VGX_exp_ligand, 7VGX_experimental and chain B
create 7VGX_Chai-1_ligand, 7VGX_Chai-1 and chain B
show cartoon, 7VGX_exp_ligand
show cartoon, 7VGX_Chai-1_ligand
set cartoon_oval_width, 0.7, 7VGX_exp_ligand
set cartoon_oval_width, 0.7, 7VGX_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7VGX_exp_ligand
set cartoon_loop_radius, 0.7, 7VGX_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8F7W.pdb, 8F7W_Chai-1
align 8F7W_experimental, 7SK4_experimental 
align 8F7W_Chai-1, 8F7W_experimental
color white, chain A
color Chai-1, 8F7W_Chai-1 and chain B
color experimental_color, 8F7W_experimental and chain B
create 8F7W_exp_ligand, 8F7W_experimental and chain B
create 8F7W_Chai-1_ligand, 8F7W_Chai-1 and chain B
show cartoon, 8F7W_exp_ligand
show cartoon, 8F7W_Chai-1_ligand
set cartoon_oval_width, 0.7, 8F7W_exp_ligand
set cartoon_oval_width, 0.7, 8F7W_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8F7W_exp_ligand
set cartoon_loop_radius, 0.7, 8F7W_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7Q_AB.pdb, 8F7Q_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8F7Q.pdb, 8F7Q_Chai-1
align 8F7Q_experimental, 7SK4_experimental 
align 8F7Q_Chai-1, 8F7Q_experimental
color white, chain A
color Chai-1, 8F7Q_Chai-1 and chain B
color experimental_color, 8F7Q_experimental and chain B
create 8F7Q_exp_ligand, 8F7Q_experimental and chain B
create 8F7Q_Chai-1_ligand, 8F7Q_Chai-1 and chain B
show cartoon, 8F7Q_exp_ligand
show cartoon, 8F7Q_Chai-1_ligand
set cartoon_oval_width, 0.7, 8F7Q_exp_ligand
set cartoon_oval_width, 0.7, 8F7Q_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8F7Q_exp_ligand
set cartoon_loop_radius, 0.7, 8F7Q_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/8F7X.pdb, 8F7X_Chai-1
align 8F7X_experimental, 7SK4_experimental 
align 8F7X_Chai-1, 8F7X_experimental
color white, chain A
color Chai-1, 8F7X_Chai-1 and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_Chai-1_ligand, 8F7X_Chai-1 and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_Chai-1_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_Chai-1_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7T10.pdb, 7T10_Chai-1
align 7T10_experimental, 7SK4_experimental 
align 7T10_Chai-1, 7T10_experimental
color white, chain A
color Chai-1, 7T10_Chai-1 and chain B
color experimental_color, 7T10_experimental and chain B
create 7T10_exp_ligand, 7T10_experimental and chain B
create 7T10_Chai-1_ligand, 7T10_Chai-1 and chain B
show cartoon, 7T10_exp_ligand
show cartoon, 7T10_Chai-1_ligand
set cartoon_oval_width, 0.7, 7T10_exp_ligand
set cartoon_oval_width, 0.7, 7T10_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7T10_exp_ligand
set cartoon_loop_radius, 0.7, 7T10_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T11_AB.pdb, 7T11_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7T11.pdb, 7T11_Chai-1
align 7T11_experimental, 7SK4_experimental 
align 7T11_Chai-1, 7T11_experimental
color white, chain A
color Chai-1, 7T11_Chai-1 and chain B
color experimental_color, 7T11_experimental and chain B
create 7T11_exp_ligand, 7T11_experimental and chain B
create 7T11_Chai-1_ligand, 7T11_Chai-1 and chain B
show cartoon, 7T11_exp_ligand
show cartoon, 7T11_Chai-1_ligand
set cartoon_oval_width, 0.7, 7T11_exp_ligand
set cartoon_oval_width, 0.7, 7T11_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7T11_exp_ligand
set cartoon_loop_radius, 0.7, 7T11_Chai-1_ligand
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XMS_AB.pdb, 7XMS_experimental
load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/Chai-1/renamed_chains/7XMS.pdb, 7XMS_Chai-1
align 7XMS_experimental, 7SK4_experimental 
align 7XMS_Chai-1, 7XMS_experimental
color white, chain A
color Chai-1, 7XMS_Chai-1 and chain B
color experimental_color, 7XMS_experimental and chain B
create 7XMS_exp_ligand, 7XMS_experimental and chain B
create 7XMS_Chai-1_ligand, 7XMS_Chai-1 and chain B
show cartoon, 7XMS_exp_ligand
show cartoon, 7XMS_Chai-1_ligand
set cartoon_oval_width, 0.7, 7XMS_exp_ligand
set cartoon_oval_width, 0.7, 7XMS_Chai-1_ligand
set cartoon_loop_radius, 0.7, 7XMS_exp_ligand
set cartoon_loop_radius, 0.7, 7XMS_Chai-1_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_Chai-1
set grid_slot, 1, 7SK4_Chai-1_ligand
set grid_slot, 2, 7F6I_experimental
set grid_slot, 2, 7F6I_exp_ligand
set grid_slot, 2, 7F6I_Chai-1
set grid_slot, 2, 7F6I_Chai-1_ligand
set grid_slot, 3, 8IA8_experimental
set grid_slot, 3, 8IA8_exp_ligand
set grid_slot, 3, 8IA8_Chai-1
set grid_slot, 3, 8IA8_Chai-1_ligand
set grid_slot, 4, 8HK2_experimental
set grid_slot, 4, 8HK2_exp_ligand
set grid_slot, 4, 8HK2_Chai-1
set grid_slot, 4, 8HK2_Chai-1_ligand
set grid_slot, 5, 7Y64_experimental
set grid_slot, 5, 7Y64_exp_ligand
set grid_slot, 5, 7Y64_Chai-1
set grid_slot, 5, 7Y64_Chai-1_ligand
set grid_slot, 6, 7W40_experimental
set grid_slot, 6, 7W40_exp_ligand
set grid_slot, 6, 7W40_Chai-1
set grid_slot, 6, 7W40_Chai-1_ligand
set grid_slot, 7, 7W3Z_experimental
set grid_slot, 7, 7W3Z_exp_ligand
set grid_slot, 7, 7W3Z_Chai-1
set grid_slot, 7, 7W3Z_Chai-1_ligand
set grid_slot, 8, 8DWG_experimental
set grid_slot, 8, 8DWG_exp_ligand
set grid_slot, 8, 8DWG_Chai-1
set grid_slot, 8, 8DWG_Chai-1_ligand
set grid_slot, 9, 7S8L_experimental
set grid_slot, 9, 7S8L_exp_ligand
set grid_slot, 9, 7S8L_Chai-1
set grid_slot, 9, 7S8L_Chai-1_ligand
set grid_slot, 10, 7VDM_experimental
set grid_slot, 10, 7VDM_exp_ligand
set grid_slot, 10, 7VDM_Chai-1
set grid_slot, 10, 7VDM_Chai-1_ligand
set grid_slot, 11, 7VV0_experimental
set grid_slot, 11, 7VV0_exp_ligand
set grid_slot, 11, 7VV0_Chai-1
set grid_slot, 11, 7VV0_Chai-1_ligand
set grid_slot, 12, 7P00_experimental
set grid_slot, 12, 7P00_exp_ligand
set grid_slot, 12, 7P00_Chai-1
set grid_slot, 12, 7P00_Chai-1_ligand
set grid_slot, 13, 7W56_experimental
set grid_slot, 13, 7W56_exp_ligand
set grid_slot, 13, 7W56_Chai-1
set grid_slot, 13, 7W56_Chai-1_ligand
set grid_slot, 14, 7W53_experimental
set grid_slot, 14, 7W53_exp_ligand
set grid_slot, 14, 7W53_Chai-1
set grid_slot, 14, 7W53_Chai-1_ligand
set grid_slot, 15, 7W55_experimental
set grid_slot, 15, 7W55_exp_ligand
set grid_slot, 15, 7W55_Chai-1
set grid_slot, 15, 7W55_Chai-1_ligand
set grid_slot, 16, 7W57_experimental
set grid_slot, 16, 7W57_exp_ligand
set grid_slot, 16, 7W57_Chai-1
set grid_slot, 16, 7W57_Chai-1_ligand
set grid_slot, 17, 7VGX_experimental
set grid_slot, 17, 7VGX_exp_ligand
set grid_slot, 17, 7VGX_Chai-1
set grid_slot, 17, 7VGX_Chai-1_ligand
set grid_slot, 18, 8F7W_experimental
set grid_slot, 18, 8F7W_exp_ligand
set grid_slot, 18, 8F7W_Chai-1
set grid_slot, 18, 8F7W_Chai-1_ligand
set grid_slot, 19, 8F7Q_experimental
set grid_slot, 19, 8F7Q_exp_ligand
set grid_slot, 19, 8F7Q_Chai-1
set grid_slot, 19, 8F7Q_Chai-1_ligand
set grid_slot, 20, 8F7X_experimental
set grid_slot, 20, 8F7X_exp_ligand
set grid_slot, 20, 8F7X_Chai-1
set grid_slot, 20, 8F7X_Chai-1_ligand
set grid_slot, 21, 7T10_experimental
set grid_slot, 21, 7T10_exp_ligand
set grid_slot, 21, 7T10_Chai-1
set grid_slot, 21, 7T10_Chai-1_ligand
set grid_slot, 22, 7T11_experimental
set grid_slot, 22, 7T11_exp_ligand
set grid_slot, 22, 7T11_Chai-1
set grid_slot, 22, 7T11_Chai-1_ligand
set grid_slot, 23, 7XMS_experimental
set grid_slot, 23, 7XMS_exp_ligand
set grid_slot, 23, 7XMS_Chai-1
set grid_slot, 23, 7XMS_Chai-1_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
