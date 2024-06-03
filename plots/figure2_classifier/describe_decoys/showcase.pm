reinitialize
# LOAD
load ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/glr_human___1136.pdb, complex

# COLORS
# background color white
bg_color white
# color receptor
color white
# ligand orange
set_color custom_orange, [1.000, 0.647, 0.000]
color custom_orange, chain C

# RENDER SETTINGS
@/Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/ray.pm

# RAY COMPLEX
ray 1200,1200
# save img
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/complex.png


# BINDING POCKET
# ### cut below here and paste into script ###
# set_view (\
#      0.164590821,    0.040686730,   -0.985516787,\
#     -0.497419298,    0.866219938,   -0.047312848,\
#      0.851750672,    0.498008430,    0.162811175,\
#      0.000000000,    0.000000000, -142.239929199,\
#      4.070068359,   -6.255594254,   -4.915115356,\
#     53.445980072,  231.033813477,   20.000000000 )
# ### cut above here and paste into script ###

# color receptor grey80
color grey80, complex and chain B
set_color custom_blue, [0.043, 0.239, 0.569]
# color binding pocket, from sticks_for_grns.py
#5x44 308, R308
show spheres, complex and chain B and resi 308
color custom_blue, complex and chain B and resi 308
#3x40 239, Y239
show spheres, complex and chain B and resi 239
color custom_blue, complex and chain B and resi 239
#7x41 389, S389
show spheres, complex and chain B and resi 389
color custom_blue, complex and chain B and resi 389
#3x36 235, I235
show spheres, complex and chain B and resi 235
color custom_blue, complex and chain B and resi 235
#7x42 390, S390
show spheres, complex and chain B and resi 390
color custom_blue, complex and chain B and resi 390
#7x35 383, F383
show spheres, complex and chain B and resi 383
color custom_blue, complex and chain B and resi 383
#1x36 142, Q142
show spheres, complex and chain B and resi 142
color custom_blue, complex and chain B and resi 142
#6x54 368, V368
show spheres, complex and chain B and resi 368
color custom_blue, complex and chain B and resi 368
#7x38 386, L386
show spheres, complex and chain B and resi 386
color custom_blue, complex and chain B and resi 386
#1x32 138, Y138
show spheres, complex and chain B and resi 138
color custom_blue, complex and chain B and resi 138
#5x47 311, V311
show spheres, complex and chain B and resi 311
color custom_blue, complex and chain B and resi 311
#45x51 295, W295
show spheres, complex and chain B and resi 295
color custom_blue, complex and chain B and resi 295
# save binding pocket
# give cartoon opacity
# set cartoon_transparency, 0.2
# hide spheres
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/binding_pocket.png


# END # 
hide spheres
# remove cartoon opacity
set cartoon_transparency, 0

# RAY LIGAND
# hide receptor
hide cartoon, complex and chain B
# save img
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/ligand.png


# RAY ALL LIGAND COLORS
# go through the color scheme of decoys
# (0.6, 0.13725490196078433, 0.10588235294117647, 1.0) #99231b
# (0.6676662821991541, 0.29565551710880433, 0.27043444828911956, 1.0) #aa4b44
# (0.7380392156862745, 0.46039215686274515, 0.4415686274509804, 1.0) #bc7570
# (0.8057054978854287, 0.6187927720107651, 0.6061207227989235, 1.0) #cd9d9a
# (0.8760784313725489, 0.783529411764706, 0.7772549019607843, 1.0) #dfc7c6
# (0.7647058823529411, 0.803921568627451, 0.8698039215686274, 1.0) #c3cddd
# (0.5807766243752402, 0.6599769319492503, 0.793033448673587, 1.0) #94a8ca
# (0.403921568627451, 0.5215686274509804, 0.7192156862745098, 1.0) #6785b7
# (0.21999231064975, 0.37762399077277975, 0.6424452133794694, 1.0) #3860a3
# (0.043137254901960784, 0.23921568627450981, 0.5686274509803921, 1.0) #0b3d91

# 1
set_color red1, [0.6, 0.13725490196078433, 0.10588235294117647]
color red1
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/1.png

# 2
set_color red2, [0.6676662821991541, 0.29565551710880433, 0.27043444828911956]
color red2
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/2.png

# 3
set_color red3, [0.7380392156862745, 0.46039215686274515, 0.4415686274509804]
color red3
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/3.png

# 4
set_color red4, [0.8057054978854287, 0.6187927720107651, 0.6061207227989235]
color red4
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/4.png

# 5
set_color red5, [0.8760784313725489, 0.783529411764706, 0.7772549019607843]
color red5
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/5.png

# 6
set_color red6, [0.7647058823529411, 0.803921568627451, 0.8698039215686274]
color red6
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/6.png

# 7
set_color red7, [0.5807766243752402, 0.6599769319492503, 0.793033448673587]
color red7
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/7.png

# 8
set_color red8, [0.403921568627451, 0.5215686274509804, 0.7192156862745098]
color red8
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/8.png

# 9
set_color red9, [0.21999231064975, 0.37762399077277975, 0.6424452133794694]
color red9
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/9.png

# 10
set_color red10, [0.043137254901960784, 0.23921568627450981, 0.5686274509803921]
color red10
ray 1200,1200
png ~/Documents/Github/GPRC_peptide_benchmarking/plots/figure2_classifier/describe_decoys/10.png

