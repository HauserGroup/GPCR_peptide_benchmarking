"""Simple script to view the peptides"""

import pathlib


def get_unrelaxed(p: pathlib.Path):
    # read file
    all_files = p.glob("*.pdb")
    # only keep if starts with 'unrelaxed_'
    unrelaxed_files = [f for f in all_files if f.name.startswith("unrelaxed_")]
    return unrelaxed_files


def get_model_index(p: pathlib.Path):
    # /Users/kcd635/Documents/GitHub/GPRC_peptide_benchmarking/classifier_subanalysis/AFM_LIS_highlight/lgr4_human___5654/unrelaxed_model_5_multimer_v3_pred_0.pdb -> 5

    name = p.name
    after_model = name.split("model_")[1]
    model_index = after_model.split("_")[0]
    return int(model_index)


def set_view_focus_on_LRRR(file_p):
    s = """    
    ### cut below here and paste into script ###
    set_view (\
        0.426546276,    0.770357192,   -0.473923832,\
        0.857468903,   -0.511127412,   -0.059075937,\
        -0.287741214,   -0.381175786,   -0.878568947,\
        0.000000000,    4.000000000, -425.326263428,\
        9.173591614,    8.383514404,    6.905570984,\
    -25697.369140625, 26548.062500000,  -20.000000000 )
    ### cut above here and paste into script ###
    """
    with open(file_p, "a") as f:
        f.write("\n")
        f.write(s)
        f.write("\n")


def show_how_real_agonist_is_saved():
    # make a pymol script.
    script_dir = pathlib.Path(__file__).parent.absolute()
    out_p = script_dir / "real_agonist.pm"

    # real agonist: lgr4_human,,100.0,LNRRKKQVGTGLGGNCTGCIICSEENGCSTCQQRLFLFIRREGIRQYGKCLHDCPPGYFGIRGQEVNRCKKCGATCESCFSQDFCIRCKRQFYLYKGKCLPTCPPGTLAHQNTRECQGECELGPWGGWSPCTHNGKTCGSAWGLESRVREAGRAGHEEAATCQVLSESRKCPIQRPCPGERSPGQKKGRKDRRPRKDRKLDRRLDVRPRQPGLQP,MPGPLGLLCFLALGLLGSAGPSGAAPPLCAAPCSCDGDRRVDCSGKGLTAVPEGLSAFTQALDISMNNITQLPEDAFKNFPFLEELQLAGNDLSFIHPKALSGLKELKVLTLQNNQLKTVPSEAIRGLSALQSLRLDANHITSVPEDSFEGLVQLRHLWLDDNSLTEVPVHPLSNLPTLQALTLALNKISSIPDFAFTNLSSLVVLHLHNNKIRSLSQHCFDGLDNLETLDLNYNNLGEFPQAIKALPSLKELGFHSNSISVIPDGAFDGNPLLRTIHLYDNPLSFVGNSAFHNLSDLHSLVIRGASMVQQFPNLTGTVHLESLTLTGTKISSIPNNLCQEQKMLRTLDLSYNNIRDLPSFNGCHALEEISLQRNQIYQIKEGTFQGLISLRILDLSRNLIHEIHSRAFATLGPITNLDVSFNELTSFPTEGLNGLNQLKLVGNFKLKEALAAKDFVNLRSLSVPYAYQCCAFWGCDSYANLNTEDNSLQDHSVAQEKGTADAANVTSTLENEEHSQIIIHCTPSTGAFKPCEYLLGSWMIRLTVWFIFLVALFFNLLVILTTFASCTSLPSSKLFIGLISVSNLFMGIYTGILTFLDAVSWGRFAEFGIWWETGSGCKVAGFLAVFSSESAIFLLMLATVERSLSAKDIMKNGKSNHLKQFRVAALLAFLGATVAGCFPLFHRGEYSASPLCLPFPTGETPSLGFTVTLVLLNSLAFLLMAVIYTKLYCNLEKEDLSENSQSSMIKHVAWLIFTNCIFFCPVAFFSFAPLITAISISPEIMKSVTLIFFPLPACLNPVLYVFFNPKFKEDWKLLKRRVTKKSGSVSVSISSQGGCLEQDFYYDCGMYSHLQGNLTVCDCCESFLLTKPVSCKHLIKSHSCPALAVASCQRPEGYWSDCGTQSAHSDYADEEDSFVSDSSDQVQACGRACFYQSRGFPLVRYAYNLPRVKD,lgr4_human___3700,lgr4_human,3700,True,Principal Agonist
    # this agonist was ranked as nr 1 by LIS
    real_agonist = "lgr4_human___3700"
    real_agonist_d = script_dir / f"{real_agonist}"
    real_agonist_pdbs = get_unrelaxed(real_agonist_d)
    real_agonist_names = list()
    with open(out_p, "w") as out_f:
        out_f.write("reinitialize\n")
        for pdb in real_agonist_pdbs:
            model_index = get_model_index(pdb)
            peptide = pdb.parent.name.split("___")[1]
            short_name = f"{peptide}_{model_index}"
            out_f.write(f"load {pdb}, {short_name}\n")
            real_agonist_names.append(short_name)

    # what was the (falsely) best agonist of AF2?
    false_best = "lgr4_human___5654"
    false_best_d = script_dir / f"{false_best}"
    false_best_pdbs = get_unrelaxed(false_best_d)
    false_best_names = list()
    with open(out_p, "a") as out_f:
        for pdb in false_best_pdbs:
            model_index = get_model_index(pdb)
            peptide = pdb.parent.name.split("___")[1]
            short_name = f"{peptide}_{model_index}"
            out_f.write(f"load {pdb}, {short_name}\n")
            false_best_names.append(short_name)

    # align all to first real agonist
    reference_pdb = real_agonist_names[0]
    for pdb in real_agonist_names + false_best_names:
        with open(out_p, "a") as out_f:
            out_f.write(f"align {pdb}, {reference_pdb}\n")

    # only show the first real agonist receptor
    with open(out_p, "a") as out_f:
        out_f.write(f"hide cartoon, chain B\n")
        out_f.write(f"show cartoon, {reference_pdb} and chain B\n")

    # background color white
    with open(out_p, "a") as out_f:
        out_f.write(f"bg_color white\n")

    # color gpcr
    with open(out_p, "a") as out_f:
        out_f.write(f"color grey80, chain B\n")

    # for gpcr, hide resi 827 to end
    with open(out_p, "a") as out_f:
        out_f.write(f"hide cartoon, chain B and resi 827-\n")
    # custom colors
    with open(out_p, "a") as out_f:
        # #3860a3 = (56, 96, 163)
        out_f.write("set_color decoy, (56, 96, 163)\n")
        out_f.write("set_color real_agonist, (249, 170, 67)\n")

    # for each pdb, color peptides
    for pdb in real_agonist_names:
        with open(out_p, "a") as out_f:
            out_f.write(f"color real_agonist, {pdb} and chain C\n")
    for pdb in false_best_names:
        with open(out_p, "a") as out_f:
            out_f.write(f"color decoy, {pdb} and chain C\n")

    # set opacity of chain C
    # with open(out_p, "a") as out_f:
    #     out_f.write(f"set cartoon_transparency, 0.3, chain C\n")

    # set opacity of receptor
    with open(out_p, "a") as out_f:
        out_f.write(f"set cartoon_transparency, 0.1, chain B\n")

    # set view focus on LRRR
    set_view_focus_on_LRRR(out_p)


if __name__ == "__main__":
    show_how_real_agonist_is_saved()
