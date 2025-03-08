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
set_color NeuralPLexer, [0.357, 0.380, 0.420]
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7SK4_AB.pdb, 7SK4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7SK4.pdb, 7SK4_NeuralPLexer
align 7SK4_NeuralPLexer, 7SK4_experimental
color grey70, chain A and 7SK4_NeuralPLexer
color white, chain A and 7SK4_experimental
color NeuralPLexer, 7SK4_NeuralPLexer and chain B
color experimental_color, 7SK4_experimental and chain B
create 7SK4_exp_ligand, 7SK4_experimental and chain B
create 7SK4_NeuralPLexer_ligand, 7SK4_NeuralPLexer and chain B
show cartoon, 7SK4_exp_ligand
show cartoon, 7SK4_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7SK4_exp_ligand
set cartoon_oval_width, 0.7, 7SK4_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7SK4_exp_ligand
set cartoon_loop_radius, 0.7, 7SK4_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8GY7_AB.pdb, 8GY7_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8GY7.pdb, 8GY7_NeuralPLexer
align 8GY7_experimental, 7SK4_experimental 
align 8GY7_NeuralPLexer, 8GY7_experimental
color grey70, chain A and 8GY7_NeuralPLexer
color white, chain A and 8GY7_experimental
color NeuralPLexer, 8GY7_NeuralPLexer and chain B
color experimental_color, 8GY7_experimental and chain B
create 8GY7_exp_ligand, 8GY7_experimental and chain B
create 8GY7_NeuralPLexer_ligand, 8GY7_NeuralPLexer and chain B
show cartoon, 8GY7_exp_ligand
show cartoon, 8GY7_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8GY7_exp_ligand
set cartoon_oval_width, 0.7, 8GY7_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8GY7_exp_ligand
set cartoon_loop_radius, 0.7, 8GY7_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7EIB_AB.pdb, 7EIB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7EIB.pdb, 7EIB_NeuralPLexer
align 7EIB_experimental, 7SK4_experimental 
align 7EIB_NeuralPLexer, 7EIB_experimental
color grey70, chain A and 7EIB_NeuralPLexer
color white, chain A and 7EIB_experimental
color NeuralPLexer, 7EIB_NeuralPLexer and chain B
color experimental_color, 7EIB_experimental and chain B
create 7EIB_exp_ligand, 7EIB_experimental and chain B
create 7EIB_NeuralPLexer_ligand, 7EIB_NeuralPLexer and chain B
show cartoon, 7EIB_exp_ligand
show cartoon, 7EIB_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7EIB_exp_ligand
set cartoon_oval_width, 0.7, 7EIB_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7EIB_exp_ligand
set cartoon_loop_radius, 0.7, 7EIB_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7F6I_AB.pdb, 7F6I_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7F6I.pdb, 7F6I_NeuralPLexer
align 7F6I_experimental, 7SK4_experimental 
align 7F6I_NeuralPLexer, 7F6I_experimental
color grey70, chain A and 7F6I_NeuralPLexer
color white, chain A and 7F6I_experimental
color NeuralPLexer, 7F6I_NeuralPLexer and chain B
color experimental_color, 7F6I_experimental and chain B
create 7F6I_exp_ligand, 7F6I_experimental and chain B
create 7F6I_NeuralPLexer_ligand, 7F6I_NeuralPLexer and chain B
show cartoon, 7F6I_exp_ligand
show cartoon, 7F6I_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7F6I_exp_ligand
set cartoon_oval_width, 0.7, 7F6I_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7F6I_exp_ligand
set cartoon_loop_radius, 0.7, 7F6I_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8IA8.pdb, 8IA8_NeuralPLexer
align 8IA8_experimental, 7SK4_experimental 
align 8IA8_NeuralPLexer, 8IA8_experimental
color grey70, chain A and 8IA8_NeuralPLexer
color white, chain A and 8IA8_experimental
color NeuralPLexer, 8IA8_NeuralPLexer and chain B
color experimental_color, 8IA8_experimental and chain B
create 8IA8_exp_ligand, 8IA8_experimental and chain B
create 8IA8_NeuralPLexer_ligand, 8IA8_NeuralPLexer and chain B
show cartoon, 8IA8_exp_ligand
show cartoon, 8IA8_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8IA8_exp_ligand
set cartoon_oval_width, 0.7, 8IA8_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8IA8_exp_ligand
set cartoon_loop_radius, 0.7, 8IA8_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8I95_AB.pdb, 8I95_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8I95.pdb, 8I95_NeuralPLexer
align 8I95_experimental, 7SK4_experimental 
align 8I95_NeuralPLexer, 8I95_experimental
color grey70, chain A and 8I95_NeuralPLexer
color white, chain A and 8I95_experimental
color NeuralPLexer, 8I95_NeuralPLexer and chain B
color experimental_color, 8I95_experimental and chain B
create 8I95_exp_ligand, 8I95_experimental and chain B
create 8I95_NeuralPLexer_ligand, 8I95_NeuralPLexer and chain B
show cartoon, 8I95_exp_ligand
show cartoon, 8I95_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8I95_exp_ligand
set cartoon_oval_width, 0.7, 8I95_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8I95_exp_ligand
set cartoon_loop_radius, 0.7, 8I95_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8HK2.pdb, 8HK2_NeuralPLexer
align 8HK2_experimental, 7SK4_experimental 
align 8HK2_NeuralPLexer, 8HK2_experimental
color grey70, chain A and 8HK2_NeuralPLexer
color white, chain A and 8HK2_experimental
color NeuralPLexer, 8HK2_NeuralPLexer and chain B
color experimental_color, 8HK2_experimental and chain B
create 8HK2_exp_ligand, 8HK2_experimental and chain B
create 8HK2_NeuralPLexer_ligand, 8HK2_NeuralPLexer and chain B
show cartoon, 8HK2_exp_ligand
show cartoon, 8HK2_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8HK2_exp_ligand
set cartoon_oval_width, 0.7, 8HK2_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8HK2_exp_ligand
set cartoon_loop_radius, 0.7, 8HK2_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F0K_AB.pdb, 8F0K_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8F0K.pdb, 8F0K_NeuralPLexer
align 8F0K_experimental, 7SK4_experimental 
align 8F0K_NeuralPLexer, 8F0K_experimental
color grey70, chain A and 8F0K_NeuralPLexer
color white, chain A and 8F0K_experimental
color NeuralPLexer, 8F0K_NeuralPLexer and chain B
color experimental_color, 8F0K_experimental and chain B
create 8F0K_exp_ligand, 8F0K_experimental and chain B
create 8F0K_NeuralPLexer_ligand, 8F0K_NeuralPLexer and chain B
show cartoon, 8F0K_exp_ligand
show cartoon, 8F0K_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8F0K_exp_ligand
set cartoon_oval_width, 0.7, 8F0K_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8F0K_exp_ligand
set cartoon_loop_radius, 0.7, 8F0K_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/9AUC_AB.pdb, 9AUC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/9AUC.pdb, 9AUC_NeuralPLexer
align 9AUC_experimental, 7SK4_experimental 
align 9AUC_NeuralPLexer, 9AUC_experimental
color grey70, chain A and 9AUC_NeuralPLexer
color white, chain A and 9AUC_experimental
color NeuralPLexer, 9AUC_NeuralPLexer and chain B
color experimental_color, 9AUC_experimental and chain B
create 9AUC_exp_ligand, 9AUC_experimental and chain B
create 9AUC_NeuralPLexer_ligand, 9AUC_NeuralPLexer and chain B
show cartoon, 9AUC_exp_ligand
show cartoon, 9AUC_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 9AUC_exp_ligand
set cartoon_oval_width, 0.7, 9AUC_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 9AUC_exp_ligand
set cartoon_loop_radius, 0.7, 9AUC_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7TYO_AB.pdb, 7TYO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7TYO.pdb, 7TYO_NeuralPLexer
align 7TYO_experimental, 7SK4_experimental 
align 7TYO_NeuralPLexer, 7TYO_experimental
color grey70, chain A and 7TYO_NeuralPLexer
color white, chain A and 7TYO_experimental
color NeuralPLexer, 7TYO_NeuralPLexer and chain B
color experimental_color, 7TYO_experimental and chain B
create 7TYO_exp_ligand, 7TYO_experimental and chain B
create 7TYO_NeuralPLexer_ligand, 7TYO_NeuralPLexer and chain B
show cartoon, 7TYO_exp_ligand
show cartoon, 7TYO_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7TYO_exp_ligand
set cartoon_oval_width, 0.7, 7TYO_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7TYO_exp_ligand
set cartoon_loop_radius, 0.7, 7TYO_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VL9_AB.pdb, 7VL9_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VL9.pdb, 7VL9_NeuralPLexer
align 7VL9_experimental, 7SK4_experimental 
align 7VL9_NeuralPLexer, 7VL9_experimental
color grey70, chain A and 7VL9_NeuralPLexer
color white, chain A and 7VL9_experimental
color NeuralPLexer, 7VL9_NeuralPLexer and chain B
color experimental_color, 7VL9_experimental and chain B
create 7VL9_exp_ligand, 7VL9_experimental and chain B
create 7VL9_NeuralPLexer_ligand, 7VL9_NeuralPLexer and chain B
show cartoon, 7VL9_exp_ligand
show cartoon, 7VL9_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VL9_exp_ligand
set cartoon_oval_width, 0.7, 7VL9_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VL9_exp_ligand
set cartoon_loop_radius, 0.7, 7VL9_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XA3_AB.pdb, 7XA3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7XA3.pdb, 7XA3_NeuralPLexer
align 7XA3_experimental, 7SK4_experimental 
align 7XA3_NeuralPLexer, 7XA3_experimental
color grey70, chain A and 7XA3_NeuralPLexer
color white, chain A and 7XA3_experimental
color NeuralPLexer, 7XA3_NeuralPLexer and chain B
color experimental_color, 7XA3_experimental and chain B
create 7XA3_exp_ligand, 7XA3_experimental and chain B
create 7XA3_NeuralPLexer_ligand, 7XA3_NeuralPLexer and chain B
show cartoon, 7XA3_exp_ligand
show cartoon, 7XA3_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7XA3_exp_ligand
set cartoon_oval_width, 0.7, 7XA3_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7XA3_exp_ligand
set cartoon_loop_radius, 0.7, 7XA3_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YKD_AB.pdb, 7YKD_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7YKD.pdb, 7YKD_NeuralPLexer
align 7YKD_experimental, 7SK4_experimental 
align 7YKD_NeuralPLexer, 7YKD_experimental
color grey70, chain A and 7YKD_NeuralPLexer
color white, chain A and 7YKD_experimental
color NeuralPLexer, 7YKD_NeuralPLexer and chain B
color experimental_color, 7YKD_experimental and chain B
create 7YKD_exp_ligand, 7YKD_experimental and chain B
create 7YKD_NeuralPLexer_ligand, 7YKD_NeuralPLexer and chain B
show cartoon, 7YKD_exp_ligand
show cartoon, 7YKD_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7YKD_exp_ligand
set cartoon_oval_width, 0.7, 7YKD_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7YKD_exp_ligand
set cartoon_loop_radius, 0.7, 7YKD_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JJP_AB.pdb, 8JJP_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8JJP.pdb, 8JJP_NeuralPLexer
align 8JJP_experimental, 7SK4_experimental 
align 8JJP_NeuralPLexer, 8JJP_experimental
color grey70, chain A and 8JJP_NeuralPLexer
color white, chain A and 8JJP_experimental
color NeuralPLexer, 8JJP_NeuralPLexer and chain B
color experimental_color, 8JJP_experimental and chain B
create 8JJP_exp_ligand, 8JJP_experimental and chain B
create 8JJP_NeuralPLexer_ligand, 8JJP_NeuralPLexer and chain B
show cartoon, 8JJP_exp_ligand
show cartoon, 8JJP_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8JJP_exp_ligand
set cartoon_oval_width, 0.7, 8JJP_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8JJP_exp_ligand
set cartoon_loop_radius, 0.7, 8JJP_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGM_AB.pdb, 8XGM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8XGM.pdb, 8XGM_NeuralPLexer
align 8XGM_experimental, 7SK4_experimental 
align 8XGM_NeuralPLexer, 8XGM_experimental
color grey70, chain A and 8XGM_NeuralPLexer
color white, chain A and 8XGM_experimental
color NeuralPLexer, 8XGM_NeuralPLexer and chain B
color experimental_color, 8XGM_experimental and chain B
create 8XGM_exp_ligand, 8XGM_experimental and chain B
create 8XGM_NeuralPLexer_ligand, 8XGM_NeuralPLexer and chain B
show cartoon, 8XGM_exp_ligand
show cartoon, 8XGM_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8XGM_exp_ligand
set cartoon_oval_width, 0.7, 8XGM_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8XGM_exp_ligand
set cartoon_loop_radius, 0.7, 8XGM_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IC0_AB.pdb, 8IC0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8IC0.pdb, 8IC0_NeuralPLexer
align 8IC0_experimental, 7SK4_experimental 
align 8IC0_NeuralPLexer, 8IC0_experimental
color grey70, chain A and 8IC0_NeuralPLexer
color white, chain A and 8IC0_experimental
color NeuralPLexer, 8IC0_NeuralPLexer and chain B
color experimental_color, 8IC0_experimental and chain B
create 8IC0_exp_ligand, 8IC0_experimental and chain B
create 8IC0_NeuralPLexer_ligand, 8IC0_NeuralPLexer and chain B
show cartoon, 8IC0_exp_ligand
show cartoon, 8IC0_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8IC0_exp_ligand
set cartoon_oval_width, 0.7, 8IC0_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8IC0_exp_ligand
set cartoon_loop_radius, 0.7, 8IC0_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HNK_AB.pdb, 8HNK_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8HNK.pdb, 8HNK_NeuralPLexer
align 8HNK_experimental, 7SK4_experimental 
align 8HNK_NeuralPLexer, 8HNK_experimental
color grey70, chain A and 8HNK_NeuralPLexer
color white, chain A and 8HNK_experimental
color NeuralPLexer, 8HNK_NeuralPLexer and chain B
color experimental_color, 8HNK_experimental and chain B
create 8HNK_exp_ligand, 8HNK_experimental and chain B
create 8HNK_NeuralPLexer_ligand, 8HNK_NeuralPLexer and chain B
show cartoon, 8HNK_exp_ligand
show cartoon, 8HNK_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8HNK_exp_ligand
set cartoon_oval_width, 0.7, 8HNK_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8HNK_exp_ligand
set cartoon_loop_radius, 0.7, 8HNK_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HCQ_AB.pdb, 8HCQ_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8HCQ.pdb, 8HCQ_NeuralPLexer
align 8HCQ_experimental, 7SK4_experimental 
align 8HCQ_NeuralPLexer, 8HCQ_experimental
color grey70, chain A and 8HCQ_NeuralPLexer
color white, chain A and 8HCQ_experimental
color NeuralPLexer, 8HCQ_NeuralPLexer and chain B
color experimental_color, 8HCQ_experimental and chain B
create 8HCQ_exp_ligand, 8HCQ_experimental and chain B
create 8HCQ_NeuralPLexer_ligand, 8HCQ_NeuralPLexer and chain B
show cartoon, 8HCQ_exp_ligand
show cartoon, 8HCQ_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8HCQ_exp_ligand
set cartoon_oval_width, 0.7, 8HCQ_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8HCQ_exp_ligand
set cartoon_loop_radius, 0.7, 8HCQ_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VFX_AB.pdb, 7VFX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VFX.pdb, 7VFX_NeuralPLexer
align 7VFX_experimental, 7SK4_experimental 
align 7VFX_NeuralPLexer, 7VFX_experimental
color grey70, chain A and 7VFX_NeuralPLexer
color white, chain A and 7VFX_experimental
color NeuralPLexer, 7VFX_NeuralPLexer and chain B
color experimental_color, 7VFX_experimental and chain B
create 7VFX_exp_ligand, 7VFX_experimental and chain B
create 7VFX_NeuralPLexer_ligand, 7VFX_NeuralPLexer and chain B
show cartoon, 7VFX_exp_ligand
show cartoon, 7VFX_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VFX_exp_ligand
set cartoon_oval_width, 0.7, 7VFX_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VFX_exp_ligand
set cartoon_loop_radius, 0.7, 7VFX_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T6T_AB.pdb, 7T6T_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7T6T.pdb, 7T6T_NeuralPLexer
align 7T6T_experimental, 7SK4_experimental 
align 7T6T_NeuralPLexer, 7T6T_experimental
color grey70, chain A and 7T6T_NeuralPLexer
color white, chain A and 7T6T_experimental
color NeuralPLexer, 7T6T_NeuralPLexer and chain B
color experimental_color, 7T6T_experimental and chain B
create 7T6T_exp_ligand, 7T6T_experimental and chain B
create 7T6T_NeuralPLexer_ligand, 7T6T_NeuralPLexer and chain B
show cartoon, 7T6T_exp_ligand
show cartoon, 7T6T_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7T6T_exp_ligand
set cartoon_oval_width, 0.7, 7T6T_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7T6T_exp_ligand
set cartoon_loop_radius, 0.7, 7T6T_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ3_AB.pdb, 7WQ3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7WQ3.pdb, 7WQ3_NeuralPLexer
align 7WQ3_experimental, 7SK4_experimental 
align 7WQ3_NeuralPLexer, 7WQ3_experimental
color grey70, chain A and 7WQ3_NeuralPLexer
color white, chain A and 7WQ3_experimental
color NeuralPLexer, 7WQ3_NeuralPLexer and chain B
color experimental_color, 7WQ3_experimental and chain B
create 7WQ3_exp_ligand, 7WQ3_experimental and chain B
create 7WQ3_NeuralPLexer_ligand, 7WQ3_NeuralPLexer and chain B
show cartoon, 7WQ3_exp_ligand
show cartoon, 7WQ3_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7WQ3_exp_ligand
set cartoon_oval_width, 0.7, 7WQ3_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7WQ3_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ3_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7WQ4.pdb, 7WQ4_NeuralPLexer
align 7WQ4_experimental, 7SK4_experimental 
align 7WQ4_NeuralPLexer, 7WQ4_experimental
color grey70, chain A and 7WQ4_NeuralPLexer
color white, chain A and 7WQ4_experimental
color NeuralPLexer, 7WQ4_NeuralPLexer and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_NeuralPLexer_ligand, 7WQ4_NeuralPLexer and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA7_AB.pdb, 8IA7_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8IA7.pdb, 8IA7_NeuralPLexer
align 8IA7_experimental, 7SK4_experimental 
align 8IA7_NeuralPLexer, 8IA7_experimental
color grey70, chain A and 8IA7_NeuralPLexer
color white, chain A and 8IA7_experimental
color NeuralPLexer, 8IA7_NeuralPLexer and chain B
color experimental_color, 8IA7_experimental and chain B
create 8IA7_exp_ligand, 8IA7_experimental and chain B
create 8IA7_NeuralPLexer_ligand, 8IA7_NeuralPLexer and chain B
show cartoon, 8IA7_exp_ligand
show cartoon, 8IA7_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8IA7_exp_ligand
set cartoon_oval_width, 0.7, 8IA7_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8IA7_exp_ligand
set cartoon_loop_radius, 0.7, 8IA7_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XOW_AB.pdb, 7XOW_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7XOW.pdb, 7XOW_NeuralPLexer
align 7XOW_experimental, 7SK4_experimental 
align 7XOW_NeuralPLexer, 7XOW_experimental
color grey70, chain A and 7XOW_NeuralPLexer
color white, chain A and 7XOW_experimental
color NeuralPLexer, 7XOW_NeuralPLexer and chain B
color experimental_color, 7XOW_experimental and chain B
create 7XOW_exp_ligand, 7XOW_experimental and chain B
create 7XOW_NeuralPLexer_ligand, 7XOW_NeuralPLexer and chain B
show cartoon, 7XOW_exp_ligand
show cartoon, 7XOW_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7XOW_exp_ligand
set cartoon_oval_width, 0.7, 7XOW_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7XOW_exp_ligand
set cartoon_loop_radius, 0.7, 7XOW_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RBT_AB.pdb, 7RBT_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7RBT.pdb, 7RBT_NeuralPLexer
align 7RBT_experimental, 7SK4_experimental 
align 7RBT_NeuralPLexer, 7RBT_experimental
color grey70, chain A and 7RBT_NeuralPLexer
color white, chain A and 7RBT_experimental
color NeuralPLexer, 7RBT_NeuralPLexer and chain B
color experimental_color, 7RBT_experimental and chain B
create 7RBT_exp_ligand, 7RBT_experimental and chain B
create 7RBT_NeuralPLexer_ligand, 7RBT_NeuralPLexer and chain B
show cartoon, 7RBT_exp_ligand
show cartoon, 7RBT_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7RBT_exp_ligand
set cartoon_oval_width, 0.7, 7RBT_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7RBT_exp_ligand
set cartoon_loop_radius, 0.7, 7RBT_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7FIN_AB.pdb, 7FIN_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7FIN.pdb, 7FIN_NeuralPLexer
align 7FIN_experimental, 7SK4_experimental 
align 7FIN_NeuralPLexer, 7FIN_experimental
color grey70, chain A and 7FIN_NeuralPLexer
color white, chain A and 7FIN_experimental
color NeuralPLexer, 7FIN_NeuralPLexer and chain B
color experimental_color, 7FIN_experimental and chain B
create 7FIN_exp_ligand, 7FIN_experimental and chain B
create 7FIN_NeuralPLexer_ligand, 7FIN_NeuralPLexer and chain B
show cartoon, 7FIN_exp_ligand
show cartoon, 7FIN_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7FIN_exp_ligand
set cartoon_oval_width, 0.7, 7FIN_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7FIN_exp_ligand
set cartoon_loop_radius, 0.7, 7FIN_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8YW4_AB.pdb, 8YW4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8YW4.pdb, 8YW4_NeuralPLexer
align 8YW4_experimental, 7SK4_experimental 
align 8YW4_NeuralPLexer, 8YW4_experimental
color grey70, chain A and 8YW4_NeuralPLexer
color white, chain A and 8YW4_experimental
color NeuralPLexer, 8YW4_NeuralPLexer and chain B
color experimental_color, 8YW4_experimental and chain B
create 8YW4_exp_ligand, 8YW4_experimental and chain B
create 8YW4_NeuralPLexer_ligand, 8YW4_NeuralPLexer and chain B
show cartoon, 8YW4_exp_ligand
show cartoon, 8YW4_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8YW4_exp_ligand
set cartoon_oval_width, 0.7, 8YW4_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8YW4_exp_ligand
set cartoon_loop_radius, 0.7, 8YW4_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W3Z_AB.pdb, 7W3Z_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7W3Z.pdb, 7W3Z_NeuralPLexer
align 7W3Z_experimental, 7SK4_experimental 
align 7W3Z_NeuralPLexer, 7W3Z_experimental
color grey70, chain A and 7W3Z_NeuralPLexer
color white, chain A and 7W3Z_experimental
color NeuralPLexer, 7W3Z_NeuralPLexer and chain B
color experimental_color, 7W3Z_experimental and chain B
create 7W3Z_exp_ligand, 7W3Z_experimental and chain B
create 7W3Z_NeuralPLexer_ligand, 7W3Z_NeuralPLexer and chain B
show cartoon, 7W3Z_exp_ligand
show cartoon, 7W3Z_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7W3Z_exp_ligand
set cartoon_oval_width, 0.7, 7W3Z_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7W3Z_exp_ligand
set cartoon_loop_radius, 0.7, 7W3Z_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8XGS_AB.pdb, 8XGS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8XGS.pdb, 8XGS_NeuralPLexer
align 8XGS_experimental, 7SK4_experimental 
align 8XGS_NeuralPLexer, 8XGS_experimental
color grey70, chain A and 8XGS_NeuralPLexer
color white, chain A and 8XGS_experimental
color NeuralPLexer, 8XGS_NeuralPLexer and chain B
color experimental_color, 8XGS_experimental and chain B
create 8XGS_exp_ligand, 8XGS_experimental and chain B
create 8XGS_NeuralPLexer_ligand, 8XGS_NeuralPLexer and chain B
show cartoon, 8XGS_exp_ligand
show cartoon, 8XGS_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8XGS_exp_ligand
set cartoon_oval_width, 0.7, 8XGS_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8XGS_exp_ligand
set cartoon_loop_radius, 0.7, 8XGS_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WVY_AB.pdb, 8WVY_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8WVY.pdb, 8WVY_NeuralPLexer
align 8WVY_experimental, 7SK4_experimental 
align 8WVY_NeuralPLexer, 8WVY_experimental
color grey70, chain A and 8WVY_NeuralPLexer
color white, chain A and 8WVY_experimental
color NeuralPLexer, 8WVY_NeuralPLexer and chain B
color experimental_color, 8WVY_experimental and chain B
create 8WVY_exp_ligand, 8WVY_experimental and chain B
create 8WVY_NeuralPLexer_ligand, 8WVY_NeuralPLexer and chain B
show cartoon, 8WVY_exp_ligand
show cartoon, 8WVY_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8WVY_exp_ligand
set cartoon_oval_width, 0.7, 8WVY_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8WVY_exp_ligand
set cartoon_loop_radius, 0.7, 8WVY_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IOC_AB.pdb, 8IOC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8IOC.pdb, 8IOC_NeuralPLexer
align 8IOC_experimental, 7SK4_experimental 
align 8IOC_NeuralPLexer, 8IOC_experimental
color grey70, chain A and 8IOC_NeuralPLexer
color white, chain A and 8IOC_experimental
color NeuralPLexer, 8IOC_NeuralPLexer and chain B
color experimental_color, 8IOC_experimental and chain B
create 8IOC_exp_ligand, 8IOC_experimental and chain B
create 8IOC_NeuralPLexer_ligand, 8IOC_NeuralPLexer and chain B
show cartoon, 8IOC_exp_ligand
show cartoon, 8IOC_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8IOC_exp_ligand
set cartoon_oval_width, 0.7, 8IOC_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8IOC_exp_ligand
set cartoon_loop_radius, 0.7, 8IOC_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8INR_AB.pdb, 8INR_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8INR.pdb, 8INR_NeuralPLexer
align 8INR_experimental, 7SK4_experimental 
align 8INR_NeuralPLexer, 8INR_experimental
color grey70, chain A and 8INR_NeuralPLexer
color white, chain A and 8INR_experimental
color NeuralPLexer, 8INR_NeuralPLexer and chain B
color experimental_color, 8INR_experimental and chain B
create 8INR_exp_ligand, 8INR_experimental and chain B
create 8INR_NeuralPLexer_ligand, 8INR_NeuralPLexer and chain B
show cartoon, 8INR_exp_ligand
show cartoon, 8INR_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8INR_exp_ligand
set cartoon_oval_width, 0.7, 8INR_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8INR_exp_ligand
set cartoon_loop_radius, 0.7, 8INR_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WSS_AB.pdb, 8WSS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8WSS.pdb, 8WSS_NeuralPLexer
align 8WSS_experimental, 7SK4_experimental 
align 8WSS_NeuralPLexer, 8WSS_experimental
color grey70, chain A and 8WSS_NeuralPLexer
color white, chain A and 8WSS_experimental
color NeuralPLexer, 8WSS_NeuralPLexer and chain B
color experimental_color, 8WSS_experimental and chain B
create 8WSS_exp_ligand, 8WSS_experimental and chain B
create 8WSS_NeuralPLexer_ligand, 8WSS_NeuralPLexer and chain B
show cartoon, 8WSS_exp_ligand
show cartoon, 8WSS_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8WSS_exp_ligand
set cartoon_oval_width, 0.7, 8WSS_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8WSS_exp_ligand
set cartoon_loop_radius, 0.7, 8WSS_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WST_AB.pdb, 8WST_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8WST.pdb, 8WST_NeuralPLexer
align 8WST_experimental, 7SK4_experimental 
align 8WST_NeuralPLexer, 8WST_experimental
color grey70, chain A and 8WST_NeuralPLexer
color white, chain A and 8WST_experimental
color NeuralPLexer, 8WST_NeuralPLexer and chain B
color experimental_color, 8WST_experimental and chain B
create 8WST_exp_ligand, 8WST_experimental and chain B
create 8WST_NeuralPLexer_ligand, 8WST_NeuralPLexer and chain B
show cartoon, 8WST_exp_ligand
show cartoon, 8WST_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8WST_exp_ligand
set cartoon_oval_width, 0.7, 8WST_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8WST_exp_ligand
set cartoon_loop_radius, 0.7, 8WST_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGF_AB.pdb, 8JGF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8JGF.pdb, 8JGF_NeuralPLexer
align 8JGF_experimental, 7SK4_experimental 
align 8JGF_NeuralPLexer, 8JGF_experimental
color grey70, chain A and 8JGF_NeuralPLexer
color white, chain A and 8JGF_experimental
color NeuralPLexer, 8JGF_NeuralPLexer and chain B
color experimental_color, 8JGF_experimental and chain B
create 8JGF_exp_ligand, 8JGF_experimental and chain B
create 8JGF_NeuralPLexer_ligand, 8JGF_NeuralPLexer and chain B
show cartoon, 8JGF_exp_ligand
show cartoon, 8JGF_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8JGF_exp_ligand
set cartoon_oval_width, 0.7, 8JGF_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8JGF_exp_ligand
set cartoon_loop_radius, 0.7, 8JGF_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JGB_AB.pdb, 8JGB_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8JGB.pdb, 8JGB_NeuralPLexer
align 8JGB_experimental, 7SK4_experimental 
align 8JGB_NeuralPLexer, 8JGB_experimental
color grey70, chain A and 8JGB_NeuralPLexer
color white, chain A and 8JGB_experimental
color NeuralPLexer, 8JGB_NeuralPLexer and chain B
color experimental_color, 8JGB_experimental and chain B
create 8JGB_exp_ligand, 8JGB_experimental and chain B
create 8JGB_NeuralPLexer_ligand, 8JGB_NeuralPLexer and chain B
show cartoon, 8JGB_exp_ligand
show cartoon, 8JGB_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8JGB_exp_ligand
set cartoon_oval_width, 0.7, 8JGB_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8JGB_exp_ligand
set cartoon_loop_radius, 0.7, 8JGB_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7S8L_AB.pdb, 7S8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7S8L.pdb, 7S8L_NeuralPLexer
align 7S8L_experimental, 7SK4_experimental 
align 7S8L_NeuralPLexer, 7S8L_experimental
color grey70, chain A and 7S8L_NeuralPLexer
color white, chain A and 7S8L_experimental
color NeuralPLexer, 7S8L_NeuralPLexer and chain B
color experimental_color, 7S8L_experimental and chain B
create 7S8L_exp_ligand, 7S8L_experimental and chain B
create 7S8L_NeuralPLexer_ligand, 7S8L_NeuralPLexer and chain B
show cartoon, 7S8L_exp_ligand
show cartoon, 7S8L_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7S8L_exp_ligand
set cartoon_oval_width, 0.7, 7S8L_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7S8L_exp_ligand
set cartoon_loop_radius, 0.7, 7S8L_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VDM_AB.pdb, 7VDM_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VDM.pdb, 7VDM_NeuralPLexer
align 7VDM_experimental, 7SK4_experimental 
align 7VDM_NeuralPLexer, 7VDM_experimental
color grey70, chain A and 7VDM_NeuralPLexer
color white, chain A and 7VDM_experimental
color NeuralPLexer, 7VDM_NeuralPLexer and chain B
color experimental_color, 7VDM_experimental and chain B
create 7VDM_exp_ligand, 7VDM_experimental and chain B
create 7VDM_NeuralPLexer_ligand, 7VDM_NeuralPLexer and chain B
show cartoon, 7VDM_exp_ligand
show cartoon, 7VDM_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VDM_exp_ligand
set cartoon_oval_width, 0.7, 7VDM_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VDM_exp_ligand
set cartoon_loop_radius, 0.7, 7VDM_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VV0_AB.pdb, 7VV0_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VV0.pdb, 7VV0_NeuralPLexer
align 7VV0_experimental, 7SK4_experimental 
align 7VV0_NeuralPLexer, 7VV0_experimental
color grey70, chain A and 7VV0_NeuralPLexer
color white, chain A and 7VV0_experimental
color NeuralPLexer, 7VV0_NeuralPLexer and chain B
color experimental_color, 7VV0_experimental and chain B
create 7VV0_exp_ligand, 7VV0_experimental and chain B
create 7VV0_NeuralPLexer_ligand, 7VV0_NeuralPLexer and chain B
show cartoon, 7VV0_exp_ligand
show cartoon, 7VV0_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VV0_exp_ligand
set cartoon_oval_width, 0.7, 7VV0_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VV0_exp_ligand
set cartoon_loop_radius, 0.7, 7VV0_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IBV_AB.pdb, 8IBV_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8IBV.pdb, 8IBV_NeuralPLexer
align 8IBV_experimental, 7SK4_experimental 
align 8IBV_NeuralPLexer, 8IBV_experimental
color grey70, chain A and 8IBV_NeuralPLexer
color white, chain A and 8IBV_experimental
color NeuralPLexer, 8IBV_NeuralPLexer and chain B
color experimental_color, 8IBV_experimental and chain B
create 8IBV_exp_ligand, 8IBV_experimental and chain B
create 8IBV_NeuralPLexer_ligand, 8IBV_NeuralPLexer and chain B
show cartoon, 8IBV_exp_ligand
show cartoon, 8IBV_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8IBV_exp_ligand
set cartoon_oval_width, 0.7, 8IBV_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8IBV_exp_ligand
set cartoon_loop_radius, 0.7, 8IBV_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8U26_AB.pdb, 8U26_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8U26.pdb, 8U26_NeuralPLexer
align 8U26_experimental, 7SK4_experimental 
align 8U26_NeuralPLexer, 8U26_experimental
color grey70, chain A and 8U26_NeuralPLexer
color white, chain A and 8U26_experimental
color NeuralPLexer, 8U26_NeuralPLexer and chain B
color experimental_color, 8U26_experimental and chain B
create 8U26_exp_ligand, 8U26_experimental and chain B
create 8U26_NeuralPLexer_ligand, 8U26_NeuralPLexer and chain B
show cartoon, 8U26_exp_ligand
show cartoon, 8U26_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8U26_exp_ligand
set cartoon_oval_width, 0.7, 8U26_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8U26_exp_ligand
set cartoon_loop_radius, 0.7, 8U26_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XWO_AB.pdb, 7XWO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7XWO.pdb, 7XWO_NeuralPLexer
align 7XWO_experimental, 7SK4_experimental 
align 7XWO_NeuralPLexer, 7XWO_experimental
color grey70, chain A and 7XWO_NeuralPLexer
color white, chain A and 7XWO_experimental
color NeuralPLexer, 7XWO_NeuralPLexer and chain B
color experimental_color, 7XWO_experimental and chain B
create 7XWO_exp_ligand, 7XWO_experimental and chain B
create 7XWO_NeuralPLexer_ligand, 7XWO_NeuralPLexer and chain B
show cartoon, 7XWO_exp_ligand
show cartoon, 7XWO_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7XWO_exp_ligand
set cartoon_oval_width, 0.7, 7XWO_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7XWO_exp_ligand
set cartoon_loop_radius, 0.7, 7XWO_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JBF_AB.pdb, 8JBF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8JBF.pdb, 8JBF_NeuralPLexer
align 8JBF_experimental, 7SK4_experimental 
align 8JBF_NeuralPLexer, 8JBF_experimental
color grey70, chain A and 8JBF_NeuralPLexer
color white, chain A and 8JBF_experimental
color NeuralPLexer, 8JBF_NeuralPLexer and chain B
color experimental_color, 8JBF_experimental and chain B
create 8JBF_exp_ligand, 8JBF_experimental and chain B
create 8JBF_NeuralPLexer_ligand, 8JBF_NeuralPLexer and chain B
show cartoon, 8JBF_exp_ligand
show cartoon, 8JBF_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8JBF_exp_ligand
set cartoon_oval_width, 0.7, 8JBF_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8JBF_exp_ligand
set cartoon_loop_radius, 0.7, 8JBF_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8H0P_AB.pdb, 8H0P_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8H0P.pdb, 8H0P_NeuralPLexer
align 8H0P_experimental, 7SK4_experimental 
align 8H0P_NeuralPLexer, 8H0P_experimental
color grey70, chain A and 8H0P_NeuralPLexer
color white, chain A and 8H0P_experimental
color NeuralPLexer, 8H0P_NeuralPLexer and chain B
color experimental_color, 8H0P_experimental and chain B
create 8H0P_exp_ligand, 8H0P_experimental and chain B
create 8H0P_NeuralPLexer_ligand, 8H0P_NeuralPLexer and chain B
show cartoon, 8H0P_exp_ligand
show cartoon, 8H0P_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8H0P_exp_ligand
set cartoon_oval_width, 0.7, 8H0P_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8H0P_exp_ligand
set cartoon_loop_radius, 0.7, 8H0P_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W56_AB.pdb, 7W56_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7W56.pdb, 7W56_NeuralPLexer
align 7W56_experimental, 7SK4_experimental 
align 7W56_NeuralPLexer, 7W56_experimental
color grey70, chain A and 7W56_NeuralPLexer
color white, chain A and 7W56_experimental
color NeuralPLexer, 7W56_NeuralPLexer and chain B
color experimental_color, 7W56_experimental and chain B
create 7W56_exp_ligand, 7W56_experimental and chain B
create 7W56_NeuralPLexer_ligand, 7W56_NeuralPLexer and chain B
show cartoon, 7W56_exp_ligand
show cartoon, 7W56_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7W56_exp_ligand
set cartoon_oval_width, 0.7, 7W56_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7W56_exp_ligand
set cartoon_loop_radius, 0.7, 7W56_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W53_AB.pdb, 7W53_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7W53.pdb, 7W53_NeuralPLexer
align 7W53_experimental, 7SK4_experimental 
align 7W53_NeuralPLexer, 7W53_experimental
color grey70, chain A and 7W53_NeuralPLexer
color white, chain A and 7W53_experimental
color NeuralPLexer, 7W53_NeuralPLexer and chain B
color experimental_color, 7W53_experimental and chain B
create 7W53_exp_ligand, 7W53_experimental and chain B
create 7W53_NeuralPLexer_ligand, 7W53_NeuralPLexer and chain B
show cartoon, 7W53_exp_ligand
show cartoon, 7W53_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7W53_exp_ligand
set cartoon_oval_width, 0.7, 7W53_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7W53_exp_ligand
set cartoon_loop_radius, 0.7, 7W53_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W55_AB.pdb, 7W55_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7W55.pdb, 7W55_NeuralPLexer
align 7W55_experimental, 7SK4_experimental 
align 7W55_NeuralPLexer, 7W55_experimental
color grey70, chain A and 7W55_NeuralPLexer
color white, chain A and 7W55_experimental
color NeuralPLexer, 7W55_NeuralPLexer and chain B
color experimental_color, 7W55_experimental and chain B
create 7W55_exp_ligand, 7W55_experimental and chain B
create 7W55_NeuralPLexer_ligand, 7W55_NeuralPLexer and chain B
show cartoon, 7W55_exp_ligand
show cartoon, 7W55_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7W55_exp_ligand
set cartoon_oval_width, 0.7, 7W55_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7W55_exp_ligand
set cartoon_loop_radius, 0.7, 7W55_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7W57_AB.pdb, 7W57_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7W57.pdb, 7W57_NeuralPLexer
align 7W57_experimental, 7SK4_experimental 
align 7W57_NeuralPLexer, 7W57_experimental
color grey70, chain A and 7W57_NeuralPLexer
color white, chain A and 7W57_experimental
color NeuralPLexer, 7W57_NeuralPLexer and chain B
color experimental_color, 7W57_experimental and chain B
create 7W57_exp_ligand, 7W57_experimental and chain B
create 7W57_NeuralPLexer_ligand, 7W57_NeuralPLexer and chain B
show cartoon, 7W57_exp_ligand
show cartoon, 7W57_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7W57_exp_ligand
set cartoon_oval_width, 0.7, 7W57_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7W57_exp_ligand
set cartoon_loop_radius, 0.7, 7W57_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VGX_AB.pdb, 7VGX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VGX.pdb, 7VGX_NeuralPLexer
align 7VGX_experimental, 7SK4_experimental 
align 7VGX_NeuralPLexer, 7VGX_experimental
color grey70, chain A and 7VGX_NeuralPLexer
color white, chain A and 7VGX_experimental
color NeuralPLexer, 7VGX_NeuralPLexer and chain B
color experimental_color, 7VGX_experimental and chain B
create 7VGX_exp_ligand, 7VGX_experimental and chain B
create 7VGX_NeuralPLexer_ligand, 7VGX_NeuralPLexer and chain B
show cartoon, 7VGX_exp_ligand
show cartoon, 7VGX_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VGX_exp_ligand
set cartoon_oval_width, 0.7, 7VGX_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VGX_exp_ligand
set cartoon_loop_radius, 0.7, 7VGX_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YON_AB.pdb, 7YON_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7YON.pdb, 7YON_NeuralPLexer
align 7YON_experimental, 7SK4_experimental 
align 7YON_NeuralPLexer, 7YON_experimental
color grey70, chain A and 7YON_NeuralPLexer
color white, chain A and 7YON_experimental
color NeuralPLexer, 7YON_NeuralPLexer and chain B
color experimental_color, 7YON_experimental and chain B
create 7YON_exp_ligand, 7YON_experimental and chain B
create 7YON_NeuralPLexer_ligand, 7YON_NeuralPLexer and chain B
show cartoon, 7YON_exp_ligand
show cartoon, 7YON_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7YON_exp_ligand
set cartoon_oval_width, 0.7, 7YON_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7YON_exp_ligand
set cartoon_loop_radius, 0.7, 7YON_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7YOO_AB.pdb, 7YOO_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7YOO.pdb, 7YOO_NeuralPLexer
align 7YOO_experimental, 7SK4_experimental 
align 7YOO_NeuralPLexer, 7YOO_experimental
color grey70, chain A and 7YOO_NeuralPLexer
color white, chain A and 7YOO_experimental
color NeuralPLexer, 7YOO_NeuralPLexer and chain B
color experimental_color, 7YOO_experimental and chain B
create 7YOO_exp_ligand, 7YOO_experimental and chain B
create 7YOO_NeuralPLexer_ligand, 7YOO_NeuralPLexer and chain B
show cartoon, 7YOO_exp_ligand
show cartoon, 7YOO_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7YOO_exp_ligand
set cartoon_oval_width, 0.7, 7YOO_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7YOO_exp_ligand
set cartoon_loop_radius, 0.7, 7YOO_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7X9C_AB.pdb, 7X9C_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7X9C.pdb, 7X9C_NeuralPLexer
align 7X9C_experimental, 7SK4_experimental 
align 7X9C_NeuralPLexer, 7X9C_experimental
color grey70, chain A and 7X9C_NeuralPLexer
color white, chain A and 7X9C_experimental
color NeuralPLexer, 7X9C_NeuralPLexer and chain B
color experimental_color, 7X9C_experimental and chain B
create 7X9C_exp_ligand, 7X9C_experimental and chain B
create 7X9C_NeuralPLexer_ligand, 7X9C_NeuralPLexer and chain B
show cartoon, 7X9C_exp_ligand
show cartoon, 7X9C_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7X9C_exp_ligand
set cartoon_oval_width, 0.7, 7X9C_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7X9C_exp_ligand
set cartoon_loop_radius, 0.7, 7X9C_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8F7W.pdb, 8F7W_NeuralPLexer
align 8F7W_experimental, 7SK4_experimental 
align 8F7W_NeuralPLexer, 8F7W_experimental
color grey70, chain A and 8F7W_NeuralPLexer
color white, chain A and 8F7W_experimental
color NeuralPLexer, 8F7W_NeuralPLexer and chain B
color experimental_color, 8F7W_experimental and chain B
create 8F7W_exp_ligand, 8F7W_experimental and chain B
create 8F7W_NeuralPLexer_ligand, 8F7W_NeuralPLexer and chain B
show cartoon, 8F7W_exp_ligand
show cartoon, 8F7W_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8F7W_exp_ligand
set cartoon_oval_width, 0.7, 8F7W_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8F7W_exp_ligand
set cartoon_loop_radius, 0.7, 8F7W_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8K9K_AB.pdb, 8K9K_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8K9K.pdb, 8K9K_NeuralPLexer
align 8K9K_experimental, 7SK4_experimental 
align 8K9K_NeuralPLexer, 8K9K_experimental
color grey70, chain A and 8K9K_NeuralPLexer
color white, chain A and 8K9K_experimental
color NeuralPLexer, 8K9K_NeuralPLexer and chain B
color experimental_color, 8K9K_experimental and chain B
create 8K9K_exp_ligand, 8K9K_experimental and chain B
create 8K9K_NeuralPLexer_ligand, 8K9K_NeuralPLexer and chain B
show cartoon, 8K9K_exp_ligand
show cartoon, 8K9K_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8K9K_exp_ligand
set cartoon_oval_width, 0.7, 8K9K_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8K9K_exp_ligand
set cartoon_loop_radius, 0.7, 8K9K_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7Q_AB.pdb, 8F7Q_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8F7Q.pdb, 8F7Q_NeuralPLexer
align 8F7Q_experimental, 7SK4_experimental 
align 8F7Q_NeuralPLexer, 8F7Q_experimental
color grey70, chain A and 8F7Q_NeuralPLexer
color white, chain A and 8F7Q_experimental
color NeuralPLexer, 8F7Q_NeuralPLexer and chain B
color experimental_color, 8F7Q_experimental and chain B
create 8F7Q_exp_ligand, 8F7Q_experimental and chain B
create 8F7Q_NeuralPLexer_ligand, 8F7Q_NeuralPLexer and chain B
show cartoon, 8F7Q_exp_ligand
show cartoon, 8F7Q_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8F7Q_exp_ligand
set cartoon_oval_width, 0.7, 8F7Q_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8F7Q_exp_ligand
set cartoon_loop_radius, 0.7, 8F7Q_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7R_AB.pdb, 8F7R_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8F7R.pdb, 8F7R_NeuralPLexer
align 8F7R_experimental, 7SK4_experimental 
align 8F7R_NeuralPLexer, 8F7R_experimental
color grey70, chain A and 8F7R_NeuralPLexer
color white, chain A and 8F7R_experimental
color NeuralPLexer, 8F7R_NeuralPLexer and chain B
color experimental_color, 8F7R_experimental and chain B
create 8F7R_exp_ligand, 8F7R_experimental and chain B
create 8F7R_NeuralPLexer_ligand, 8F7R_NeuralPLexer and chain B
show cartoon, 8F7R_exp_ligand
show cartoon, 8F7R_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8F7R_exp_ligand
set cartoon_oval_width, 0.7, 8F7R_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8F7R_exp_ligand
set cartoon_loop_radius, 0.7, 8F7R_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7X_AB.pdb, 8F7X_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8F7X.pdb, 8F7X_NeuralPLexer
align 8F7X_experimental, 7SK4_experimental 
align 8F7X_NeuralPLexer, 8F7X_experimental
color grey70, chain A and 8F7X_NeuralPLexer
color white, chain A and 8F7X_experimental
color NeuralPLexer, 8F7X_NeuralPLexer and chain B
color experimental_color, 8F7X_experimental and chain B
create 8F7X_exp_ligand, 8F7X_experimental and chain B
create 8F7X_NeuralPLexer_ligand, 8F7X_NeuralPLexer and chain B
show cartoon, 8F7X_exp_ligand
show cartoon, 8F7X_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8F7X_exp_ligand
set cartoon_oval_width, 0.7, 8F7X_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8F7X_exp_ligand
set cartoon_loop_radius, 0.7, 8F7X_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7RYC_AB.pdb, 7RYC_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7RYC.pdb, 7RYC_NeuralPLexer
align 7RYC_experimental, 7SK4_experimental 
align 7RYC_NeuralPLexer, 7RYC_experimental
color grey70, chain A and 7RYC_NeuralPLexer
color white, chain A and 7RYC_experimental
color NeuralPLexer, 7RYC_NeuralPLexer and chain B
color experimental_color, 7RYC_experimental and chain B
create 7RYC_exp_ligand, 7RYC_experimental and chain B
create 7RYC_NeuralPLexer_ligand, 7RYC_NeuralPLexer and chain B
show cartoon, 7RYC_exp_ligand
show cartoon, 7RYC_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7RYC_exp_ligand
set cartoon_oval_width, 0.7, 7RYC_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7RYC_exp_ligand
set cartoon_loop_radius, 0.7, 7RYC_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8ZPT_AB.pdb, 8ZPT_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8ZPT.pdb, 8ZPT_NeuralPLexer
align 8ZPT_experimental, 7SK4_experimental 
align 8ZPT_NeuralPLexer, 8ZPT_experimental
color grey70, chain A and 8ZPT_NeuralPLexer
color white, chain A and 8ZPT_experimental
color NeuralPLexer, 8ZPT_NeuralPLexer and chain B
color experimental_color, 8ZPT_experimental and chain B
create 8ZPT_exp_ligand, 8ZPT_experimental and chain B
create 8ZPT_NeuralPLexer_ligand, 8ZPT_NeuralPLexer and chain B
show cartoon, 8ZPT_exp_ligand
show cartoon, 8ZPT_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8ZPT_exp_ligand
set cartoon_oval_width, 0.7, 8ZPT_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8ZPT_exp_ligand
set cartoon_loop_radius, 0.7, 8ZPT_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8WZ2_AB.pdb, 8WZ2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8WZ2.pdb, 8WZ2_NeuralPLexer
align 8WZ2_experimental, 7SK4_experimental 
align 8WZ2_NeuralPLexer, 8WZ2_experimental
color grey70, chain A and 8WZ2_NeuralPLexer
color white, chain A and 8WZ2_experimental
color NeuralPLexer, 8WZ2_NeuralPLexer and chain B
color experimental_color, 8WZ2_experimental and chain B
create 8WZ2_exp_ligand, 8WZ2_experimental and chain B
create 8WZ2_NeuralPLexer_ligand, 8WZ2_NeuralPLexer and chain B
show cartoon, 8WZ2_exp_ligand
show cartoon, 8WZ2_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8WZ2_exp_ligand
set cartoon_oval_width, 0.7, 8WZ2_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8WZ2_exp_ligand
set cartoon_loop_radius, 0.7, 8WZ2_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8ZH8_AB.pdb, 8ZH8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8ZH8.pdb, 8ZH8_NeuralPLexer
align 8ZH8_experimental, 7SK4_experimental 
align 8ZH8_NeuralPLexer, 8ZH8_experimental
color grey70, chain A and 8ZH8_NeuralPLexer
color white, chain A and 8ZH8_experimental
color NeuralPLexer, 8ZH8_NeuralPLexer and chain B
color experimental_color, 8ZH8_experimental and chain B
create 8ZH8_exp_ligand, 8ZH8_experimental and chain B
create 8ZH8_NeuralPLexer_ligand, 8ZH8_NeuralPLexer and chain B
show cartoon, 8ZH8_exp_ligand
show cartoon, 8ZH8_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8ZH8_exp_ligand
set cartoon_oval_width, 0.7, 8ZH8_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8ZH8_exp_ligand
set cartoon_loop_radius, 0.7, 8ZH8_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T10_AB.pdb, 7T10_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7T10.pdb, 7T10_NeuralPLexer
align 7T10_experimental, 7SK4_experimental 
align 7T10_NeuralPLexer, 7T10_experimental
color grey70, chain A and 7T10_NeuralPLexer
color white, chain A and 7T10_experimental
color NeuralPLexer, 7T10_NeuralPLexer and chain B
color experimental_color, 7T10_experimental and chain B
create 7T10_exp_ligand, 7T10_experimental and chain B
create 7T10_NeuralPLexer_ligand, 7T10_NeuralPLexer and chain B
show cartoon, 7T10_exp_ligand
show cartoon, 7T10_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7T10_exp_ligand
set cartoon_oval_width, 0.7, 7T10_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7T10_exp_ligand
set cartoon_loop_radius, 0.7, 7T10_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7T11_AB.pdb, 7T11_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7T11.pdb, 7T11_NeuralPLexer
align 7T11_experimental, 7SK4_experimental 
align 7T11_NeuralPLexer, 7T11_experimental
color grey70, chain A and 7T11_NeuralPLexer
color white, chain A and 7T11_experimental
color NeuralPLexer, 7T11_NeuralPLexer and chain B
color experimental_color, 7T11_experimental and chain B
create 7T11_exp_ligand, 7T11_experimental and chain B
create 7T11_NeuralPLexer_ligand, 7T11_NeuralPLexer and chain B
show cartoon, 7T11_exp_ligand
show cartoon, 7T11_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7T11_exp_ligand
set cartoon_oval_width, 0.7, 7T11_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7T11_exp_ligand
set cartoon_loop_radius, 0.7, 7T11_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XMS_AB.pdb, 7XMS_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7XMS.pdb, 7XMS_NeuralPLexer
align 7XMS_experimental, 7SK4_experimental 
align 7XMS_NeuralPLexer, 7XMS_experimental
color grey70, chain A and 7XMS_NeuralPLexer
color white, chain A and 7XMS_experimental
color NeuralPLexer, 7XMS_NeuralPLexer and chain B
color experimental_color, 7XMS_experimental and chain B
create 7XMS_exp_ligand, 7XMS_experimental and chain B
create 7XMS_NeuralPLexer_ligand, 7XMS_NeuralPLexer and chain B
show cartoon, 7XMS_exp_ligand
show cartoon, 7XMS_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7XMS_exp_ligand
set cartoon_oval_width, 0.7, 7XMS_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7XMS_exp_ligand
set cartoon_loop_radius, 0.7, 7XMS_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8L_AB.pdb, 8X8L_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8X8L.pdb, 8X8L_NeuralPLexer
align 8X8L_experimental, 7SK4_experimental 
align 8X8L_NeuralPLexer, 8X8L_experimental
color grey70, chain A and 8X8L_NeuralPLexer
color white, chain A and 8X8L_experimental
color NeuralPLexer, 8X8L_NeuralPLexer and chain B
color experimental_color, 8X8L_experimental and chain B
create 8X8L_exp_ligand, 8X8L_experimental and chain B
create 8X8L_NeuralPLexer_ligand, 8X8L_NeuralPLexer and chain B
show cartoon, 8X8L_exp_ligand
show cartoon, 8X8L_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8X8L_exp_ligand
set cartoon_oval_width, 0.7, 8X8L_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8X8L_exp_ligand
set cartoon_loop_radius, 0.7, 8X8L_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8X8N_AB.pdb, 8X8N_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/8X8N.pdb, 8X8N_NeuralPLexer
align 8X8N_experimental, 7SK4_experimental 
align 8X8N_NeuralPLexer, 8X8N_experimental
color grey70, chain A and 8X8N_NeuralPLexer
color white, chain A and 8X8N_experimental
color NeuralPLexer, 8X8N_NeuralPLexer and chain B
color experimental_color, 8X8N_experimental and chain B
create 8X8N_exp_ligand, 8X8N_experimental and chain B
create 8X8N_NeuralPLexer_ligand, 8X8N_NeuralPLexer and chain B
show cartoon, 8X8N_exp_ligand
show cartoon, 8X8N_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 8X8N_exp_ligand
set cartoon_oval_width, 0.7, 8X8N_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 8X8N_exp_ligand
set cartoon_loop_radius, 0.7, 8X8N_NeuralPLexer_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7VQX_AB.pdb, 7VQX_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/NeuralPLexer/7VQX.pdb, 7VQX_NeuralPLexer
align 7VQX_experimental, 7SK4_experimental 
align 7VQX_NeuralPLexer, 7VQX_experimental
color grey70, chain A and 7VQX_NeuralPLexer
color white, chain A and 7VQX_experimental
color NeuralPLexer, 7VQX_NeuralPLexer and chain B
color experimental_color, 7VQX_experimental and chain B
create 7VQX_exp_ligand, 7VQX_experimental and chain B
create 7VQX_NeuralPLexer_ligand, 7VQX_NeuralPLexer and chain B
show cartoon, 7VQX_exp_ligand
show cartoon, 7VQX_NeuralPLexer_ligand
set cartoon_oval_width, 0.7, 7VQX_exp_ligand
set cartoon_oval_width, 0.7, 7VQX_NeuralPLexer_ligand
set cartoon_loop_radius, 0.7, 7VQX_exp_ligand
set cartoon_loop_radius, 0.7, 7VQX_NeuralPLexer_ligand



set grid_mode, 1
set grid_slot, 1, 7SK4_experimental
set grid_slot, 1, 7SK4_exp_ligand
set grid_slot, 1, 7SK4_NeuralPLexer
set grid_slot, 1, 7SK4_NeuralPLexer_ligand
set grid_slot, 2, 8GY7_experimental
set grid_slot, 2, 8GY7_exp_ligand
set grid_slot, 2, 8GY7_NeuralPLexer
set grid_slot, 2, 8GY7_NeuralPLexer_ligand
set grid_slot, 3, 7EIB_experimental
set grid_slot, 3, 7EIB_exp_ligand
set grid_slot, 3, 7EIB_NeuralPLexer
set grid_slot, 3, 7EIB_NeuralPLexer_ligand
set grid_slot, 4, 7F6I_experimental
set grid_slot, 4, 7F6I_exp_ligand
set grid_slot, 4, 7F6I_NeuralPLexer
set grid_slot, 4, 7F6I_NeuralPLexer_ligand
set grid_slot, 5, 8IA8_experimental
set grid_slot, 5, 8IA8_exp_ligand
set grid_slot, 5, 8IA8_NeuralPLexer
set grid_slot, 5, 8IA8_NeuralPLexer_ligand
set grid_slot, 6, 8I95_experimental
set grid_slot, 6, 8I95_exp_ligand
set grid_slot, 6, 8I95_NeuralPLexer
set grid_slot, 6, 8I95_NeuralPLexer_ligand
set grid_slot, 7, 8HK2_experimental
set grid_slot, 7, 8HK2_exp_ligand
set grid_slot, 7, 8HK2_NeuralPLexer
set grid_slot, 7, 8HK2_NeuralPLexer_ligand
set grid_slot, 8, 8F0K_experimental
set grid_slot, 8, 8F0K_exp_ligand
set grid_slot, 8, 8F0K_NeuralPLexer
set grid_slot, 8, 8F0K_NeuralPLexer_ligand
set grid_slot, 9, 9AUC_experimental
set grid_slot, 9, 9AUC_exp_ligand
set grid_slot, 9, 9AUC_NeuralPLexer
set grid_slot, 9, 9AUC_NeuralPLexer_ligand
set grid_slot, 10, 7TYO_experimental
set grid_slot, 10, 7TYO_exp_ligand
set grid_slot, 10, 7TYO_NeuralPLexer
set grid_slot, 10, 7TYO_NeuralPLexer_ligand
set grid_slot, 11, 7VL9_experimental
set grid_slot, 11, 7VL9_exp_ligand
set grid_slot, 11, 7VL9_NeuralPLexer
set grid_slot, 11, 7VL9_NeuralPLexer_ligand
set grid_slot, 12, 7XA3_experimental
set grid_slot, 12, 7XA3_exp_ligand
set grid_slot, 12, 7XA3_NeuralPLexer
set grid_slot, 12, 7XA3_NeuralPLexer_ligand
set grid_slot, 13, 7YKD_experimental
set grid_slot, 13, 7YKD_exp_ligand
set grid_slot, 13, 7YKD_NeuralPLexer
set grid_slot, 13, 7YKD_NeuralPLexer_ligand
set grid_slot, 14, 8JJP_experimental
set grid_slot, 14, 8JJP_exp_ligand
set grid_slot, 14, 8JJP_NeuralPLexer
set grid_slot, 14, 8JJP_NeuralPLexer_ligand
set grid_slot, 15, 8XGM_experimental
set grid_slot, 15, 8XGM_exp_ligand
set grid_slot, 15, 8XGM_NeuralPLexer
set grid_slot, 15, 8XGM_NeuralPLexer_ligand
set grid_slot, 16, 8IC0_experimental
set grid_slot, 16, 8IC0_exp_ligand
set grid_slot, 16, 8IC0_NeuralPLexer
set grid_slot, 16, 8IC0_NeuralPLexer_ligand
set grid_slot, 17, 8HNK_experimental
set grid_slot, 17, 8HNK_exp_ligand
set grid_slot, 17, 8HNK_NeuralPLexer
set grid_slot, 17, 8HNK_NeuralPLexer_ligand
set grid_slot, 18, 8HCQ_experimental
set grid_slot, 18, 8HCQ_exp_ligand
set grid_slot, 18, 8HCQ_NeuralPLexer
set grid_slot, 18, 8HCQ_NeuralPLexer_ligand
set grid_slot, 19, 7VFX_experimental
set grid_slot, 19, 7VFX_exp_ligand
set grid_slot, 19, 7VFX_NeuralPLexer
set grid_slot, 19, 7VFX_NeuralPLexer_ligand
set grid_slot, 20, 7T6T_experimental
set grid_slot, 20, 7T6T_exp_ligand
set grid_slot, 20, 7T6T_NeuralPLexer
set grid_slot, 20, 7T6T_NeuralPLexer_ligand
set grid_slot, 21, 7WQ3_experimental
set grid_slot, 21, 7WQ3_exp_ligand
set grid_slot, 21, 7WQ3_NeuralPLexer
set grid_slot, 21, 7WQ3_NeuralPLexer_ligand
set grid_slot, 22, 7WQ4_experimental
set grid_slot, 22, 7WQ4_exp_ligand
set grid_slot, 22, 7WQ4_NeuralPLexer
set grid_slot, 22, 7WQ4_NeuralPLexer_ligand
set grid_slot, 23, 8IA7_experimental
set grid_slot, 23, 8IA7_exp_ligand
set grid_slot, 23, 8IA7_NeuralPLexer
set grid_slot, 23, 8IA7_NeuralPLexer_ligand
set grid_slot, 24, 7XOW_experimental
set grid_slot, 24, 7XOW_exp_ligand
set grid_slot, 24, 7XOW_NeuralPLexer
set grid_slot, 24, 7XOW_NeuralPLexer_ligand
set grid_slot, 25, 7RBT_experimental
set grid_slot, 25, 7RBT_exp_ligand
set grid_slot, 25, 7RBT_NeuralPLexer
set grid_slot, 25, 7RBT_NeuralPLexer_ligand
set grid_slot, 26, 7FIN_experimental
set grid_slot, 26, 7FIN_exp_ligand
set grid_slot, 26, 7FIN_NeuralPLexer
set grid_slot, 26, 7FIN_NeuralPLexer_ligand
set grid_slot, 27, 8YW4_experimental
set grid_slot, 27, 8YW4_exp_ligand
set grid_slot, 27, 8YW4_NeuralPLexer
set grid_slot, 27, 8YW4_NeuralPLexer_ligand
set grid_slot, 28, 7W3Z_experimental
set grid_slot, 28, 7W3Z_exp_ligand
set grid_slot, 28, 7W3Z_NeuralPLexer
set grid_slot, 28, 7W3Z_NeuralPLexer_ligand
set grid_slot, 29, 8XGS_experimental
set grid_slot, 29, 8XGS_exp_ligand
set grid_slot, 29, 8XGS_NeuralPLexer
set grid_slot, 29, 8XGS_NeuralPLexer_ligand
set grid_slot, 30, 8WVY_experimental
set grid_slot, 30, 8WVY_exp_ligand
set grid_slot, 30, 8WVY_NeuralPLexer
set grid_slot, 30, 8WVY_NeuralPLexer_ligand
set grid_slot, 31, 8IOC_experimental
set grid_slot, 31, 8IOC_exp_ligand
set grid_slot, 31, 8IOC_NeuralPLexer
set grid_slot, 31, 8IOC_NeuralPLexer_ligand
set grid_slot, 32, 8INR_experimental
set grid_slot, 32, 8INR_exp_ligand
set grid_slot, 32, 8INR_NeuralPLexer
set grid_slot, 32, 8INR_NeuralPLexer_ligand
set grid_slot, 33, 8WSS_experimental
set grid_slot, 33, 8WSS_exp_ligand
set grid_slot, 33, 8WSS_NeuralPLexer
set grid_slot, 33, 8WSS_NeuralPLexer_ligand
set grid_slot, 34, 8WST_experimental
set grid_slot, 34, 8WST_exp_ligand
set grid_slot, 34, 8WST_NeuralPLexer
set grid_slot, 34, 8WST_NeuralPLexer_ligand
set grid_slot, 35, 8JGF_experimental
set grid_slot, 35, 8JGF_exp_ligand
set grid_slot, 35, 8JGF_NeuralPLexer
set grid_slot, 35, 8JGF_NeuralPLexer_ligand
set grid_slot, 36, 8JGB_experimental
set grid_slot, 36, 8JGB_exp_ligand
set grid_slot, 36, 8JGB_NeuralPLexer
set grid_slot, 36, 8JGB_NeuralPLexer_ligand
set grid_slot, 37, 7S8L_experimental
set grid_slot, 37, 7S8L_exp_ligand
set grid_slot, 37, 7S8L_NeuralPLexer
set grid_slot, 37, 7S8L_NeuralPLexer_ligand
set grid_slot, 38, 7VDM_experimental
set grid_slot, 38, 7VDM_exp_ligand
set grid_slot, 38, 7VDM_NeuralPLexer
set grid_slot, 38, 7VDM_NeuralPLexer_ligand
set grid_slot, 39, 7VV0_experimental
set grid_slot, 39, 7VV0_exp_ligand
set grid_slot, 39, 7VV0_NeuralPLexer
set grid_slot, 39, 7VV0_NeuralPLexer_ligand
set grid_slot, 40, 8IBV_experimental
set grid_slot, 40, 8IBV_exp_ligand
set grid_slot, 40, 8IBV_NeuralPLexer
set grid_slot, 40, 8IBV_NeuralPLexer_ligand
set grid_slot, 41, 8U26_experimental
set grid_slot, 41, 8U26_exp_ligand
set grid_slot, 41, 8U26_NeuralPLexer
set grid_slot, 41, 8U26_NeuralPLexer_ligand
set grid_slot, 42, 7XWO_experimental
set grid_slot, 42, 7XWO_exp_ligand
set grid_slot, 42, 7XWO_NeuralPLexer
set grid_slot, 42, 7XWO_NeuralPLexer_ligand
set grid_slot, 43, 8JBF_experimental
set grid_slot, 43, 8JBF_exp_ligand
set grid_slot, 43, 8JBF_NeuralPLexer
set grid_slot, 43, 8JBF_NeuralPLexer_ligand
set grid_slot, 44, 8H0P_experimental
set grid_slot, 44, 8H0P_exp_ligand
set grid_slot, 44, 8H0P_NeuralPLexer
set grid_slot, 44, 8H0P_NeuralPLexer_ligand
set grid_slot, 45, 7W56_experimental
set grid_slot, 45, 7W56_exp_ligand
set grid_slot, 45, 7W56_NeuralPLexer
set grid_slot, 45, 7W56_NeuralPLexer_ligand
set grid_slot, 46, 7W53_experimental
set grid_slot, 46, 7W53_exp_ligand
set grid_slot, 46, 7W53_NeuralPLexer
set grid_slot, 46, 7W53_NeuralPLexer_ligand
set grid_slot, 47, 7W55_experimental
set grid_slot, 47, 7W55_exp_ligand
set grid_slot, 47, 7W55_NeuralPLexer
set grid_slot, 47, 7W55_NeuralPLexer_ligand
set grid_slot, 48, 7W57_experimental
set grid_slot, 48, 7W57_exp_ligand
set grid_slot, 48, 7W57_NeuralPLexer
set grid_slot, 48, 7W57_NeuralPLexer_ligand
set grid_slot, 49, 7VGX_experimental
set grid_slot, 49, 7VGX_exp_ligand
set grid_slot, 49, 7VGX_NeuralPLexer
set grid_slot, 49, 7VGX_NeuralPLexer_ligand
set grid_slot, 50, 7YON_experimental
set grid_slot, 50, 7YON_exp_ligand
set grid_slot, 50, 7YON_NeuralPLexer
set grid_slot, 50, 7YON_NeuralPLexer_ligand
set grid_slot, 51, 7YOO_experimental
set grid_slot, 51, 7YOO_exp_ligand
set grid_slot, 51, 7YOO_NeuralPLexer
set grid_slot, 51, 7YOO_NeuralPLexer_ligand
set grid_slot, 52, 7X9C_experimental
set grid_slot, 52, 7X9C_exp_ligand
set grid_slot, 52, 7X9C_NeuralPLexer
set grid_slot, 52, 7X9C_NeuralPLexer_ligand
set grid_slot, 53, 8F7W_experimental
set grid_slot, 53, 8F7W_exp_ligand
set grid_slot, 53, 8F7W_NeuralPLexer
set grid_slot, 53, 8F7W_NeuralPLexer_ligand
set grid_slot, 54, 8K9K_experimental
set grid_slot, 54, 8K9K_exp_ligand
set grid_slot, 54, 8K9K_NeuralPLexer
set grid_slot, 54, 8K9K_NeuralPLexer_ligand
set grid_slot, 55, 8F7Q_experimental
set grid_slot, 55, 8F7Q_exp_ligand
set grid_slot, 55, 8F7Q_NeuralPLexer
set grid_slot, 55, 8F7Q_NeuralPLexer_ligand
set grid_slot, 56, 8F7R_experimental
set grid_slot, 56, 8F7R_exp_ligand
set grid_slot, 56, 8F7R_NeuralPLexer
set grid_slot, 56, 8F7R_NeuralPLexer_ligand
set grid_slot, 57, 8F7X_experimental
set grid_slot, 57, 8F7X_exp_ligand
set grid_slot, 57, 8F7X_NeuralPLexer
set grid_slot, 57, 8F7X_NeuralPLexer_ligand
set grid_slot, 58, 7RYC_experimental
set grid_slot, 58, 7RYC_exp_ligand
set grid_slot, 58, 7RYC_NeuralPLexer
set grid_slot, 58, 7RYC_NeuralPLexer_ligand
set grid_slot, 59, 8ZPT_experimental
set grid_slot, 59, 8ZPT_exp_ligand
set grid_slot, 59, 8ZPT_NeuralPLexer
set grid_slot, 59, 8ZPT_NeuralPLexer_ligand
set grid_slot, 60, 8WZ2_experimental
set grid_slot, 60, 8WZ2_exp_ligand
set grid_slot, 60, 8WZ2_NeuralPLexer
set grid_slot, 60, 8WZ2_NeuralPLexer_ligand
set grid_slot, 61, 8ZH8_experimental
set grid_slot, 61, 8ZH8_exp_ligand
set grid_slot, 61, 8ZH8_NeuralPLexer
set grid_slot, 61, 8ZH8_NeuralPLexer_ligand
set grid_slot, 62, 7T10_experimental
set grid_slot, 62, 7T10_exp_ligand
set grid_slot, 62, 7T10_NeuralPLexer
set grid_slot, 62, 7T10_NeuralPLexer_ligand
set grid_slot, 63, 7T11_experimental
set grid_slot, 63, 7T11_exp_ligand
set grid_slot, 63, 7T11_NeuralPLexer
set grid_slot, 63, 7T11_NeuralPLexer_ligand
set grid_slot, 64, 7XMS_experimental
set grid_slot, 64, 7XMS_exp_ligand
set grid_slot, 64, 7XMS_NeuralPLexer
set grid_slot, 64, 7XMS_NeuralPLexer_ligand
set grid_slot, 65, 8X8L_experimental
set grid_slot, 65, 8X8L_exp_ligand
set grid_slot, 65, 8X8L_NeuralPLexer
set grid_slot, 65, 8X8L_NeuralPLexer_ligand
set grid_slot, 66, 8X8N_experimental
set grid_slot, 66, 8X8N_exp_ligand
set grid_slot, 66, 8X8N_NeuralPLexer
set grid_slot, 66, 8X8N_NeuralPLexer_ligand
set grid_slot, 67, 7VQX_experimental
set grid_slot, 67, 7VQX_exp_ligand
set grid_slot, 67, 7VQX_NeuralPLexer
set grid_slot, 67, 7VQX_NeuralPLexer_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
