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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8IA8_AB.pdb, 8IA8_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8IA8.pdb, 8IA8_RFAA
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8I95_AB.pdb, 8I95_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8I95.pdb, 8I95_RFAA
align 8I95_experimental, 8IA8_experimental 
align 8I95_RFAA, 8I95_experimental
color grey70, chain A and 8I95_RFAA
color white, chain A and 8I95_experimental
color RF-AA, 8I95_RFAA and chain B
color experimental_color, 8I95_experimental and chain B
create 8I95_exp_ligand, 8I95_experimental and chain B
create 8I95_RFAA_ligand, 8I95_RFAA and chain B
show cartoon, 8I95_exp_ligand
show cartoon, 8I95_RFAA_ligand
set cartoon_oval_width, 0.7, 8I95_exp_ligand
set cartoon_oval_width, 0.7, 8I95_RFAA_ligand
set cartoon_loop_radius, 0.7, 8I95_exp_ligand
set cartoon_loop_radius, 0.7, 8I95_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8HK2_AB.pdb, 8HK2_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8HK2.pdb, 8HK2_RFAA
align 8HK2_experimental, 8IA8_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7XA3_AB.pdb, 7XA3_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7XA3.pdb, 7XA3_RFAA
align 7XA3_experimental, 8IA8_experimental 
align 7XA3_RFAA, 7XA3_experimental
color grey70, chain A and 7XA3_RFAA
color white, chain A and 7XA3_experimental
color RF-AA, 7XA3_RFAA and chain B
color experimental_color, 7XA3_experimental and chain B
create 7XA3_exp_ligand, 7XA3_experimental and chain B
create 7XA3_RFAA_ligand, 7XA3_RFAA and chain B
show cartoon, 7XA3_exp_ligand
show cartoon, 7XA3_RFAA_ligand
set cartoon_oval_width, 0.7, 7XA3_exp_ligand
set cartoon_oval_width, 0.7, 7XA3_RFAA_ligand
set cartoon_loop_radius, 0.7, 7XA3_exp_ligand
set cartoon_loop_radius, 0.7, 7XA3_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/7WQ4_AB.pdb, 7WQ4_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7WQ4.pdb, 7WQ4_RFAA
align 7WQ4_experimental, 8IA8_experimental 
align 7WQ4_RFAA, 7WQ4_experimental
color grey70, chain A and 7WQ4_RFAA
color white, chain A and 7WQ4_experimental
color RF-AA, 7WQ4_RFAA and chain B
color experimental_color, 7WQ4_experimental and chain B
create 7WQ4_exp_ligand, 7WQ4_experimental and chain B
create 7WQ4_RFAA_ligand, 7WQ4_RFAA and chain B
show cartoon, 7WQ4_exp_ligand
show cartoon, 7WQ4_RFAA_ligand
set cartoon_oval_width, 0.7, 7WQ4_exp_ligand
set cartoon_oval_width, 0.7, 7WQ4_RFAA_ligand
set cartoon_loop_radius, 0.7, 7WQ4_exp_ligand
set cartoon_loop_radius, 0.7, 7WQ4_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8JBF_AB.pdb, 8JBF_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8JBF.pdb, 8JBF_RFAA
align 8JBF_experimental, 8IA8_experimental 
align 8JBF_RFAA, 8JBF_experimental
color grey70, chain A and 8JBF_RFAA
color white, chain A and 8JBF_experimental
color RF-AA, 8JBF_RFAA and chain B
color experimental_color, 8JBF_experimental and chain B
create 8JBF_exp_ligand, 8JBF_experimental and chain B
create 8JBF_RFAA_ligand, 8JBF_RFAA and chain B
show cartoon, 8JBF_exp_ligand
show cartoon, 8JBF_RFAA_ligand
set cartoon_oval_width, 0.7, 8JBF_exp_ligand
set cartoon_oval_width, 0.7, 8JBF_RFAA_ligand
set cartoon_loop_radius, 0.7, 8JBF_exp_ligand
set cartoon_loop_radius, 0.7, 8JBF_RFAA_ligand
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/cleaned_pdbs/8F7W_AB.pdb, 8F7W_experimental
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8F7W.pdb, 8F7W_RFAA
align 8F7W_experimental, 8IA8_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8F7Q.pdb, 8F7Q_RFAA
align 8F7Q_experimental, 8IA8_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/8F7X.pdb, 8F7X_RFAA
align 8F7X_experimental, 8IA8_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7T10.pdb, 7T10_RFAA
align 7T10_experimental, 8IA8_experimental 
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
load /Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark/RFAA/7T11.pdb, 7T11_RFAA
align 7T11_experimental, 8IA8_experimental 
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



set grid_mode, 1
set grid_slot, 1, 8IA8_experimental
set grid_slot, 1, 8IA8_exp_ligand
set grid_slot, 1, 8IA8_RFAA
set grid_slot, 1, 8IA8_RFAA_ligand
set grid_slot, 2, 8I95_experimental
set grid_slot, 2, 8I95_exp_ligand
set grid_slot, 2, 8I95_RFAA
set grid_slot, 2, 8I95_RFAA_ligand
set grid_slot, 3, 8HK2_experimental
set grid_slot, 3, 8HK2_exp_ligand
set grid_slot, 3, 8HK2_RFAA
set grid_slot, 3, 8HK2_RFAA_ligand
set grid_slot, 4, 7XA3_experimental
set grid_slot, 4, 7XA3_exp_ligand
set grid_slot, 4, 7XA3_RFAA
set grid_slot, 4, 7XA3_RFAA_ligand
set grid_slot, 5, 7WQ4_experimental
set grid_slot, 5, 7WQ4_exp_ligand
set grid_slot, 5, 7WQ4_RFAA
set grid_slot, 5, 7WQ4_RFAA_ligand
set grid_slot, 6, 8JBF_experimental
set grid_slot, 6, 8JBF_exp_ligand
set grid_slot, 6, 8JBF_RFAA
set grid_slot, 6, 8JBF_RFAA_ligand
set grid_slot, 7, 8F7W_experimental
set grid_slot, 7, 8F7W_exp_ligand
set grid_slot, 7, 8F7W_RFAA
set grid_slot, 7, 8F7W_RFAA_ligand
set grid_slot, 8, 8F7Q_experimental
set grid_slot, 8, 8F7Q_exp_ligand
set grid_slot, 8, 8F7Q_RFAA
set grid_slot, 8, 8F7Q_RFAA_ligand
set grid_slot, 9, 8F7X_experimental
set grid_slot, 9, 8F7X_exp_ligand
set grid_slot, 9, 8F7X_RFAA
set grid_slot, 9, 8F7X_RFAA_ligand
set grid_slot, 10, 7T10_experimental
set grid_slot, 10, 7T10_exp_ligand
set grid_slot, 10, 7T10_RFAA
set grid_slot, 10, 7T10_RFAA_ligand
set grid_slot, 11, 7T11_experimental
set grid_slot, 11, 7T11_exp_ligand
set grid_slot, 11, 7T11_RFAA
set grid_slot, 11, 7T11_RFAA_ligand
set cartoon_transparency, 0.25, chain A
hide (hydro)
hide everything, not polymer
set cartoon_transparency, 0, chain B
set cartoon_transparency, 0, chain B
set cartoon_loop_radius, 0.4
center
zoom
