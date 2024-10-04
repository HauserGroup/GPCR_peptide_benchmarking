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


set_color PrincipalAgonist, [0.976, 0.667, 0.263]
set_color Similar0, [0.765, 0.804, 0.867]
set_color Dissimilar0, [0.875, 0.780, 0.776]
set_color Similar1, [0.580, 0.659, 0.792]
set_color Dissimilar1, [0.804, 0.616, 0.604]
set_color Similar2, [0.404, 0.522, 0.718]
set_color Dissimilar2, [0.737, 0.459, 0.439]
set_color Similar3, [0.220, 0.376, 0.639]
set_color Dissimilar3, [0.667, 0.294, 0.267]
set_color Similar4, [0.043, 0.239, 0.569]
set_color Dissimilar4, [0.600, 0.137, 0.106]



load /Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/tournament_benchmark/one_to_ten/ackr1_one_to_ten/ackr1_one_to_ten.pdb, ackr1_tournament
color white, ackr1_tournament and chain B
color PrincipalAgonist, ackr1_tournament and chain C
color Similar0, ackr1_tournament and chain H
color Dissimilar0, ackr1_tournament and chain I
color Similar1, ackr1_tournament and chain D
color Dissimilar1, ackr1_tournament and chain J
color Similar2, ackr1_tournament and chain E
color Dissimilar2, ackr1_tournament and chain K
color Similar3, ackr1_tournament and chain F
color Dissimilar3, ackr1_tournament and chain L
color Similar4, ackr1_tournament and chain G
color Dissimilar4, ackr1_tournament and chain M



set cartoon_transparency, 0.25, chain B
hide (hydro)
hide everything, not polymer
hide everything, chain C
set cartoon_transparency, 0, chain C
set cartoon_transparency, 0, chain C
hide everything, chain D
set cartoon_transparency, 0, chain D
set cartoon_transparency, 0, chain D
hide everything, chain E
set cartoon_transparency, 0, chain E
set cartoon_transparency, 0, chain E
hide everything, chain F
set cartoon_transparency, 0, chain F
set cartoon_transparency, 0, chain F
hide everything, chain G
set cartoon_transparency, 0, chain G
set cartoon_transparency, 0, chain G
hide everything, chain H
set cartoon_transparency, 0, chain H
set cartoon_transparency, 0, chain H
hide everything, chain I
set cartoon_transparency, 0, chain I
set cartoon_transparency, 0, chain I
hide everything, chain J
set cartoon_transparency, 0, chain J
set cartoon_transparency, 0, chain J
hide everything, chain K
set cartoon_transparency, 0, chain K
set cartoon_transparency, 0, chain K
hide everything, chain L
set cartoon_transparency, 0, chain L
set cartoon_transparency, 0, chain L
hide everything, chain M
set cartoon_transparency, 0, chain M
set cartoon_transparency, 0, chain M
set cartoon_loop_radius, 0.4


create ackr1_tournament_C, ackr1_tournament and chain C
show cartoon, ackr1_tournament_C
set cartoon_oval_width, 0.7, ackr1_tournament_C
set cartoon_loop_radius, 0.7, ackr1_tournament_C
create ackr1_tournament_D, ackr1_tournament and chain D
show cartoon, ackr1_tournament_D
set cartoon_oval_width, 0.7, ackr1_tournament_D
set cartoon_loop_radius, 0.7, ackr1_tournament_D
create ackr1_tournament_E, ackr1_tournament and chain E
show cartoon, ackr1_tournament_E
set cartoon_oval_width, 0.7, ackr1_tournament_E
set cartoon_loop_radius, 0.7, ackr1_tournament_E
create ackr1_tournament_F, ackr1_tournament and chain F
show cartoon, ackr1_tournament_F
set cartoon_oval_width, 0.7, ackr1_tournament_F
set cartoon_loop_radius, 0.7, ackr1_tournament_F
create ackr1_tournament_G, ackr1_tournament and chain G
show cartoon, ackr1_tournament_G
set cartoon_oval_width, 0.7, ackr1_tournament_G
set cartoon_loop_radius, 0.7, ackr1_tournament_G
create ackr1_tournament_H, ackr1_tournament and chain H
show cartoon, ackr1_tournament_H
set cartoon_oval_width, 0.7, ackr1_tournament_H
set cartoon_loop_radius, 0.7, ackr1_tournament_H
create ackr1_tournament_I, ackr1_tournament and chain I
show cartoon, ackr1_tournament_I
set cartoon_oval_width, 0.7, ackr1_tournament_I
set cartoon_loop_radius, 0.7, ackr1_tournament_I
create ackr1_tournament_J, ackr1_tournament and chain J
show cartoon, ackr1_tournament_J
set cartoon_oval_width, 0.7, ackr1_tournament_J
set cartoon_loop_radius, 0.7, ackr1_tournament_J
create ackr1_tournament_K, ackr1_tournament and chain K
show cartoon, ackr1_tournament_K
set cartoon_oval_width, 0.7, ackr1_tournament_K
set cartoon_loop_radius, 0.7, ackr1_tournament_K
create ackr1_tournament_L, ackr1_tournament and chain L
show cartoon, ackr1_tournament_L
set cartoon_oval_width, 0.7, ackr1_tournament_L
set cartoon_loop_radius, 0.7, ackr1_tournament_L
create ackr1_tournament_M, ackr1_tournament and chain M
show cartoon, ackr1_tournament_M
set cartoon_oval_width, 0.7, ackr1_tournament_M
set cartoon_loop_radius, 0.7, ackr1_tournament_M
zoom
