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
set_color ESMFold, [0.278, 0.514, 0.278]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7SK4.pdb, 7SK4_ESMFold
align 7SK4_ESMFold, 7SK4_experimental
color grey70, chain A and 7SK4_ESMFold
color white, chain A and 7SK4_experimental
color ESMFold, 7SK4_ESMFold and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_ESMFold_ligand, 7SK4_ESMFold and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_ESMFold_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8GY7_AB.pdb, 8GY7_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8GY7.pdb, 8GY7_ESMFold
align 8GY7_experimental, 7SK4_experimental 
align 8GY7_ESMFold, 8GY7_experimental
color grey70, chain A and 8GY7_ESMFold
color white, chain A and 8GY7_experimental
color ESMFold, 8GY7_ESMFold and chain B
color experimental_color, 8GY7_experimental and chain B
create 8GY7_exp_ligand, 8GY7_experimental and chain B
create 8GY7_ESMFold_ligand, 8GY7_ESMFold and chain B
show cartoon, 8GY7_exp_ligand
show cartoon, 8GY7_ESMFold_ligand
set cartoon_oval_width, 0.7, 8GY7_exp_ligand
set cartoon_oval_width, 0.7, 8GY7_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8GY7_exp_ligand
set cartoon_loop_radius, 0.7, 8GY7_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7EIB_AB.pdb, 7EIB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7EIB.pdb, 7EIB_ESMFold
align 7EIB_experimental, 7SK4_experimental 
align 7EIB_ESMFold, 7EIB_experimental
color grey70, chain A and 7EIB_ESMFold
color white, chain A and 7EIB_experimental
color ESMFold, 7EIB_ESMFold and chain B
color experimental_color, 7EIB_experimental and chain B
create 7EIB_exp_ligand, 7EIB_experimental and chain B
create 7EIB_ESMFold_ligand, 7EIB_ESMFold and chain B
show cartoon, 7EIB_exp_ligand
show cartoon, 7EIB_ESMFold_ligand
set cartoon_oval_width, 0.7, 7EIB_exp_ligand
set cartoon_oval_width, 0.7, 7EIB_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7EIB_exp_ligand
set cartoon_loop_radius, 0.7, 7EIB_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7F6I.pdb, 7F6I_ESMFold
align 7F6I_experimental, 7SK4_experimental 
align 7F6I_ESMFold, 7F6I_experimental
color grey70, chain A and 7F6I_ESMFold
color white, chain A and 7F6I_experimental
color ESMFold, 7F6I_ESMFold and chain B
color experimental_color, 7F6I_experimental and chain B
create 7F6I_exp_ligand, 7F6I_experimental and chain B
create 7F6I_ESMFold_ligand, 7F6I_ESMFold and chain B
show cartoon, 7F6I_exp_ligand
show cartoon, 7F6I_ESMFold_ligand
set cartoon_oval_width, 0.7, 7F6I_exp_ligand
set cartoon_oval_width, 0.7, 7F6I_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7F6I_exp_ligand
set cartoon_loop_radius, 0.7, 7F6I_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8IA8.pdb, 8IA8_ESMFold
align 8IA8_experimental, 7SK4_experimental 
align 8IA8_ESMFold, 8IA8_experimental
color grey70, chain A and 8IA8_ESMFold
color white, chain A and 8IA8_experimental
color ESMFold, 8IA8_ESMFold and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_ESMFold_ligand, 8IA8_ESMFold and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_ESMFold_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8I95_AB.pdb, 8I95_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8I95.pdb, 8I95_ESMFold
align 8I95_experimental, 7SK4_experimental 
align 8I95_ESMFold, 8I95_experimental
color grey70, chain A and 8I95_ESMFold
color white, chain A and 8I95_experimental
color ESMFold, 8I95_ESMFold and chain B
color experimental_color, 8I95_experimental and chain B
create 8I95_exp_ligand, 8I95_experimental and chain B
create 8I95_ESMFold_ligand, 8I95_ESMFold and chain B
show cartoon, 8I95_exp_ligand
show cartoon, 8I95_ESMFold_ligand
set cartoon_oval_width, 0.7, 8I95_exp_ligand
set cartoon_oval_width, 0.7, 8I95_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8I95_exp_ligand
set cartoon_loop_radius, 0.7, 8I95_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8HK2.pdb, 8HK2_ESMFold
align 8HK2_experimental, 7SK4_experimental 
align 8HK2_ESMFold, 8HK2_experimental
color grey70, chain A and 8HK2_ESMFold
color white, chain A and 8HK2_experimental
color ESMFold, 8HK2_ESMFold and chain B
color experimental_color, 8HK2_experimental and chain B
create 8HK2_exp_ligand, 8HK2_experimental and chain B
create 8HK2_ESMFold_ligand, 8HK2_ESMFold and chain B
show cartoon, 8HK2_exp_ligand
show cartoon, 8HK2_ESMFold_ligand
set cartoon_oval_width, 0.7, 8HK2_exp_ligand
set cartoon_oval_width, 0.7, 8HK2_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8HK2_exp_ligand
set cartoon_loop_radius, 0.7, 8HK2_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F0K_AB.pdb, 8F0K_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8F0K.pdb, 8F0K_ESMFold
align 8F0K_experimental, 7SK4_experimental 
align 8F0K_ESMFold, 8F0K_experimental
color grey70, chain A and 8F0K_ESMFold
color white, chain A and 8F0K_experimental
color ESMFold, 8F0K_ESMFold and chain B
color experimental_color, 8F0K_experimental and chain B
create 8F0K_exp_ligand, 8F0K_experimental and chain B
create 8F0K_ESMFold_ligand, 8F0K_ESMFold and chain B
show cartoon, 8F0K_exp_ligand
show cartoon, 8F0K_ESMFold_ligand
set cartoon_oval_width, 0.7, 8F0K_exp_ligand
set cartoon_oval_width, 0.7, 8F0K_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8F0K_exp_ligand
set cartoon_loop_radius, 0.7, 8F0K_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/9AUC_AB.pdb, 9AUC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/9AUC.pdb, 9AUC_ESMFold
align 9AUC_experimental, 7SK4_experimental 
align 9AUC_ESMFold, 9AUC_experimental
color grey70, chain A and 9AUC_ESMFold
color white, chain A and 9AUC_experimental
color ESMFold, 9AUC_ESMFold and chain B
color experimental_color, 9AUC_experimental and chain B
create 9AUC_exp_ligand, 9AUC_experimental and chain B
create 9AUC_ESMFold_ligand, 9AUC_ESMFold and chain B
show cartoon, 9AUC_exp_ligand
show cartoon, 9AUC_ESMFold_ligand
set cartoon_oval_width, 0.7, 9AUC_exp_ligand
set cartoon_oval_width, 0.7, 9AUC_ESMFold_ligand
set cartoon_loop_radius, 0.7, 9AUC_exp_ligand
set cartoon_loop_radius, 0.7, 9AUC_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7TYO_AB.pdb, 7TYO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7TYO.pdb, 7TYO_ESMFold
align 7TYO_experimental, 7SK4_experimental 
align 7TYO_ESMFold, 7TYO_experimental
color grey70, chain A and 7TYO_ESMFold
color white, chain A and 7TYO_experimental
color ESMFold, 7TYO_ESMFold and chain B
color experimental_color, 7TYO_experimental and chain B
create 7TYO_exp_ligand, 7TYO_experimental and chain B
create 7TYO_ESMFold_ligand, 7TYO_ESMFold and chain B
show cartoon, 7TYO_exp_ligand
show cartoon, 7TYO_ESMFold_ligand
set cartoon_oval_width, 0.7, 7TYO_exp_ligand
set cartoon_oval_width, 0.7, 7TYO_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7TYO_exp_ligand
set cartoon_loop_radius, 0.7, 7TYO_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VL9_AB.pdb, 7VL9_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7VL9.pdb, 7VL9_ESMFold
align 7VL9_experimental, 7SK4_experimental 
align 7VL9_ESMFold, 7VL9_experimental
color grey70, chain A and 7VL9_ESMFold
color white, chain A and 7VL9_experimental
color ESMFold, 7VL9_ESMFold and chain B
color experimental_color, 7VL9_experimental and chain B
create 7VL9_exp_ligand, 7VL9_experimental and chain B
create 7VL9_ESMFold_ligand, 7VL9_ESMFold and chain B
show cartoon, 7VL9_exp_ligand
show cartoon, 7VL9_ESMFold_ligand
set cartoon_oval_width, 0.7, 7VL9_exp_ligand
set cartoon_oval_width, 0.7, 7VL9_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7VL9_exp_ligand
set cartoon_loop_radius, 0.7, 7VL9_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XA3_AB.pdb, 7XA3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7XA3.pdb, 7XA3_ESMFold
align 7XA3_experimental, 7SK4_experimental 
align 7XA3_ESMFold, 7XA3_experimental
color grey70, chain A and 7XA3_ESMFold
color white, chain A and 7XA3_experimental
color ESMFold, 7XA3_ESMFold and chain B
color experimental_color, 7XA3_experimental and chain B
create 7XA3_exp_ligand, 7XA3_experimental and chain B
create 7XA3_ESMFold_ligand, 7XA3_ESMFold and chain B
show cartoon, 7XA3_exp_ligand
show cartoon, 7XA3_ESMFold_ligand
set cartoon_oval_width, 0.7, 7XA3_exp_ligand
set cartoon_oval_width, 0.7, 7XA3_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7XA3_exp_ligand
set cartoon_loop_radius, 0.7, 7XA3_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YKD_AB.pdb, 7YKD_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7YKD.pdb, 7YKD_ESMFold
align 7YKD_experimental, 7SK4_experimental 
align 7YKD_ESMFold, 7YKD_experimental
color grey70, chain A and 7YKD_ESMFold
color white, chain A and 7YKD_experimental
color ESMFold, 7YKD_ESMFold and chain B
color experimental_color, 7YKD_experimental and chain B
create 7YKD_exp_ligand, 7YKD_experimental and chain B
create 7YKD_ESMFold_ligand, 7YKD_ESMFold and chain B
show cartoon, 7YKD_exp_ligand
show cartoon, 7YKD_ESMFold_ligand
set cartoon_oval_width, 0.7, 7YKD_exp_ligand
set cartoon_oval_width, 0.7, 7YKD_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7YKD_exp_ligand
set cartoon_loop_radius, 0.7, 7YKD_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JJP_AB.pdb, 8JJP_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8JJP.pdb, 8JJP_ESMFold
align 8JJP_experimental, 7SK4_experimental 
align 8JJP_ESMFold, 8JJP_experimental
color grey70, chain A and 8JJP_ESMFold
color white, chain A and 8JJP_experimental
color ESMFold, 8JJP_ESMFold and chain B
color experimental_color, 8JJP_experimental and chain B
create 8JJP_exp_ligand, 8JJP_experimental and chain B
create 8JJP_ESMFold_ligand, 8JJP_ESMFold and chain B
show cartoon, 8JJP_exp_ligand
show cartoon, 8JJP_ESMFold_ligand
set cartoon_oval_width, 0.7, 8JJP_exp_ligand
set cartoon_oval_width, 0.7, 8JJP_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8JJP_exp_ligand
set cartoon_loop_radius, 0.7, 8JJP_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGM_AB.pdb, 8XGM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8XGM.pdb, 8XGM_ESMFold
align 8XGM_experimental, 7SK4_experimental 
align 8XGM_ESMFold, 8XGM_experimental
color grey70, chain A and 8XGM_ESMFold
color white, chain A and 8XGM_experimental
color ESMFold, 8XGM_ESMFold and chain B
color experimental_color, 8XGM_experimental and chain B
create 8XGM_exp_ligand, 8XGM_experimental and chain B
create 8XGM_ESMFold_ligand, 8XGM_ESMFold and chain B
show cartoon, 8XGM_exp_ligand
show cartoon, 8XGM_ESMFold_ligand
set cartoon_oval_width, 0.7, 8XGM_exp_ligand
set cartoon_oval_width, 0.7, 8XGM_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8XGM_exp_ligand
set cartoon_loop_radius, 0.7, 8XGM_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IC0_AB.pdb, 8IC0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8IC0.pdb, 8IC0_ESMFold
align 8IC0_experimental, 7SK4_experimental 
align 8IC0_ESMFold, 8IC0_experimental
color grey70, chain A and 8IC0_ESMFold
color white, chain A and 8IC0_experimental
color ESMFold, 8IC0_ESMFold and chain B
color experimental_color, 8IC0_experimental and chain B
create 8IC0_exp_ligand, 8IC0_experimental and chain B
create 8IC0_ESMFold_ligand, 8IC0_ESMFold and chain B
show cartoon, 8IC0_exp_ligand
show cartoon, 8IC0_ESMFold_ligand
set cartoon_oval_width, 0.7, 8IC0_exp_ligand
set cartoon_oval_width, 0.7, 8IC0_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8IC0_exp_ligand
set cartoon_loop_radius, 0.7, 8IC0_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HNK_AB.pdb, 8HNK_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8HNK.pdb, 8HNK_ESMFold
align 8HNK_experimental, 7SK4_experimental 
align 8HNK_ESMFold, 8HNK_experimental
color grey70, chain A and 8HNK_ESMFold
color white, chain A and 8HNK_experimental
color ESMFold, 8HNK_ESMFold and chain B
color experimental_color, 8HNK_experimental and chain B
create 8HNK_exp_ligand, 8HNK_experimental and chain B
create 8HNK_ESMFold_ligand, 8HNK_ESMFold and chain B
show cartoon, 8HNK_exp_ligand
show cartoon, 8HNK_ESMFold_ligand
set cartoon_oval_width, 0.7, 8HNK_exp_ligand
set cartoon_oval_width, 0.7, 8HNK_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8HNK_exp_ligand
set cartoon_loop_radius, 0.7, 8HNK_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HCQ_AB.pdb, 8HCQ_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8HCQ.pdb, 8HCQ_ESMFold
align 8HCQ_experimental, 7SK4_experimental 
align 8HCQ_ESMFold, 8HCQ_experimental
color grey70, chain A and 8HCQ_ESMFold
color white, chain A and 8HCQ_experimental
color ESMFold, 8HCQ_ESMFold and chain B
color experimental_color, 8HCQ_experimental and chain B
create 8HCQ_exp_ligand, 8HCQ_experimental and chain B
create 8HCQ_ESMFold_ligand, 8HCQ_ESMFold and chain B
show cartoon, 8HCQ_exp_ligand
show cartoon, 8HCQ_ESMFold_ligand
set cartoon_oval_width, 0.7, 8HCQ_exp_ligand
set cartoon_oval_width, 0.7, 8HCQ_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8HCQ_exp_ligand
set cartoon_loop_radius, 0.7, 8HCQ_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ3_AB.pdb, 7WQ3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7WQ3.pdb, 7WQ3_ESMFold
align 7WQ3_experimental, 7SK4_experimental 
align 7WQ3_ESMFold, 7WQ3_experimental
color grey70, chain A and 7WQ3_ESMFold
color white, chain A and 7WQ3_experimental
color ESMFold, 7WQ3_ESMFold and chain B
color experimental_color, 7WQ3_experimental and chain B
create 7WQ3_exp_ligand, 7WQ3_experimental and chain B
create 7WQ3_ESMFold_ligand, 7WQ3_ESMFold and chain B
show cartoon, 7WQ3_exp_ligand
show cartoon, 7WQ3_ESMFold_ligand
set cartoon_oval_width, 0.7, 7WQ3_exp_ligand
set cartoon_oval_width, 0.7, 7WQ3_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7WQ3_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ3_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7WQ4.pdb, 7WQ4_ESMFold
align 7WQ4_experimental, 7SK4_experimental 
align 7WQ4_ESMFold, 7WQ4_experimental
color grey70, chain A and 7WQ4_ESMFold
color white, chain A and 7WQ4_experimental
color ESMFold, 7WQ4_ESMFold and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_ESMFold_ligand, 7WQ4_ESMFold and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_ESMFold_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA7_AB.pdb, 8IA7_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8IA7.pdb, 8IA7_ESMFold
align 8IA7_experimental, 7SK4_experimental 
align 8IA7_ESMFold, 8IA7_experimental
color grey70, chain A and 8IA7_ESMFold
color white, chain A and 8IA7_experimental
color ESMFold, 8IA7_ESMFold and chain B
color experimental_color, 8IA7_experimental and chain B
create 8IA7_exp_ligand, 8IA7_experimental and chain B
create 8IA7_ESMFold_ligand, 8IA7_ESMFold and chain B
show cartoon, 8IA7_exp_ligand
show cartoon, 8IA7_ESMFold_ligand
set cartoon_oval_width, 0.7, 8IA7_exp_ligand
set cartoon_oval_width, 0.7, 8IA7_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8IA7_exp_ligand
set cartoon_loop_radius, 0.7, 8IA7_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XOW_AB.pdb, 7XOW_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7XOW.pdb, 7XOW_ESMFold
align 7XOW_experimental, 7SK4_experimental 
align 7XOW_ESMFold, 7XOW_experimental
color grey70, chain A and 7XOW_ESMFold
color white, chain A and 7XOW_experimental
color ESMFold, 7XOW_ESMFold and chain B
color experimental_color, 7XOW_experimental and chain B
create 7XOW_exp_ligand, 7XOW_experimental and chain B
create 7XOW_ESMFold_ligand, 7XOW_ESMFold and chain B
show cartoon, 7XOW_exp_ligand
show cartoon, 7XOW_ESMFold_ligand
set cartoon_oval_width, 0.7, 7XOW_exp_ligand
set cartoon_oval_width, 0.7, 7XOW_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7XOW_exp_ligand
set cartoon_loop_radius, 0.7, 7XOW_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RBT_AB.pdb, 7RBT_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7RBT.pdb, 7RBT_ESMFold
align 7RBT_experimental, 7SK4_experimental 
align 7RBT_ESMFold, 7RBT_experimental
color grey70, chain A and 7RBT_ESMFold
color white, chain A and 7RBT_experimental
color ESMFold, 7RBT_ESMFold and chain B
color experimental_color, 7RBT_experimental and chain B
create 7RBT_exp_ligand, 7RBT_experimental and chain B
create 7RBT_ESMFold_ligand, 7RBT_ESMFold and chain B
show cartoon, 7RBT_exp_ligand
show cartoon, 7RBT_ESMFold_ligand
set cartoon_oval_width, 0.7, 7RBT_exp_ligand
set cartoon_oval_width, 0.7, 7RBT_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7RBT_exp_ligand
set cartoon_loop_radius, 0.7, 7RBT_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7FIN_AB.pdb, 7FIN_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7FIN.pdb, 7FIN_ESMFold
align 7FIN_experimental, 7SK4_experimental 
align 7FIN_ESMFold, 7FIN_experimental
color grey70, chain A and 7FIN_ESMFold
color white, chain A and 7FIN_experimental
color ESMFold, 7FIN_ESMFold and chain B
color experimental_color, 7FIN_experimental and chain B
create 7FIN_exp_ligand, 7FIN_experimental and chain B
create 7FIN_ESMFold_ligand, 7FIN_ESMFold and chain B
show cartoon, 7FIN_exp_ligand
show cartoon, 7FIN_ESMFold_ligand
set cartoon_oval_width, 0.7, 7FIN_exp_ligand
set cartoon_oval_width, 0.7, 7FIN_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7FIN_exp_ligand
set cartoon_loop_radius, 0.7, 7FIN_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8YW4_AB.pdb, 8YW4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8YW4.pdb, 8YW4_ESMFold
align 8YW4_experimental, 7SK4_experimental 
align 8YW4_ESMFold, 8YW4_experimental
color grey70, chain A and 8YW4_ESMFold
color white, chain A and 8YW4_experimental
color ESMFold, 8YW4_ESMFold and chain B
color experimental_color, 8YW4_experimental and chain B
create 8YW4_exp_ligand, 8YW4_experimental and chain B
create 8YW4_ESMFold_ligand, 8YW4_ESMFold and chain B
show cartoon, 8YW4_exp_ligand
show cartoon, 8YW4_ESMFold_ligand
set cartoon_oval_width, 0.7, 8YW4_exp_ligand
set cartoon_oval_width, 0.7, 8YW4_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8YW4_exp_ligand
set cartoon_loop_radius, 0.7, 8YW4_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7W3Z.pdb, 7W3Z_ESMFold
align 7W3Z_experimental, 7SK4_experimental 
align 7W3Z_ESMFold, 7W3Z_experimental
color grey70, chain A and 7W3Z_ESMFold
color white, chain A and 7W3Z_experimental
color ESMFold, 7W3Z_ESMFold and chain B
color experimental_color, 7W3Z_experimental and chain B
create 7W3Z_exp_ligand, 7W3Z_experimental and chain B
create 7W3Z_ESMFold_ligand, 7W3Z_ESMFold and chain B
show cartoon, 7W3Z_exp_ligand
show cartoon, 7W3Z_ESMFold_ligand
set cartoon_oval_width, 0.7, 7W3Z_exp_ligand
set cartoon_oval_width, 0.7, 7W3Z_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7W3Z_exp_ligand
set cartoon_loop_radius, 0.7, 7W3Z_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGS_AB.pdb, 8XGS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8XGS.pdb, 8XGS_ESMFold
align 8XGS_experimental, 7SK4_experimental 
align 8XGS_ESMFold, 8XGS_experimental
color grey70, chain A and 8XGS_ESMFold
color white, chain A and 8XGS_experimental
color ESMFold, 8XGS_ESMFold and chain B
color experimental_color, 8XGS_experimental and chain B
create 8XGS_exp_ligand, 8XGS_experimental and chain B
create 8XGS_ESMFold_ligand, 8XGS_ESMFold and chain B
show cartoon, 8XGS_exp_ligand
show cartoon, 8XGS_ESMFold_ligand
set cartoon_oval_width, 0.7, 8XGS_exp_ligand
set cartoon_oval_width, 0.7, 8XGS_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8XGS_exp_ligand
set cartoon_loop_radius, 0.7, 8XGS_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8WVY.pdb, 8WVY_ESMFold
align 8WVY_experimental, 7SK4_experimental 
align 8WVY_ESMFold, 8WVY_experimental
color grey70, chain A and 8WVY_ESMFold
color white, chain A and 8WVY_experimental
color ESMFold, 8WVY_ESMFold and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_ESMFold_ligand, 8WVY_ESMFold and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_ESMFold_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IOC_AB.pdb, 8IOC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8IOC.pdb, 8IOC_ESMFold
align 8IOC_experimental, 7SK4_experimental 
align 8IOC_ESMFold, 8IOC_experimental
color grey70, chain A and 8IOC_ESMFold
color white, chain A and 8IOC_experimental
color ESMFold, 8IOC_ESMFold and chain B
color experimental_color, 8IOC_experimental and chain B
create 8IOC_exp_ligand, 8IOC_experimental and chain B
create 8IOC_ESMFold_ligand, 8IOC_ESMFold and chain B
show cartoon, 8IOC_exp_ligand
show cartoon, 8IOC_ESMFold_ligand
set cartoon_oval_width, 0.7, 8IOC_exp_ligand
set cartoon_oval_width, 0.7, 8IOC_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8IOC_exp_ligand
set cartoon_loop_radius, 0.7, 8IOC_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8INR_AB.pdb, 8INR_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8INR.pdb, 8INR_ESMFold
align 8INR_experimental, 7SK4_experimental 
align 8INR_ESMFold, 8INR_experimental
color grey70, chain A and 8INR_ESMFold
color white, chain A and 8INR_experimental
color ESMFold, 8INR_ESMFold and chain B
color experimental_color, 8INR_experimental and chain B
create 8INR_exp_ligand, 8INR_experimental and chain B
create 8INR_ESMFold_ligand, 8INR_ESMFold and chain B
show cartoon, 8INR_exp_ligand
show cartoon, 8INR_ESMFold_ligand
set cartoon_oval_width, 0.7, 8INR_exp_ligand
set cartoon_oval_width, 0.7, 8INR_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8INR_exp_ligand
set cartoon_loop_radius, 0.7, 8INR_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WSS_AB.pdb, 8WSS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8WSS.pdb, 8WSS_ESMFold
align 8WSS_experimental, 7SK4_experimental 
align 8WSS_ESMFold, 8WSS_experimental
color grey70, chain A and 8WSS_ESMFold
color white, chain A and 8WSS_experimental
color ESMFold, 8WSS_ESMFold and chain B
color experimental_color, 8WSS_experimental and chain B
create 8WSS_exp_ligand, 8WSS_experimental and chain B
create 8WSS_ESMFold_ligand, 8WSS_ESMFold and chain B
show cartoon, 8WSS_exp_ligand
show cartoon, 8WSS_ESMFold_ligand
set cartoon_oval_width, 0.7, 8WSS_exp_ligand
set cartoon_oval_width, 0.7, 8WSS_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8WSS_exp_ligand
set cartoon_loop_radius, 0.7, 8WSS_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WST_AB.pdb, 8WST_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8WST.pdb, 8WST_ESMFold
align 8WST_experimental, 7SK4_experimental 
align 8WST_ESMFold, 8WST_experimental
color grey70, chain A and 8WST_ESMFold
color white, chain A and 8WST_experimental
color ESMFold, 8WST_ESMFold and chain B
color experimental_color, 8WST_experimental and chain B
create 8WST_exp_ligand, 8WST_experimental and chain B
create 8WST_ESMFold_ligand, 8WST_ESMFold and chain B
show cartoon, 8WST_exp_ligand
show cartoon, 8WST_ESMFold_ligand
set cartoon_oval_width, 0.7, 8WST_exp_ligand
set cartoon_oval_width, 0.7, 8WST_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8WST_exp_ligand
set cartoon_loop_radius, 0.7, 8WST_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGF_AB.pdb, 8JGF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8JGF.pdb, 8JGF_ESMFold
align 8JGF_experimental, 7SK4_experimental 
align 8JGF_ESMFold, 8JGF_experimental
color grey70, chain A and 8JGF_ESMFold
color white, chain A and 8JGF_experimental
color ESMFold, 8JGF_ESMFold and chain B
color experimental_color, 8JGF_experimental and chain B
create 8JGF_exp_ligand, 8JGF_experimental and chain B
create 8JGF_ESMFold_ligand, 8JGF_ESMFold and chain B
show cartoon, 8JGF_exp_ligand
show cartoon, 8JGF_ESMFold_ligand
set cartoon_oval_width, 0.7, 8JGF_exp_ligand
set cartoon_oval_width, 0.7, 8JGF_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8JGF_exp_ligand
set cartoon_loop_radius, 0.7, 8JGF_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGB_AB.pdb, 8JGB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8JGB.pdb, 8JGB_ESMFold
align 8JGB_experimental, 7SK4_experimental 
align 8JGB_ESMFold, 8JGB_experimental
color grey70, chain A and 8JGB_ESMFold
color white, chain A and 8JGB_experimental
color ESMFold, 8JGB_ESMFold and chain B
color experimental_color, 8JGB_experimental and chain B
create 8JGB_exp_ligand, 8JGB_experimental and chain B
create 8JGB_ESMFold_ligand, 8JGB_ESMFold and chain B
show cartoon, 8JGB_exp_ligand
show cartoon, 8JGB_ESMFold_ligand
set cartoon_oval_width, 0.7, 8JGB_exp_ligand
set cartoon_oval_width, 0.7, 8JGB_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8JGB_exp_ligand
set cartoon_loop_radius, 0.7, 8JGB_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7S8L.pdb, 7S8L_ESMFold
align 7S8L_experimental, 7SK4_experimental 
align 7S8L_ESMFold, 7S8L_experimental
color grey70, chain A and 7S8L_ESMFold
color white, chain A and 7S8L_experimental
color ESMFold, 7S8L_ESMFold and chain B
color experimental_color, 7S8L_experimental and chain B
create 7S8L_exp_ligand, 7S8L_experimental and chain B
create 7S8L_ESMFold_ligand, 7S8L_ESMFold and chain B
show cartoon, 7S8L_exp_ligand
show cartoon, 7S8L_ESMFold_ligand
set cartoon_oval_width, 0.7, 7S8L_exp_ligand
set cartoon_oval_width, 0.7, 7S8L_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7S8L_exp_ligand
set cartoon_loop_radius, 0.7, 7S8L_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VDM_AB.pdb, 7VDM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7VDM.pdb, 7VDM_ESMFold
align 7VDM_experimental, 7SK4_experimental 
align 7VDM_ESMFold, 7VDM_experimental
color grey70, chain A and 7VDM_ESMFold
color white, chain A and 7VDM_experimental
color ESMFold, 7VDM_ESMFold and chain B
color experimental_color, 7VDM_experimental and chain B
create 7VDM_exp_ligand, 7VDM_experimental and chain B
create 7VDM_ESMFold_ligand, 7VDM_ESMFold and chain B
show cartoon, 7VDM_exp_ligand
show cartoon, 7VDM_ESMFold_ligand
set cartoon_oval_width, 0.7, 7VDM_exp_ligand
set cartoon_oval_width, 0.7, 7VDM_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7VDM_exp_ligand
set cartoon_loop_radius, 0.7, 7VDM_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VV0_AB.pdb, 7VV0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7VV0.pdb, 7VV0_ESMFold
align 7VV0_experimental, 7SK4_experimental 
align 7VV0_ESMFold, 7VV0_experimental
color grey70, chain A and 7VV0_ESMFold
color white, chain A and 7VV0_experimental
color ESMFold, 7VV0_ESMFold and chain B
color experimental_color, 7VV0_experimental and chain B
create 7VV0_exp_ligand, 7VV0_experimental and chain B
create 7VV0_ESMFold_ligand, 7VV0_ESMFold and chain B
show cartoon, 7VV0_exp_ligand
show cartoon, 7VV0_ESMFold_ligand
set cartoon_oval_width, 0.7, 7VV0_exp_ligand
set cartoon_oval_width, 0.7, 7VV0_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7VV0_exp_ligand
set cartoon_loop_radius, 0.7, 7VV0_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IBV_AB.pdb, 8IBV_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8IBV.pdb, 8IBV_ESMFold
align 8IBV_experimental, 7SK4_experimental 
align 8IBV_ESMFold, 8IBV_experimental
color grey70, chain A and 8IBV_ESMFold
color white, chain A and 8IBV_experimental
color ESMFold, 8IBV_ESMFold and chain B
color experimental_color, 8IBV_experimental and chain B
create 8IBV_exp_ligand, 8IBV_experimental and chain B
create 8IBV_ESMFold_ligand, 8IBV_ESMFold and chain B
show cartoon, 8IBV_exp_ligand
show cartoon, 8IBV_ESMFold_ligand
set cartoon_oval_width, 0.7, 8IBV_exp_ligand
set cartoon_oval_width, 0.7, 8IBV_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8IBV_exp_ligand
set cartoon_loop_radius, 0.7, 8IBV_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XWO_AB.pdb, 7XWO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7XWO.pdb, 7XWO_ESMFold
align 7XWO_experimental, 7SK4_experimental 
align 7XWO_ESMFold, 7XWO_experimental
color grey70, chain A and 7XWO_ESMFold
color white, chain A and 7XWO_experimental
color ESMFold, 7XWO_ESMFold and chain B
color experimental_color, 7XWO_experimental and chain B
create 7XWO_exp_ligand, 7XWO_experimental and chain B
create 7XWO_ESMFold_ligand, 7XWO_ESMFold and chain B
show cartoon, 7XWO_exp_ligand
show cartoon, 7XWO_ESMFold_ligand
set cartoon_oval_width, 0.7, 7XWO_exp_ligand
set cartoon_oval_width, 0.7, 7XWO_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7XWO_exp_ligand
set cartoon_loop_radius, 0.7, 7XWO_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JBF_AB.pdb, 8JBF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8JBF.pdb, 8JBF_ESMFold
align 8JBF_experimental, 7SK4_experimental 
align 8JBF_ESMFold, 8JBF_experimental
color grey70, chain A and 8JBF_ESMFold
color white, chain A and 8JBF_experimental
color ESMFold, 8JBF_ESMFold and chain B
color experimental_color, 8JBF_experimental and chain B
create 8JBF_exp_ligand, 8JBF_experimental and chain B
create 8JBF_ESMFold_ligand, 8JBF_ESMFold and chain B
show cartoon, 8JBF_exp_ligand
show cartoon, 8JBF_ESMFold_ligand
set cartoon_oval_width, 0.7, 8JBF_exp_ligand
set cartoon_oval_width, 0.7, 8JBF_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8JBF_exp_ligand
set cartoon_loop_radius, 0.7, 8JBF_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8H0P_AB.pdb, 8H0P_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8H0P.pdb, 8H0P_ESMFold
align 8H0P_experimental, 7SK4_experimental 
align 8H0P_ESMFold, 8H0P_experimental
color grey70, chain A and 8H0P_ESMFold
color white, chain A and 8H0P_experimental
color ESMFold, 8H0P_ESMFold and chain B
color experimental_color, 8H0P_experimental and chain B
create 8H0P_exp_ligand, 8H0P_experimental and chain B
create 8H0P_ESMFold_ligand, 8H0P_ESMFold and chain B
show cartoon, 8H0P_exp_ligand
show cartoon, 8H0P_ESMFold_ligand
set cartoon_oval_width, 0.7, 8H0P_exp_ligand
set cartoon_oval_width, 0.7, 8H0P_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8H0P_exp_ligand
set cartoon_loop_radius, 0.7, 8H0P_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7W56.pdb, 7W56_ESMFold
align 7W56_experimental, 7SK4_experimental 
align 7W56_ESMFold, 7W56_experimental
color grey70, chain A and 7W56_ESMFold
color white, chain A and 7W56_experimental
color ESMFold, 7W56_ESMFold and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_ESMFold_ligand, 7W56_ESMFold and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_ESMFold_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7W53.pdb, 7W53_ESMFold
align 7W53_experimental, 7SK4_experimental 
align 7W53_ESMFold, 7W53_experimental
color grey70, chain A and 7W53_ESMFold
color white, chain A and 7W53_experimental
color ESMFold, 7W53_ESMFold and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_ESMFold_ligand, 7W53_ESMFold and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_ESMFold_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7W55.pdb, 7W55_ESMFold
align 7W55_experimental, 7SK4_experimental 
align 7W55_ESMFold, 7W55_experimental
color grey70, chain A and 7W55_ESMFold
color white, chain A and 7W55_experimental
color ESMFold, 7W55_ESMFold and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_ESMFold_ligand, 7W55_ESMFold and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_ESMFold_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7W57.pdb, 7W57_ESMFold
align 7W57_experimental, 7SK4_experimental 
align 7W57_ESMFold, 7W57_experimental
color grey70, chain A and 7W57_ESMFold
color white, chain A and 7W57_experimental
color ESMFold, 7W57_ESMFold and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_ESMFold_ligand, 7W57_ESMFold and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_ESMFold_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VGX_AB.pdb, 7VGX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7VGX.pdb, 7VGX_ESMFold
align 7VGX_experimental, 7SK4_experimental 
align 7VGX_ESMFold, 7VGX_experimental
color grey70, chain A and 7VGX_ESMFold
color white, chain A and 7VGX_experimental
color ESMFold, 7VGX_ESMFold and chain B
color experimental_color, 7VGX_experimental and chain B
create 7VGX_exp_ligand, 7VGX_experimental and chain B
create 7VGX_ESMFold_ligand, 7VGX_ESMFold and chain B
show cartoon, 7VGX_exp_ligand
show cartoon, 7VGX_ESMFold_ligand
set cartoon_oval_width, 0.7, 7VGX_exp_ligand
set cartoon_oval_width, 0.7, 7VGX_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7VGX_exp_ligand
set cartoon_loop_radius, 0.7, 7VGX_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YON_AB.pdb, 7YON_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7YON.pdb, 7YON_ESMFold
align 7YON_experimental, 7SK4_experimental 
align 7YON_ESMFold, 7YON_experimental
color grey70, chain A and 7YON_ESMFold
color white, chain A and 7YON_experimental
color ESMFold, 7YON_ESMFold and chain B
color experimental_color, 7YON_experimental and chain B
create 7YON_exp_ligand, 7YON_experimental and chain B
create 7YON_ESMFold_ligand, 7YON_ESMFold and chain B
show cartoon, 7YON_exp_ligand
show cartoon, 7YON_ESMFold_ligand
set cartoon_oval_width, 0.7, 7YON_exp_ligand
set cartoon_oval_width, 0.7, 7YON_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7YON_exp_ligand
set cartoon_loop_radius, 0.7, 7YON_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YOO_AB.pdb, 7YOO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7YOO.pdb, 7YOO_ESMFold
align 7YOO_experimental, 7SK4_experimental 
align 7YOO_ESMFold, 7YOO_experimental
color grey70, chain A and 7YOO_ESMFold
color white, chain A and 7YOO_experimental
color ESMFold, 7YOO_ESMFold and chain B
color experimental_color, 7YOO_experimental and chain B
create 7YOO_exp_ligand, 7YOO_experimental and chain B
create 7YOO_ESMFold_ligand, 7YOO_ESMFold and chain B
show cartoon, 7YOO_exp_ligand
show cartoon, 7YOO_ESMFold_ligand
set cartoon_oval_width, 0.7, 7YOO_exp_ligand
set cartoon_oval_width, 0.7, 7YOO_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7YOO_exp_ligand
set cartoon_loop_radius, 0.7, 7YOO_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7X9C_AB.pdb, 7X9C_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7X9C.pdb, 7X9C_ESMFold
align 7X9C_experimental, 7SK4_experimental 
align 7X9C_ESMFold, 7X9C_experimental
color grey70, chain A and 7X9C_ESMFold
color white, chain A and 7X9C_experimental
color ESMFold, 7X9C_ESMFold and chain B
color experimental_color, 7X9C_experimental and chain B
create 7X9C_exp_ligand, 7X9C_experimental and chain B
create 7X9C_ESMFold_ligand, 7X9C_ESMFold and chain B
show cartoon, 7X9C_exp_ligand
show cartoon, 7X9C_ESMFold_ligand
set cartoon_oval_width, 0.7, 7X9C_exp_ligand
set cartoon_oval_width, 0.7, 7X9C_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7X9C_exp_ligand
set cartoon_loop_radius, 0.7, 7X9C_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8F7W.pdb, 8F7W_ESMFold
align 8F7W_experimental, 7SK4_experimental 
align 8F7W_ESMFold, 8F7W_experimental
color grey70, chain A and 8F7W_ESMFold
color white, chain A and 8F7W_experimental
color ESMFold, 8F7W_ESMFold and chain B
color experimental_color, 8F7W_experimental and chain B
create 8F7W_exp_ligand, 8F7W_experimental and chain B
create 8F7W_ESMFold_ligand, 8F7W_ESMFold and chain B
show cartoon, 8F7W_exp_ligand
show cartoon, 8F7W_ESMFold_ligand
set cartoon_oval_width, 0.7, 8F7W_exp_ligand
set cartoon_oval_width, 0.7, 8F7W_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8F7W_exp_ligand
set cartoon_loop_radius, 0.7, 8F7W_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8K9K_AB.pdb, 8K9K_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8K9K.pdb, 8K9K_ESMFold
align 8K9K_experimental, 7SK4_experimental 
align 8K9K_ESMFold, 8K9K_experimental
color grey70, chain A and 8K9K_ESMFold
color white, chain A and 8K9K_experimental
color ESMFold, 8K9K_ESMFold and chain B
color experimental_color, 8K9K_experimental and chain B
create 8K9K_exp_ligand, 8K9K_experimental and chain B
create 8K9K_ESMFold_ligand, 8K9K_ESMFold and chain B
show cartoon, 8K9K_exp_ligand
show cartoon, 8K9K_ESMFold_ligand
set cartoon_oval_width, 0.7, 8K9K_exp_ligand
set cartoon_oval_width, 0.7, 8K9K_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8K9K_exp_ligand
set cartoon_loop_radius, 0.7, 8K9K_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7Q_AB.pdb, 8F7Q_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8F7Q.pdb, 8F7Q_ESMFold
align 8F7Q_experimental, 7SK4_experimental 
align 8F7Q_ESMFold, 8F7Q_experimental
color grey70, chain A and 8F7Q_ESMFold
color white, chain A and 8F7Q_experimental
color ESMFold, 8F7Q_ESMFold and chain B
color experimental_color, 8F7Q_experimental and chain B
create 8F7Q_exp_ligand, 8F7Q_experimental and chain B
create 8F7Q_ESMFold_ligand, 8F7Q_ESMFold and chain B
show cartoon, 8F7Q_exp_ligand
show cartoon, 8F7Q_ESMFold_ligand
set cartoon_oval_width, 0.7, 8F7Q_exp_ligand
set cartoon_oval_width, 0.7, 8F7Q_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8F7Q_exp_ligand
set cartoon_loop_radius, 0.7, 8F7Q_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7R_AB.pdb, 8F7R_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8F7R.pdb, 8F7R_ESMFold
align 8F7R_experimental, 7SK4_experimental 
align 8F7R_ESMFold, 8F7R_experimental
color grey70, chain A and 8F7R_ESMFold
color white, chain A and 8F7R_experimental
color ESMFold, 8F7R_ESMFold and chain B
color experimental_color, 8F7R_experimental and chain B
create 8F7R_exp_ligand, 8F7R_experimental and chain B
create 8F7R_ESMFold_ligand, 8F7R_ESMFold and chain B
show cartoon, 8F7R_exp_ligand
show cartoon, 8F7R_ESMFold_ligand
set cartoon_oval_width, 0.7, 8F7R_exp_ligand
set cartoon_oval_width, 0.7, 8F7R_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8F7R_exp_ligand
set cartoon_loop_radius, 0.7, 8F7R_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8F7X.pdb, 8F7X_ESMFold
align 8F7X_experimental, 7SK4_experimental 
align 8F7X_ESMFold, 8F7X_experimental
color grey70, chain A and 8F7X_ESMFold
color white, chain A and 8F7X_experimental
color ESMFold, 8F7X_ESMFold and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_ESMFold_ligand, 8F7X_ESMFold and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_ESMFold_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RYC_AB.pdb, 7RYC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7RYC.pdb, 7RYC_ESMFold
align 7RYC_experimental, 7SK4_experimental 
align 7RYC_ESMFold, 7RYC_experimental
color grey70, chain A and 7RYC_ESMFold
color white, chain A and 7RYC_experimental
color ESMFold, 7RYC_ESMFold and chain B
color experimental_color, 7RYC_experimental and chain B
create 7RYC_exp_ligand, 7RYC_experimental and chain B
create 7RYC_ESMFold_ligand, 7RYC_ESMFold and chain B
show cartoon, 7RYC_exp_ligand
show cartoon, 7RYC_ESMFold_ligand
set cartoon_oval_width, 0.7, 7RYC_exp_ligand
set cartoon_oval_width, 0.7, 7RYC_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7RYC_exp_ligand
set cartoon_loop_radius, 0.7, 7RYC_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8ZPT_AB.pdb, 8ZPT_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8ZPT.pdb, 8ZPT_ESMFold
align 8ZPT_experimental, 7SK4_experimental 
align 8ZPT_ESMFold, 8ZPT_experimental
color grey70, chain A and 8ZPT_ESMFold
color white, chain A and 8ZPT_experimental
color ESMFold, 8ZPT_ESMFold and chain B
color experimental_color, 8ZPT_experimental and chain B
create 8ZPT_exp_ligand, 8ZPT_experimental and chain B
create 8ZPT_ESMFold_ligand, 8ZPT_ESMFold and chain B
show cartoon, 8ZPT_exp_ligand
show cartoon, 8ZPT_ESMFold_ligand
set cartoon_oval_width, 0.7, 8ZPT_exp_ligand
set cartoon_oval_width, 0.7, 8ZPT_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8ZPT_exp_ligand
set cartoon_loop_radius, 0.7, 8ZPT_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WZ2_AB.pdb, 8WZ2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8WZ2.pdb, 8WZ2_ESMFold
align 8WZ2_experimental, 7SK4_experimental 
align 8WZ2_ESMFold, 8WZ2_experimental
color grey70, chain A and 8WZ2_ESMFold
color white, chain A and 8WZ2_experimental
color ESMFold, 8WZ2_ESMFold and chain B
color experimental_color, 8WZ2_experimental and chain B
create 8WZ2_exp_ligand, 8WZ2_experimental and chain B
create 8WZ2_ESMFold_ligand, 8WZ2_ESMFold and chain B
show cartoon, 8WZ2_exp_ligand
show cartoon, 8WZ2_ESMFold_ligand
set cartoon_oval_width, 0.7, 8WZ2_exp_ligand
set cartoon_oval_width, 0.7, 8WZ2_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8WZ2_exp_ligand
set cartoon_loop_radius, 0.7, 8WZ2_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8ZH8_AB.pdb, 8ZH8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8ZH8.pdb, 8ZH8_ESMFold
align 8ZH8_experimental, 7SK4_experimental 
align 8ZH8_ESMFold, 8ZH8_experimental
color grey70, chain A and 8ZH8_ESMFold
color white, chain A and 8ZH8_experimental
color ESMFold, 8ZH8_ESMFold and chain B
color experimental_color, 8ZH8_experimental and chain B
create 8ZH8_exp_ligand, 8ZH8_experimental and chain B
create 8ZH8_ESMFold_ligand, 8ZH8_ESMFold and chain B
show cartoon, 8ZH8_exp_ligand
show cartoon, 8ZH8_ESMFold_ligand
set cartoon_oval_width, 0.7, 8ZH8_exp_ligand
set cartoon_oval_width, 0.7, 8ZH8_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8ZH8_exp_ligand
set cartoon_loop_radius, 0.7, 8ZH8_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7T10.pdb, 7T10_ESMFold
align 7T10_experimental, 7SK4_experimental 
align 7T10_ESMFold, 7T10_experimental
color grey70, chain A and 7T10_ESMFold
color white, chain A and 7T10_experimental
color ESMFold, 7T10_ESMFold and chain B
color experimental_color, 7T10_experimental and chain B
create 7T10_exp_ligand, 7T10_experimental and chain B
create 7T10_ESMFold_ligand, 7T10_ESMFold and chain B
show cartoon, 7T10_exp_ligand
show cartoon, 7T10_ESMFold_ligand
set cartoon_oval_width, 0.7, 7T10_exp_ligand
set cartoon_oval_width, 0.7, 7T10_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7T10_exp_ligand
set cartoon_loop_radius, 0.7, 7T10_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T11_AB.pdb, 7T11_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7T11.pdb, 7T11_ESMFold
align 7T11_experimental, 7SK4_experimental 
align 7T11_ESMFold, 7T11_experimental
color grey70, chain A and 7T11_ESMFold
color white, chain A and 7T11_experimental
color ESMFold, 7T11_ESMFold and chain B
color experimental_color, 7T11_experimental and chain B
create 7T11_exp_ligand, 7T11_experimental and chain B
create 7T11_ESMFold_ligand, 7T11_ESMFold and chain B
show cartoon, 7T11_exp_ligand
show cartoon, 7T11_ESMFold_ligand
set cartoon_oval_width, 0.7, 7T11_exp_ligand
set cartoon_oval_width, 0.7, 7T11_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7T11_exp_ligand
set cartoon_loop_radius, 0.7, 7T11_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XMS_AB.pdb, 7XMS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7XMS.pdb, 7XMS_ESMFold
align 7XMS_experimental, 7SK4_experimental 
align 7XMS_ESMFold, 7XMS_experimental
color grey70, chain A and 7XMS_ESMFold
color white, chain A and 7XMS_experimental
color ESMFold, 7XMS_ESMFold and chain B
color experimental_color, 7XMS_experimental and chain B
create 7XMS_exp_ligand, 7XMS_experimental and chain B
create 7XMS_ESMFold_ligand, 7XMS_ESMFold and chain B
show cartoon, 7XMS_exp_ligand
show cartoon, 7XMS_ESMFold_ligand
set cartoon_oval_width, 0.7, 7XMS_exp_ligand
set cartoon_oval_width, 0.7, 7XMS_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7XMS_exp_ligand
set cartoon_loop_radius, 0.7, 7XMS_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8L_AB.pdb, 8X8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8X8L.pdb, 8X8L_ESMFold
align 8X8L_experimental, 7SK4_experimental 
align 8X8L_ESMFold, 8X8L_experimental
color grey70, chain A and 8X8L_ESMFold
color white, chain A and 8X8L_experimental
color ESMFold, 8X8L_ESMFold and chain B
color experimental_color, 8X8L_experimental and chain B
create 8X8L_exp_ligand, 8X8L_experimental and chain B
create 8X8L_ESMFold_ligand, 8X8L_ESMFold and chain B
show cartoon, 8X8L_exp_ligand
show cartoon, 8X8L_ESMFold_ligand
set cartoon_oval_width, 0.7, 8X8L_exp_ligand
set cartoon_oval_width, 0.7, 8X8L_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8X8L_exp_ligand
set cartoon_loop_radius, 0.7, 8X8L_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8N_AB.pdb, 8X8N_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/8X8N.pdb, 8X8N_ESMFold
align 8X8N_experimental, 7SK4_experimental 
align 8X8N_ESMFold, 8X8N_experimental
color grey70, chain A and 8X8N_ESMFold
color white, chain A and 8X8N_experimental
color ESMFold, 8X8N_ESMFold and chain B
color experimental_color, 8X8N_experimental and chain B
create 8X8N_exp_ligand, 8X8N_experimental and chain B
create 8X8N_ESMFold_ligand, 8X8N_ESMFold and chain B
show cartoon, 8X8N_exp_ligand
show cartoon, 8X8N_ESMFold_ligand
set cartoon_oval_width, 0.7, 8X8N_exp_ligand
set cartoon_oval_width, 0.7, 8X8N_ESMFold_ligand
set cartoon_loop_radius, 0.7, 8X8N_exp_ligand
set cartoon_loop_radius, 0.7, 8X8N_ESMFold_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VQX_AB.pdb, 7VQX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/ESMFold/7VQX.pdb, 7VQX_ESMFold
align 7VQX_experimental, 7SK4_experimental 
align 7VQX_ESMFold, 7VQX_experimental
color grey70, chain A and 7VQX_ESMFold
color white, chain A and 7VQX_experimental
color ESMFold, 7VQX_ESMFold and chain B
color experimental_color, 7VQX_experimental and chain B
create 7VQX_exp_ligand, 7VQX_experimental and chain B
create 7VQX_ESMFold_ligand, 7VQX_ESMFold and chain B
show cartoon, 7VQX_exp_ligand
show cartoon, 7VQX_ESMFold_ligand
set cartoon_oval_width, 0.7, 7VQX_exp_ligand
set cartoon_oval_width, 0.7, 7VQX_ESMFold_ligand
set cartoon_loop_radius, 0.7, 7VQX_exp_ligand
set cartoon_loop_radius, 0.7, 7VQX_ESMFold_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_ESMFold
set grid_slot, 1, 7SK4_ESMFold_ligand
set grid_slot, 2, 8GY7_experimental
set grid_slot, 2, 8GY7_exp_ligand
set grid_slot, 2, 8GY7_ESMFold
set grid_slot, 2, 8GY7_ESMFold_ligand
set grid_slot, 3, 7EIB_experimental
set grid_slot, 3, 7EIB_exp_ligand
set grid_slot, 3, 7EIB_ESMFold
set grid_slot, 3, 7EIB_ESMFold_ligand
set grid_slot, 4, 7F6I_experimental
set grid_slot, 4, 7F6I_exp_ligand
set grid_slot, 4, 7F6I_ESMFold
set grid_slot, 4, 7F6I_ESMFold_ligand
set grid_slot, 5, 8IA8_experimental
set grid_slot, 5, 8IA8_exp_ligand
set grid_slot, 5, 8IA8_ESMFold
set grid_slot, 5, 8IA8_ESMFold_ligand
set grid_slot, 6, 8I95_experimental
set grid_slot, 6, 8I95_exp_ligand
set grid_slot, 6, 8I95_ESMFold
set grid_slot, 6, 8I95_ESMFold_ligand
set grid_slot, 7, 8HK2_experimental
set grid_slot, 7, 8HK2_exp_ligand
set grid_slot, 7, 8HK2_ESMFold
set grid_slot, 7, 8HK2_ESMFold_ligand
set grid_slot, 8, 8F0K_experimental
set grid_slot, 8, 8F0K_exp_ligand
set grid_slot, 8, 8F0K_ESMFold
set grid_slot, 8, 8F0K_ESMFold_ligand
set grid_slot, 9, 9AUC_experimental
set grid_slot, 9, 9AUC_exp_ligand
set grid_slot, 9, 9AUC_ESMFold
set grid_slot, 9, 9AUC_ESMFold_ligand
set grid_slot, 10, 7TYO_experimental
set grid_slot, 10, 7TYO_exp_ligand
set grid_slot, 10, 7TYO_ESMFold
set grid_slot, 10, 7TYO_ESMFold_ligand
set grid_slot, 11, 7VL9_experimental
set grid_slot, 11, 7VL9_exp_ligand
set grid_slot, 11, 7VL9_ESMFold
set grid_slot, 11, 7VL9_ESMFold_ligand
set grid_slot, 12, 7XA3_experimental
set grid_slot, 12, 7XA3_exp_ligand
set grid_slot, 12, 7XA3_ESMFold
set grid_slot, 12, 7XA3_ESMFold_ligand
set grid_slot, 13, 7YKD_experimental
set grid_slot, 13, 7YKD_exp_ligand
set grid_slot, 13, 7YKD_ESMFold
set grid_slot, 13, 7YKD_ESMFold_ligand
set grid_slot, 14, 8JJP_experimental
set grid_slot, 14, 8JJP_exp_ligand
set grid_slot, 14, 8JJP_ESMFold
set grid_slot, 14, 8JJP_ESMFold_ligand
set grid_slot, 15, 8XGM_experimental
set grid_slot, 15, 8XGM_exp_ligand
set grid_slot, 15, 8XGM_ESMFold
set grid_slot, 15, 8XGM_ESMFold_ligand
set grid_slot, 16, 8IC0_experimental
set grid_slot, 16, 8IC0_exp_ligand
set grid_slot, 16, 8IC0_ESMFold
set grid_slot, 16, 8IC0_ESMFold_ligand
set grid_slot, 17, 8HNK_experimental
set grid_slot, 17, 8HNK_exp_ligand
set grid_slot, 17, 8HNK_ESMFold
set grid_slot, 17, 8HNK_ESMFold_ligand
set grid_slot, 18, 8HCQ_experimental
set grid_slot, 18, 8HCQ_exp_ligand
set grid_slot, 18, 8HCQ_ESMFold
set grid_slot, 18, 8HCQ_ESMFold_ligand
set grid_slot, 19, 7WQ3_experimental
set grid_slot, 19, 7WQ3_exp_ligand
set grid_slot, 19, 7WQ3_ESMFold
set grid_slot, 19, 7WQ3_ESMFold_ligand
set grid_slot, 20, 7WQ4_experimental
set grid_slot, 20, 7WQ4_exp_ligand
set grid_slot, 20, 7WQ4_ESMFold
set grid_slot, 20, 7WQ4_ESMFold_ligand
set grid_slot, 21, 8IA7_experimental
set grid_slot, 21, 8IA7_exp_ligand
set grid_slot, 21, 8IA7_ESMFold
set grid_slot, 21, 8IA7_ESMFold_ligand
set grid_slot, 22, 7XOW_experimental
set grid_slot, 22, 7XOW_exp_ligand
set grid_slot, 22, 7XOW_ESMFold
set grid_slot, 22, 7XOW_ESMFold_ligand
set grid_slot, 23, 7RBT_experimental
set grid_slot, 23, 7RBT_exp_ligand
set grid_slot, 23, 7RBT_ESMFold
set grid_slot, 23, 7RBT_ESMFold_ligand
set grid_slot, 24, 7FIN_experimental
set grid_slot, 24, 7FIN_exp_ligand
set grid_slot, 24, 7FIN_ESMFold
set grid_slot, 24, 7FIN_ESMFold_ligand
set grid_slot, 25, 8YW4_experimental
set grid_slot, 25, 8YW4_exp_ligand
set grid_slot, 25, 8YW4_ESMFold
set grid_slot, 25, 8YW4_ESMFold_ligand
set grid_slot, 26, 7W3Z_experimental
set grid_slot, 26, 7W3Z_exp_ligand
set grid_slot, 26, 7W3Z_ESMFold
set grid_slot, 26, 7W3Z_ESMFold_ligand
set grid_slot, 27, 8XGS_experimental
set grid_slot, 27, 8XGS_exp_ligand
set grid_slot, 27, 8XGS_ESMFold
set grid_slot, 27, 8XGS_ESMFold_ligand
set grid_slot, 28, 8WVY_experimental
set grid_slot, 28, 8WVY_exp_ligand
set grid_slot, 28, 8WVY_ESMFold
set grid_slot, 28, 8WVY_ESMFold_ligand
set grid_slot, 29, 8IOC_experimental
set grid_slot, 29, 8IOC_exp_ligand
set grid_slot, 29, 8IOC_ESMFold
set grid_slot, 29, 8IOC_ESMFold_ligand
set grid_slot, 30, 8INR_experimental
set grid_slot, 30, 8INR_exp_ligand
set grid_slot, 30, 8INR_ESMFold
set grid_slot, 30, 8INR_ESMFold_ligand
set grid_slot, 31, 8WSS_experimental
set grid_slot, 31, 8WSS_exp_ligand
set grid_slot, 31, 8WSS_ESMFold
set grid_slot, 31, 8WSS_ESMFold_ligand
set grid_slot, 32, 8WST_experimental
set grid_slot, 32, 8WST_exp_ligand
set grid_slot, 32, 8WST_ESMFold
set grid_slot, 32, 8WST_ESMFold_ligand
set grid_slot, 33, 8JGF_experimental
set grid_slot, 33, 8JGF_exp_ligand
set grid_slot, 33, 8JGF_ESMFold
set grid_slot, 33, 8JGF_ESMFold_ligand
set grid_slot, 34, 8JGB_experimental
set grid_slot, 34, 8JGB_exp_ligand
set grid_slot, 34, 8JGB_ESMFold
set grid_slot, 34, 8JGB_ESMFold_ligand
set grid_slot, 35, 7S8L_experimental
set grid_slot, 35, 7S8L_exp_ligand
set grid_slot, 35, 7S8L_ESMFold
set grid_slot, 35, 7S8L_ESMFold_ligand
set grid_slot, 36, 7VDM_experimental
set grid_slot, 36, 7VDM_exp_ligand
set grid_slot, 36, 7VDM_ESMFold
set grid_slot, 36, 7VDM_ESMFold_ligand
set grid_slot, 37, 7VV0_experimental
set grid_slot, 37, 7VV0_exp_ligand
set grid_slot, 37, 7VV0_ESMFold
set grid_slot, 37, 7VV0_ESMFold_ligand
set grid_slot, 38, 8IBV_experimental
set grid_slot, 38, 8IBV_exp_ligand
set grid_slot, 38, 8IBV_ESMFold
set grid_slot, 38, 8IBV_ESMFold_ligand
set grid_slot, 39, 7XWO_experimental
set grid_slot, 39, 7XWO_exp_ligand
set grid_slot, 39, 7XWO_ESMFold
set grid_slot, 39, 7XWO_ESMFold_ligand
set grid_slot, 40, 8JBF_experimental
set grid_slot, 40, 8JBF_exp_ligand
set grid_slot, 40, 8JBF_ESMFold
set grid_slot, 40, 8JBF_ESMFold_ligand
set grid_slot, 41, 8H0P_experimental
set grid_slot, 41, 8H0P_exp_ligand
set grid_slot, 41, 8H0P_ESMFold
set grid_slot, 41, 8H0P_ESMFold_ligand
set grid_slot, 42, 7W56_experimental
set grid_slot, 42, 7W56_exp_ligand
set grid_slot, 42, 7W56_ESMFold
set grid_slot, 42, 7W56_ESMFold_ligand
set grid_slot, 43, 7W53_experimental
set grid_slot, 43, 7W53_exp_ligand
set grid_slot, 43, 7W53_ESMFold
set grid_slot, 43, 7W53_ESMFold_ligand
set grid_slot, 44, 7W55_experimental
set grid_slot, 44, 7W55_exp_ligand
set grid_slot, 44, 7W55_ESMFold
set grid_slot, 44, 7W55_ESMFold_ligand
set grid_slot, 45, 7W57_experimental
set grid_slot, 45, 7W57_exp_ligand
set grid_slot, 45, 7W57_ESMFold
set grid_slot, 45, 7W57_ESMFold_ligand
set grid_slot, 46, 7VGX_experimental
set grid_slot, 46, 7VGX_exp_ligand
set grid_slot, 46, 7VGX_ESMFold
set grid_slot, 46, 7VGX_ESMFold_ligand
set grid_slot, 47, 7YON_experimental
set grid_slot, 47, 7YON_exp_ligand
set grid_slot, 47, 7YON_ESMFold
set grid_slot, 47, 7YON_ESMFold_ligand
set grid_slot, 48, 7YOO_experimental
set grid_slot, 48, 7YOO_exp_ligand
set grid_slot, 48, 7YOO_ESMFold
set grid_slot, 48, 7YOO_ESMFold_ligand
set grid_slot, 49, 7X9C_experimental
set grid_slot, 49, 7X9C_exp_ligand
set grid_slot, 49, 7X9C_ESMFold
set grid_slot, 49, 7X9C_ESMFold_ligand
set grid_slot, 50, 8F7W_experimental
set grid_slot, 50, 8F7W_exp_ligand
set grid_slot, 50, 8F7W_ESMFold
set grid_slot, 50, 8F7W_ESMFold_ligand
set grid_slot, 51, 8K9K_experimental
set grid_slot, 51, 8K9K_exp_ligand
set grid_slot, 51, 8K9K_ESMFold
set grid_slot, 51, 8K9K_ESMFold_ligand
set grid_slot, 52, 8F7Q_experimental
set grid_slot, 52, 8F7Q_exp_ligand
set grid_slot, 52, 8F7Q_ESMFold
set grid_slot, 52, 8F7Q_ESMFold_ligand
set grid_slot, 53, 8F7R_experimental
set grid_slot, 53, 8F7R_exp_ligand
set grid_slot, 53, 8F7R_ESMFold
set grid_slot, 53, 8F7R_ESMFold_ligand
set grid_slot, 54, 8F7X_experimental
set grid_slot, 54, 8F7X_exp_ligand
set grid_slot, 54, 8F7X_ESMFold
set grid_slot, 54, 8F7X_ESMFold_ligand
set grid_slot, 55, 7RYC_experimental
set grid_slot, 55, 7RYC_exp_ligand
set grid_slot, 55, 7RYC_ESMFold
set grid_slot, 55, 7RYC_ESMFold_ligand
set grid_slot, 56, 8ZPT_experimental
set grid_slot, 56, 8ZPT_exp_ligand
set grid_slot, 56, 8ZPT_ESMFold
set grid_slot, 56, 8ZPT_ESMFold_ligand
set grid_slot, 57, 8WZ2_experimental
set grid_slot, 57, 8WZ2_exp_ligand
set grid_slot, 57, 8WZ2_ESMFold
set grid_slot, 57, 8WZ2_ESMFold_ligand
set grid_slot, 58, 8ZH8_experimental
set grid_slot, 58, 8ZH8_exp_ligand
set grid_slot, 58, 8ZH8_ESMFold
set grid_slot, 58, 8ZH8_ESMFold_ligand
set grid_slot, 59, 7T10_experimental
set grid_slot, 59, 7T10_exp_ligand
set grid_slot, 59, 7T10_ESMFold
set grid_slot, 59, 7T10_ESMFold_ligand
set grid_slot, 60, 7T11_experimental
set grid_slot, 60, 7T11_exp_ligand
set grid_slot, 60, 7T11_ESMFold
set grid_slot, 60, 7T11_ESMFold_ligand
set grid_slot, 61, 7XMS_experimental
set grid_slot, 61, 7XMS_exp_ligand
set grid_slot, 61, 7XMS_ESMFold
set grid_slot, 61, 7XMS_ESMFold_ligand
set grid_slot, 62, 8X8L_experimental
set grid_slot, 62, 8X8L_exp_ligand
set grid_slot, 62, 8X8L_ESMFold
set grid_slot, 62, 8X8L_ESMFold_ligand
set grid_slot, 63, 8X8N_experimental
set grid_slot, 63, 8X8N_exp_ligand
set grid_slot, 63, 8X8N_ESMFold
set grid_slot, 63, 8X8N_ESMFold_ligand
set grid_slot, 64, 7VQX_experimental
set grid_slot, 64, 7VQX_exp_ligand
set grid_slot, 64, 7VQX_ESMFold
set grid_slot, 64, 7VQX_ESMFold_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
