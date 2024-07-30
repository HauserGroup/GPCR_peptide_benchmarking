reinitialize
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___1272.pdb, glr_1272
set_color Dissimilar1, (205, 157, 154)
color grey80, glr_1272 and chain B
color Dissimilar1, glr_1272 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___1162.pdb, glr_1162
set_color Dissimilar3, (170, 75, 68)
color grey80, glr_1162 and chain B
color Dissimilar3, glr_1162 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___758.pdb, glr_758
set_color Dissimilar4, (153, 35, 27)
color grey80, glr_758 and chain B
color Dissimilar4, glr_758 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___2257.pdb, glr_2257
set_color Similar0, (195, 205, 221)
color grey80, glr_2257 and chain B
color Similar0, glr_2257 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___1140.pdb, glr_1140
set_color Similar4, (11, 61, 145)
color grey80, glr_1140 and chain B
color Similar4, glr_1140 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___754.pdb, glr_754
set_color Dissimilar0, (223, 199, 198)
color grey80, glr_754 and chain B
color Dissimilar0, glr_754 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___3542.pdb, glr_3542
set_color Similar3, (56, 96, 163)
color grey80, glr_3542 and chain B
color Similar3, glr_3542 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___1152.pdb, glr_1152
set_color Similar2, (103, 133, 183)
color grey80, glr_1152 and chain B
color Similar2, glr_1152 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___1136.pdb, glr_1136
set_color Principal Agonist, (249, 170, 67)
color grey80, glr_1136 and chain B
color Principal Agonist, glr_1136 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___3643.pdb, glr_3643
set_color Similar1, (148, 168, 202)
color grey80, glr_3643 and chain B
color Similar1, glr_3643 and chain C
load /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/models/glr_human___6067.pdb, glr_6067
set_color Dissimilar2, (188, 117, 112)
color grey80, glr_6067 and chain B
color Dissimilar2, glr_6067 and chain C
align glr_1272 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_1162 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_758 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_2257 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_1140 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_754 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_3542 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_1152 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_1136 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_3643 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
align glr_6067 and chain B and resi 50-350, glr_1136 and chain B and resi 50-350
hide cartoon, chain B and resi 440-700
@/Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/ray.pm
### cut below here and paste into script ###
    set_view (        0.846652448,    0.043910827,   -0.530334532,        -0.092061721,    0.993649125,   -0.064698182,        0.524124205,    0.103599437,    0.845313013,        0.000000000,   -8.000000000, -308.572143555,        1.567100525,   -6.109443665,   -5.748374939,    -179078.390625000, 179695.531250000,   20.000000000 )
    ### cut above here and paste into script ###
    
bg_color white
hide cartoon, chain B
set cartoon_transparency, 0.5, chain B
show cartoon, chain B
hide cartoon, glr_1272 and chain B
hide cartoon, glr_1162 and chain B
hide cartoon, glr_758 and chain B
hide cartoon, glr_2257 and chain B
hide cartoon, glr_1140 and chain B
hide cartoon, glr_754 and chain B
hide cartoon, glr_3542 and chain B
hide cartoon, glr_1152 and chain B
hide cartoon, glr_3643 and chain B
hide cartoon, glr_6067 and chain B
ray 800, 800
save /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/plots/figure2_classifier/show_10_decoys/show.png
