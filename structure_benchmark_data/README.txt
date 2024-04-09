# on 1apr2024 we noticed this
Could not be created: [('7W40_ligand', 'FQWAVXHFL'), ('7XK8_ligand', 'FRVDEEFQSPFASQSRGYFLFRPRNX'), ('8F7R_ligand', 'YPWFX'), ('7XW9_ligand', 'QHPX'), ('7W3Z_ligand', 'PRGNHWAVGHLMX')]
# It seems like in all the above pdbs where the X is in the end of the sequence, 
#    it means the C-terminus amidation so we can remove the X in those cases. 
#    For 7W40, it seems like the X is beta alanine, so I guess we could try replacing the X with normal alanine

# update the known_structures_benchmark .csv file. the 'ligand_pdb_seq'
'7W40_ligand', 'FQWAVXHFL' -> FQWAVAHFL
'7XK8_ligand', 'FRVDEEFQSPFASQSRGYFLFRPRNX' -> FRVDEEFQSPFASQSRGYFLFRPRN
'8F7R_ligand', 'YPWFX' -> YPWF
'7W3Z_ligand', 'PRGNHWAVGHLMX' -> PRGNHWAVGHLM
! important:
'7XW9_ligand', 'QHPX' -> QHP, but there is a structure with that exact ligand already. Remove it

# also updates the fastas