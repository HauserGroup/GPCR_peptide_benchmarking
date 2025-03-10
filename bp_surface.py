# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# bp_surface.py - Binding pocket surface generator for Pymol (updated for Python 3)
# -------------------------------------------------------------------------------

# Original script Copyright (C) 2008 by Lightnir - lightnir@gmail.com
# Updated for Python 3 compatibility

"""
select ligand, glp1r and chain C
select pocket, byres(ligand around 4)
run /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/bp_surface.py
"""
from pymol import cmd

def get_selections():
    selections = cmd.get_names("selections")
    return [item for item in selections if not item.startswith("_")] if selections else []

def clear_flags(r, d):
    cmd.flag('ignore', 'all', 'clear')
    if r:
        cmd.rebuild('all')
    if d:
        cmd.delete('bp_cutoff')
        cmd.delete('bp_surface')

def apply_binding_pocket_surface(ligand, pocket, cutoff=0, create_new=True):
    selections = get_selections()
    if ligand not in selections or pocket not in selections:
        print(f"ERROR: One or both selections ({ligand}, {pocket}) do not exist in PyMOL.")
        return
    
    cmd.origin(ligand)
    d = cmd.get_view()
    vector = [
        [
            d[0] * 0 + d[1] * 0 + d[2] * 1,
            d[3] * 0 + d[4] * 0 + d[5] * 1,
            d[6] * 0 + d[7] * 0 + d[8] * 1
        ]
    ]

    A, B, C = vector[0]
    D = -A * d[12] - B * d[13] - C * d[14]

    atoms = cmd.get_model(pocket)
    if not atoms or not atoms.atom:
        print(f"ERROR: No atoms found in selection {pocket}.")
        return
    
    clear_flags(0, 1)
    if 'bp_cutoff' in get_selections():
        cmd.delete('bp_cutoff')
    for at in atoms.atom:
        if (A * at.coord[0] + B * at.coord[1] + C * at.coord[2] + D - cutoff > 0):
            cmd.select('bp_cutoff', f'index {at.index}', merge=1)
    
    if 'bp_cutoff' in get_selections():
        if not create_new:
            cmd.flag('ignore', 'bp_cutoff', 'reset')
            cmd.delete('indicate')
            cmd.show('surface', pocket)
        else:
            clear_flags(0, 0)
            cmd.hide('surface', pocket)
            cmd.create('bp_surface', f'{pocket} and not bp_cutoff')
            cmd.show('surface', 'bp_surface')
        cmd.rebuild(pocket)

# Example usage:
apply_binding_pocket_surface('ligand',
                             'pocket',
                             cutoff=4,
                             create_new=True)