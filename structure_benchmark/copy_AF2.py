""" """

import os
import pathlib
import pandas as pd


def map_identifier_to_pdb_id(pdb_csv: pd.DataFrame) -> str:
    """Return dict that maps identifier to pdb_id

    Example:
    identifier = "ackr3_human___LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK
        where ackr3_human is the gpcr
        and LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK is the peptide sequence.
        this corresponds to 7SK4, as the row in the input_csv looks like this:
        pdb,receptor,uniprot_id,description,class,family,resolution,type,state,ligand_name,ligand_chain,ligand_sequence,ligand_pdb_seq,receptor_chain,receptor_uniprot_seq,receptor_pdb_seq,publication,publication_date
        7SK4,ackr3_human,P25106,Atypical chemokine receptor 3,Class A (Rhodopsin),Chemokine receptors,3.3,Electron microscopy,Active,Stromal cell-derived factor 1,B,LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK,LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK,A,MDLHLFDYSEPGNFSDISWPCNSSDCIVVDTVMCPNMPNKSVLLYTLSFIYIFIFVIGMIANSVVVWVNIQAKTTGYDTHCYILNLAIADLWVVLTIPVWVVSLVQHNQWPMGELTCKVTHLIFSINLFGSIFFLTCMSVDRYLSITYFTNTPSSRKKMVRRVVCILVWLLAFCVSLPDTYYLKTVTSASNNETYCRSFYPEHSIKEWLIGMELVSVVLGFAVPFSIIAVFYFLLARAISASSDQEKHSSRKIIFSYVVVFLVCWLPYHVAVLLDIFSILHYIPFTCRLEHALFTALHVTQCLSLVHCCVNPVLYSFINRNYRYELMKAFIFKYSAKTGLTKLIDASRVSETEYSALEQSTK,GAPDLHLFDYSEPGNFSDISWPCNSSDCIVVDTVMCPNMPNKSVLLYTLSFIYIFIFVIGMIANSVVVWVNIQAKTTGYDTHCYILNLAIADLWVVLTIPVWVVSLVQHNQWPMGELTCKVTHLIFSINLFGSIFFLTCMSVDRYLSITYFTNTPSSRKKMVRRVVCILVWLLAFCVSLPDTYYLKTVTSASNNETYCRSFYPEHSIKEWLIGMELVSVVLGFAVPFSIIAVFYFLLARAISASSDQEKHSSRKIIFSYVVVFLVCWLPYHVAVLLDIFSILHYIPFTCRLEHALFTALHVTQCLSLVHCCVNPVLYSFINRNYRYELMKAFIFKYSAKTGLTKLIDASRVSETEYSALEQSTKGRPLEVLFQGPHHHHHHHHHHDYKDDDDK,https://dx.doi.org/10.1126/SCIADV.ABN8063,2022-07-27
    """
    out_dict = {}
    for _, row in pdb_csv.iterrows():
        out_dict[row["receptor"] + "___" + row["ligand_pdb_seq"]] = row["pdb"]

    return out_dict


def run_main(
    download_dir: pathlib.Path, out_dir: pathlib.Path, input_csv_p: pathlib.Path
):
    """Copy 'raw' AF2 prediction files to the out_dir.
    The prediction with the highest iptm+ptm is saved as 'PDB_ID.pdb'

    Args:
        download_dir (pathlib.Path): directory containing the AF2 prediction files
        out_dir (pathlib.Path): directory to save the 'raw' AF2 prediction files
        input_csv_p (pathlib.Path): path to the csv file containing the benchmark data
            pdb,receptor,uniprot_id,description,class,family,resolution,type,state,ligand_name,ligand_chain,ligand_sequence,ligand_pdb_seq,receptor_chain,receptor_uniprot_seq,receptor_pdb_seq,publication,publication_date
            7SK4,ackr3_human,P25106,Atypical chemokine receptor 3,Class A (Rhodopsin),Chemokine receptors,3.3,Electron microscopy,Active,Stromal cell-derived factor 1,B,LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK,LRHQSLSYRCPCRFFESHVARANVKHLKILNTPNCALQIVARLKNNNRQVCIDPKLKWIQEYLEKALNK,A,MDLHLFDYSEPGNFSDISWPCNSSDCIVVDTVMCPNMPNKSVLLYTLSFIYIFIFVIGMIANSVVVWVNIQAKTTGYDTHCYILNLAIADLWVVLTIPVWVVSLVQHNQWPMGELTCKVTHLIFSINLFGSIFFLTCMSVDRYLSITYFTNTPSSRKKMVRRVVCILVWLLAFCVSLPDTYYLKTVTSASNNETYCRSFYPEHSIKEWLIGMELVSVVLGFAVPFSIIAVFYFLLARAISASSDQEKHSSRKIIFSYVVVFLVCWLPYHVAVLLDIFSILHYIPFTCRLEHALFTALHVTQCLSLVHCCVNPVLYSFINRNYRYELMKAFIFKYSAKTGLTKLIDASRVSETEYSALEQSTK,GAPDLHLFDYSEPGNFSDISWPCNSSDCIVVDTVMCPNMPNKSVLLYTLSFIYIFIFVIGMIANSVVVWVNIQAKTTGYDTHCYILNLAIADLWVVLTIPVWVVSLVQHNQWPMGELTCKVTHLIFSINLFGSIFFLTCMSVDRYLSITYFTNTPSSRKKMVRRVVCILVWLLAFCVSLPDTYYLKTVTSASNNETYCRSFYPEHSIKEWLIGMELVSVVLGFAVPFSIIAVFYFLLARAISASSDQEKHSSRKIIFSYVVVFLVCWLPYHVAVLLDIFSILHYIPFTCRLEHALFTALHVTQCLSLVHCCVNPVLYSFINRNYRYELMKAFIFKYSAKTGLTKLIDASRVSETEYSALEQSTKGRPLEVLFQGPHHHHHHHHHHDYKDDDDK,https://dx.doi.org/10.1126/SCIADV.ABN8063,2022-07-27

    """
    script_dir = pathlib.Path(__file__).parent
    # confirm download_dir exists
    if not download_dir.exists():
        raise FileNotFoundError(f"Could not find {download_dir}")
    print("\n\n\nCopying files from ", download_dir)
    out_dir.mkdir(exist_ok=True)
    pdb_csv = pd.read_csv(input_csv_p)
    identifier_to_pdb_id = map_identifier_to_pdb_id(pdb_csv)

    # go over each subdir in the download_dir, which is a AF2 prediction directory for 1 complex
    found_count = 0
    not_found_count = 0
    for subdir in download_dir.iterdir():
        if not subdir.is_dir():
            continue
        identifier = subdir.name
        pdb_id = identifier_to_pdb_id[identifier]
        # find the prediction with the highest iptm+ptm
        # in our pipeline this is the .pdb file with filename "{identifier}.pdb"
        pdb_p = subdir / f"{identifier}.pdb"
        if not pdb_p.exists():
            print(f"Could not find {pdb_id}\t\t{pdb_p}")
            not_found_count += 1
            continue
        print(f"\tFound {pdb_id}")
        out_p = out_dir / f"{pdb_id}.pdb"
        os.system(f"cp {pdb_p} {out_p}")
        found_count += 1
        # print(f"Copied {pdb_p} to {out_p}")
    print(f"Found {found_count} and not found {not_found_count}")


if __name__ == "__main__":
    SCRIPT_DIR = pathlib.Path(__file__).parent

    # AF2 default
    run_main(
        download_dir=pathlib.Path("~/Downloads/AF2_template_2022_04_01/").expanduser(),
        out_dir=SCRIPT_DIR / "AF2",
        input_csv_p=SCRIPT_DIR.parent
        / "structure_benchmark_data/3f_known_structures_benchmark_fixed_2022-04-01.csv",
    )
    # AF2 no template
    run_main(
        download_dir=pathlib.Path(
            "~/Downloads/AF2_no_template_2022_04_01/"
        ).expanduser(),
        out_dir=SCRIPT_DIR / "AF2_no_templates",
        input_csv_p=SCRIPT_DIR.parent
        / "structure_benchmark_data/3f_known_structures_benchmark_fixed_2022-04-01.csv",
    )
