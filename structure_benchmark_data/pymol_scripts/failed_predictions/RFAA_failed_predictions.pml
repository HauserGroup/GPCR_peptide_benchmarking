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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7SK4.pdb, 7SK4_RFAA
align 7SK4_RFAA, 7SK4_experimental
color grey70, chain A and 7SK4_RFAA
color white, chain A and 7SK4_experimental
color RF-AA, 7SK4_RFAA and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_RFAA_ligand, 7SK4_RFAA and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_RFAA_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_RFAA_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7F6I.pdb, 7F6I_RFAA
align 7F6I_experimental, 7SK4_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8IA8.pdb, 8IA8_RFAA
align 8IA8_experimental, 7SK4_experimental 
align 8IA8_RFAA, 8IA8_experimental
color grey70, chain A and 8IA8_RFAA
color white, chain A and 8IA8_experimental
color RF-AA, 8IA8_RFAA and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_RFAA_ligand, 8IA8_RFAA and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_RFAA_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_RFAA_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8HK2.pdb, 8HK2_RFAA
align 8HK2_experimental, 7SK4_experimental 
align 8HK2_RFAA, 8HK2_experimental
color grey70, chain A and 8HK2_RFAA
color white, chain A and 8HK2_experimental
color RF-AA, 8HK2_RFAA and chain B
color experimental_color, 8HK2_experimental and chain B
create 8HK2_exp_ligand, 8HK2_experimental and chain B
create 8HK2_RFAA_ligand, 8HK2_RFAA and chain B
show cartoon, 8HK2_exp_ligand
show cartoon, 8HK2_RFAA_ligand
set cartoon_oval_width, 0.7, 8HK2_exp_ligand
set cartoon_oval_width, 0.7, 8HK2_RFAA_ligand
set cartoon_loop_radius, 0.7, 8HK2_exp_ligand
set cartoon_loop_radius, 0.7, 8HK2_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7Y64_AB.pdb, 7Y64_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7Y64.pdb, 7Y64_RFAA
align 7Y64_experimental, 7SK4_experimental 
align 7Y64_RFAA, 7Y64_experimental
color grey70, chain A and 7Y64_RFAA
color white, chain A and 7Y64_experimental
color RF-AA, 7Y64_RFAA and chain B
color experimental_color, 7Y64_experimental and chain B
create 7Y64_exp_ligand, 7Y64_experimental and chain B
create 7Y64_RFAA_ligand, 7Y64_RFAA and chain B
show cartoon, 7Y64_exp_ligand
show cartoon, 7Y64_RFAA_ligand
set cartoon_oval_width, 0.7, 7Y64_exp_ligand
set cartoon_oval_width, 0.7, 7Y64_RFAA_ligand
set cartoon_loop_radius, 0.7, 7Y64_exp_ligand
set cartoon_loop_radius, 0.7, 7Y64_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W40_AB.pdb, 7W40_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W40.pdb, 7W40_RFAA
align 7W40_experimental, 7SK4_experimental 
align 7W40_RFAA, 7W40_experimental
color grey70, chain A and 7W40_RFAA
color white, chain A and 7W40_experimental
color RF-AA, 7W40_RFAA and chain B
color experimental_color, 7W40_experimental and chain B
create 7W40_exp_ligand, 7W40_experimental and chain B
create 7W40_RFAA_ligand, 7W40_RFAA and chain B
show cartoon, 7W40_exp_ligand
show cartoon, 7W40_RFAA_ligand
set cartoon_oval_width, 0.7, 7W40_exp_ligand
set cartoon_oval_width, 0.7, 7W40_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W40_exp_ligand
set cartoon_loop_radius, 0.7, 7W40_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W3Z.pdb, 7W3Z_RFAA
align 7W3Z_experimental, 7SK4_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8DWG_AB.pdb, 8DWG_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8DWG.pdb, 8DWG_RFAA
align 8DWG_experimental, 7SK4_experimental 
align 8DWG_RFAA, 8DWG_experimental
color grey70, chain A and 8DWG_RFAA
color white, chain A and 8DWG_experimental
color RF-AA, 8DWG_RFAA and chain B
color experimental_color, 8DWG_experimental and chain B
create 8DWG_exp_ligand, 8DWG_experimental and chain B
create 8DWG_RFAA_ligand, 8DWG_RFAA and chain B
show cartoon, 8DWG_exp_ligand
show cartoon, 8DWG_RFAA_ligand
set cartoon_oval_width, 0.7, 8DWG_exp_ligand
set cartoon_oval_width, 0.7, 8DWG_RFAA_ligand
set cartoon_loop_radius, 0.7, 8DWG_exp_ligand
set cartoon_loop_radius, 0.7, 8DWG_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7S8L.pdb, 7S8L_RFAA
align 7S8L_experimental, 7SK4_experimental 
align 7S8L_RFAA, 7S8L_experimental
color grey70, chain A and 7S8L_RFAA
color white, chain A and 7S8L_experimental
color RF-AA, 7S8L_RFAA and chain B
color experimental_color, 7S8L_experimental and chain B
create 7S8L_exp_ligand, 7S8L_experimental and chain B
create 7S8L_RFAA_ligand, 7S8L_RFAA and chain B
show cartoon, 7S8L_exp_ligand
show cartoon, 7S8L_RFAA_ligand
set cartoon_oval_width, 0.7, 7S8L_exp_ligand
set cartoon_oval_width, 0.7, 7S8L_RFAA_ligand
set cartoon_loop_radius, 0.7, 7S8L_exp_ligand
set cartoon_loop_radius, 0.7, 7S8L_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VDM_AB.pdb, 7VDM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7VDM.pdb, 7VDM_RFAA
align 7VDM_experimental, 7SK4_experimental 
align 7VDM_RFAA, 7VDM_experimental
color grey70, chain A and 7VDM_RFAA
color white, chain A and 7VDM_experimental
color RF-AA, 7VDM_RFAA and chain B
color experimental_color, 7VDM_experimental and chain B
create 7VDM_exp_ligand, 7VDM_experimental and chain B
create 7VDM_RFAA_ligand, 7VDM_RFAA and chain B
show cartoon, 7VDM_exp_ligand
show cartoon, 7VDM_RFAA_ligand
set cartoon_oval_width, 0.7, 7VDM_exp_ligand
set cartoon_oval_width, 0.7, 7VDM_RFAA_ligand
set cartoon_loop_radius, 0.7, 7VDM_exp_ligand
set cartoon_loop_radius, 0.7, 7VDM_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VV0_AB.pdb, 7VV0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7VV0.pdb, 7VV0_RFAA
align 7VV0_experimental, 7SK4_experimental 
align 7VV0_RFAA, 7VV0_experimental
color grey70, chain A and 7VV0_RFAA
color white, chain A and 7VV0_experimental
color RF-AA, 7VV0_RFAA and chain B
color experimental_color, 7VV0_experimental and chain B
create 7VV0_exp_ligand, 7VV0_experimental and chain B
create 7VV0_RFAA_ligand, 7VV0_RFAA and chain B
show cartoon, 7VV0_exp_ligand
show cartoon, 7VV0_RFAA_ligand
set cartoon_oval_width, 0.7, 7VV0_exp_ligand
set cartoon_oval_width, 0.7, 7VV0_RFAA_ligand
set cartoon_loop_radius, 0.7, 7VV0_exp_ligand
set cartoon_loop_radius, 0.7, 7VV0_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7P00_AB.pdb, 7P00_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7P00.pdb, 7P00_RFAA
align 7P00_experimental, 7SK4_experimental 
align 7P00_RFAA, 7P00_experimental
color grey70, chain A and 7P00_RFAA
color white, chain A and 7P00_experimental
color RF-AA, 7P00_RFAA and chain B
color experimental_color, 7P00_experimental and chain B
create 7P00_exp_ligand, 7P00_experimental and chain B
create 7P00_RFAA_ligand, 7P00_RFAA and chain B
show cartoon, 7P00_exp_ligand
show cartoon, 7P00_RFAA_ligand
set cartoon_oval_width, 0.7, 7P00_exp_ligand
set cartoon_oval_width, 0.7, 7P00_RFAA_ligand
set cartoon_loop_radius, 0.7, 7P00_exp_ligand
set cartoon_loop_radius, 0.7, 7P00_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W56.pdb, 7W56_RFAA
align 7W56_experimental, 7SK4_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W53.pdb, 7W53_RFAA
align 7W53_experimental, 7SK4_experimental 
align 7W53_RFAA, 7W53_experimental
color grey70, chain A and 7W53_RFAA
color white, chain A and 7W53_experimental
color RF-AA, 7W53_RFAA and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_RFAA_ligand, 7W53_RFAA and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_RFAA_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W55.pdb, 7W55_RFAA
align 7W55_experimental, 7SK4_experimental 
align 7W55_RFAA, 7W55_experimental
color grey70, chain A and 7W55_RFAA
color white, chain A and 7W55_experimental
color RF-AA, 7W55_RFAA and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_RFAA_ligand, 7W55_RFAA and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_RFAA_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7W57.pdb, 7W57_RFAA
align 7W57_experimental, 7SK4_experimental 
align 7W57_RFAA, 7W57_experimental
color grey70, chain A and 7W57_RFAA
color white, chain A and 7W57_experimental
color RF-AA, 7W57_RFAA and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_RFAA_ligand, 7W57_RFAA and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_RFAA_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_RFAA_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VGX_AB.pdb, 7VGX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7VGX.pdb, 7VGX_RFAA
align 7VGX_experimental, 7SK4_experimental 
align 7VGX_RFAA, 7VGX_experimental
color grey70, chain A and 7VGX_RFAA
color white, chain A and 7VGX_experimental
color RF-AA, 7VGX_RFAA and chain B
color experimental_color, 7VGX_experimental and chain B
create 7VGX_exp_ligand, 7VGX_experimental and chain B
create 7VGX_RFAA_ligand, 7VGX_RFAA and chain B
show cartoon, 7VGX_exp_ligand
show cartoon, 7VGX_RFAA_ligand
set cartoon_oval_width, 0.7, 7VGX_exp_ligand
set cartoon_oval_width, 0.7, 7VGX_RFAA_ligand
set cartoon_loop_radius, 0.7, 7VGX_exp_ligand
set cartoon_loop_radius, 0.7, 7VGX_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8F7W.pdb, 8F7W_RFAA
align 8F7W_experimental, 7SK4_experimental 
align 8F7W_RFAA, 8F7W_experimental
color grey70, chain A and 8F7W_RFAA
color white, chain A and 8F7W_experimental
color RF-AA, 8F7W_RFAA and chain B
color experimental_color, 8F7W_experimental and chain B
create 8F7W_exp_ligand, 8F7W_experimental and chain B
create 8F7W_RFAA_ligand, 8F7W_RFAA and chain B
show cartoon, 8F7W_exp_ligand
show cartoon, 8F7W_RFAA_ligand
set cartoon_oval_width, 0.7, 8F7W_exp_ligand
set cartoon_oval_width, 0.7, 8F7W_RFAA_ligand
set cartoon_loop_radius, 0.7, 8F7W_exp_ligand
set cartoon_loop_radius, 0.7, 8F7W_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7Q_AB.pdb, 8F7Q_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8F7Q.pdb, 8F7Q_RFAA
align 8F7Q_experimental, 7SK4_experimental 
align 8F7Q_RFAA, 8F7Q_experimental
color grey70, chain A and 8F7Q_RFAA
color white, chain A and 8F7Q_experimental
color RF-AA, 8F7Q_RFAA and chain B
color experimental_color, 8F7Q_experimental and chain B
create 8F7Q_exp_ligand, 8F7Q_experimental and chain B
create 8F7Q_RFAA_ligand, 8F7Q_RFAA and chain B
show cartoon, 8F7Q_exp_ligand
show cartoon, 8F7Q_RFAA_ligand
set cartoon_oval_width, 0.7, 8F7Q_exp_ligand
set cartoon_oval_width, 0.7, 8F7Q_RFAA_ligand
set cartoon_loop_radius, 0.7, 8F7Q_exp_ligand
set cartoon_loop_radius, 0.7, 8F7Q_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/8F7X.pdb, 8F7X_RFAA
align 8F7X_experimental, 7SK4_experimental 
align 8F7X_RFAA, 8F7X_experimental
color grey70, chain A and 8F7X_RFAA
color white, chain A and 8F7X_experimental
color RF-AA, 8F7X_RFAA and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_RFAA_ligand, 8F7X_RFAA and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_RFAA_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_RFAA_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7T10.pdb, 7T10_RFAA
align 7T10_experimental, 7SK4_experimental 
align 7T10_RFAA, 7T10_experimental
color grey70, chain A and 7T10_RFAA
color white, chain A and 7T10_experimental
color RF-AA, 7T10_RFAA and chain B
color experimental_color, 7T10_experimental and chain B
create 7T10_exp_ligand, 7T10_experimental and chain B
create 7T10_RFAA_ligand, 7T10_RFAA and chain B
show cartoon, 7T10_exp_ligand
show cartoon, 7T10_RFAA_ligand
set cartoon_oval_width, 0.7, 7T10_exp_ligand
set cartoon_oval_width, 0.7, 7T10_RFAA_ligand
set cartoon_loop_radius, 0.7, 7T10_exp_ligand
set cartoon_loop_radius, 0.7, 7T10_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T11_AB.pdb, 7T11_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7T11.pdb, 7T11_RFAA
align 7T11_experimental, 7SK4_experimental 
align 7T11_RFAA, 7T11_experimental
color grey70, chain A and 7T11_RFAA
color white, chain A and 7T11_experimental
color RF-AA, 7T11_RFAA and chain B
color experimental_color, 7T11_experimental and chain B
create 7T11_exp_ligand, 7T11_experimental and chain B
create 7T11_RFAA_ligand, 7T11_RFAA and chain B
show cartoon, 7T11_exp_ligand
show cartoon, 7T11_RFAA_ligand
set cartoon_oval_width, 0.7, 7T11_exp_ligand
set cartoon_oval_width, 0.7, 7T11_RFAA_ligand
set cartoon_loop_radius, 0.7, 7T11_exp_ligand
set cartoon_loop_radius, 0.7, 7T11_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XMS_AB.pdb, 7XMS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA_chain/7XMS.pdb, 7XMS_RFAA
align 7XMS_experimental, 7SK4_experimental 
align 7XMS_RFAA, 7XMS_experimental
color grey70, chain A and 7XMS_RFAA
color white, chain A and 7XMS_experimental
color RF-AA, 7XMS_RFAA and chain B
color experimental_color, 7XMS_experimental and chain B
create 7XMS_exp_ligand, 7XMS_experimental and chain B
create 7XMS_RFAA_ligand, 7XMS_RFAA and chain B
show cartoon, 7XMS_exp_ligand
show cartoon, 7XMS_RFAA_ligand
set cartoon_oval_width, 0.7, 7XMS_exp_ligand
set cartoon_oval_width, 0.7, 7XMS_RFAA_ligand
set cartoon_loop_radius, 0.7, 7XMS_exp_ligand
set cartoon_loop_radius, 0.7, 7XMS_RFAA_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_RFAA
set grid_slot, 1, 7SK4_RFAA_ligand
set grid_slot, 2, 7F6I_experimental
set grid_slot, 2, 7F6I_exp_ligand
set grid_slot, 2, 7F6I_RFAA
set grid_slot, 2, 7F6I_RFAA_ligand
set grid_slot, 3, 8IA8_experimental
set grid_slot, 3, 8IA8_exp_ligand
set grid_slot, 3, 8IA8_RFAA
set grid_slot, 3, 8IA8_RFAA_ligand
set grid_slot, 4, 8HK2_experimental
set grid_slot, 4, 8HK2_exp_ligand
set grid_slot, 4, 8HK2_RFAA
set grid_slot, 4, 8HK2_RFAA_ligand
set grid_slot, 5, 7Y64_experimental
set grid_slot, 5, 7Y64_exp_ligand
set grid_slot, 5, 7Y64_RFAA
set grid_slot, 5, 7Y64_RFAA_ligand
set grid_slot, 6, 7W40_experimental
set grid_slot, 6, 7W40_exp_ligand
set grid_slot, 6, 7W40_RFAA
set grid_slot, 6, 7W40_RFAA_ligand
set grid_slot, 7, 7W3Z_experimental
set grid_slot, 7, 7W3Z_exp_ligand
set grid_slot, 7, 7W3Z_RFAA
set grid_slot, 7, 7W3Z_RFAA_ligand
set grid_slot, 8, 8DWG_experimental
set grid_slot, 8, 8DWG_exp_ligand
set grid_slot, 8, 8DWG_RFAA
set grid_slot, 8, 8DWG_RFAA_ligand
set grid_slot, 9, 7S8L_experimental
set grid_slot, 9, 7S8L_exp_ligand
set grid_slot, 9, 7S8L_RFAA
set grid_slot, 9, 7S8L_RFAA_ligand
set grid_slot, 10, 7VDM_experimental
set grid_slot, 10, 7VDM_exp_ligand
set grid_slot, 10, 7VDM_RFAA
set grid_slot, 10, 7VDM_RFAA_ligand
set grid_slot, 11, 7VV0_experimental
set grid_slot, 11, 7VV0_exp_ligand
set grid_slot, 11, 7VV0_RFAA
set grid_slot, 11, 7VV0_RFAA_ligand
set grid_slot, 12, 7P00_experimental
set grid_slot, 12, 7P00_exp_ligand
set grid_slot, 12, 7P00_RFAA
set grid_slot, 12, 7P00_RFAA_ligand
set grid_slot, 13, 7W56_experimental
set grid_slot, 13, 7W56_exp_ligand
set grid_slot, 13, 7W56_RFAA
set grid_slot, 13, 7W56_RFAA_ligand
set grid_slot, 14, 7W53_experimental
set grid_slot, 14, 7W53_exp_ligand
set grid_slot, 14, 7W53_RFAA
set grid_slot, 14, 7W53_RFAA_ligand
set grid_slot, 15, 7W55_experimental
set grid_slot, 15, 7W55_exp_ligand
set grid_slot, 15, 7W55_RFAA
set grid_slot, 15, 7W55_RFAA_ligand
set grid_slot, 16, 7W57_experimental
set grid_slot, 16, 7W57_exp_ligand
set grid_slot, 16, 7W57_RFAA
set grid_slot, 16, 7W57_RFAA_ligand
set grid_slot, 17, 7VGX_experimental
set grid_slot, 17, 7VGX_exp_ligand
set grid_slot, 17, 7VGX_RFAA
set grid_slot, 17, 7VGX_RFAA_ligand
set grid_slot, 18, 8F7W_experimental
set grid_slot, 18, 8F7W_exp_ligand
set grid_slot, 18, 8F7W_RFAA
set grid_slot, 18, 8F7W_RFAA_ligand
set grid_slot, 19, 8F7Q_experimental
set grid_slot, 19, 8F7Q_exp_ligand
set grid_slot, 19, 8F7Q_RFAA
set grid_slot, 19, 8F7Q_RFAA_ligand
set grid_slot, 20, 8F7X_experimental
set grid_slot, 20, 8F7X_exp_ligand
set grid_slot, 20, 8F7X_RFAA
set grid_slot, 20, 8F7X_RFAA_ligand
set grid_slot, 21, 7T10_experimental
set grid_slot, 21, 7T10_exp_ligand
set grid_slot, 21, 7T10_RFAA
set grid_slot, 21, 7T10_RFAA_ligand
set grid_slot, 22, 7T11_experimental
set grid_slot, 22, 7T11_exp_ligand
set grid_slot, 22, 7T11_RFAA
set grid_slot, 22, 7T11_RFAA_ligand
set grid_slot, 23, 7XMS_experimental
set grid_slot, 23, 7XMS_exp_ligand
set grid_slot, 23, 7XMS_RFAA
set grid_slot, 23, 7XMS_RFAA_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
