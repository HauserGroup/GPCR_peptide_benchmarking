"""find if a peptide / GPCR has any known post-translational modifications (PTMs)

for both gpcrs and peptides, use uniprot
"""

import requests
import pandas as pd
import pathlib
import time

import logging
import numpy as np
import pygtop


def get_PTM_for_uniprot_id(uniprot_id: str) -> str:
    """Get the PTM for a uniprot ID.

    # https://rest.uniprot.org/uniprotkb/P35372.json?fields=ft_chain%2Cft_carbohyd%2Cft_disulfid%2Cft_mod_res%2Cft_lipid
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json?fields=ft_chain%2Cft_carbohyd%2Cft_disulfid%2Cft_mod_res%2Cft_lipid"
    response = requests.get(url)
    data = response.json()
    # """
    # {'entryType': 'UniProtKB reviewed (Swiss-Prot)', 'primaryAccession': 'P35372', 'features': [{'type': 'Chain', 'location': {'start': {'value': 1, 'modifier': 'EXACT'}, 'end': {'value': 400, 'modifier': 'EXACT'}}, 'description': 'Mu-type opioid receptor', 'featureId': 'PRO_0000069972'}, {'type': 'Modified residue', 'location': {'start': {'value': 168, 'modifier': 'EXACT'}, 'end': {'value': 168, 'modifier': 'EXACT'}}, 'description': 'Phosphotyrosine', 'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'P33535'}]}, {'type': 'Modified residue', 'location': {'start': {'value': 365, 'modifier': 'EXACT'}, 'end': {'value': 365, 'modifier': 'EXACT'}}, 'description': 'Phosphoserine', 'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'P42866'}]}, {'type': 'Modified residue', 'location': {'start': {'value': 372, 'modifier': 'EXACT'}, 'end': {'value': 372, 'modifier': 'EXACT'}}, 'description': 'Phosphothreonine', 'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'P33535'}]}, {'type': 'Modified residue', 'location': {'start': {'value': 377, 'modifier': 'EXACT'}, 'end': {'value': 377, 'modifier': 'EXACT'}}, 'description': 'Phosphoserine', 'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'P33535'}]}, {'type': 'Modified residue', 'location': {'start': {'value': 396, 'modifier': 'EXACT'}, 'end': {'value': 396, 'modifier': 'EXACT'}}, 'description': 'Phosphothreonine', 'evidences': [{'evidenceCode': 'ECO:0000250', 'source': 'UniProtKB', 'id': 'P33535'}]}, {'type': 'Lipidation', 'location': {'start': {'value': 353, 'modifier': 'EXACT'}, 'end': {'value': 353, 'modifier': 'EXACT'}}, 'description': 'S-palmitoyl cysteine', 'evidences': [{'evidenceCode': 'ECO:0000255'}]}, {'type': 'Glycosylation', 'location': {'start': {'value': 9, 'modifier': 'EXACT'}, 'end': {'value': 9, 'modifier': 'EXACT'}}, 'description': 'N-linked (GlcNAc...) asparagine', 'evidences': [{'evidenceCode': 'ECO:0000255'}], 'featureId': ''}, {'type': 'Glycosylation', 'location': {'start': {'value': 12, 'modifier': 'EXACT'}, 'end': {'value': 12, 'modifier': 'EXACT'}}, 'description': 'N-linked (GlcNAc...) asparagine', 'evidences': [{'evidenceCode': 'ECO:0000255'}], 'featureId': ''}, {'type': 'Glycosylation', 'location': {'start': {'value': 33, 'modifier': 'EXACT'}, 'end': {'value': 33, 'modifier': 'EXACT'}}, 'description': 'N-linked (GlcNAc...) asparagine', 'evidences': [{'evidenceCode': 'ECO:0000255'}], 'featureId': ''}, {'type': 'Glycosylation', 'location': {'start': {'value': 40, 'modifier': 'EXACT'}, 'end': {'value': 40, 'modifier': 'EXACT'}}, 'description': 'N-linked (GlcNAc...) asparagine', 'evidences': [{'evidenceCode': 'ECO:0000255'}], 'featureId': ''}, {'type': 'Glycosylation', 'location': {'start': {'value': 48, 'modifier': 'EXACT'}, 'end': {'value': 48, 'modifier': 'EXACT'}}, 'description': 'N-linked (GlcNAc...) asparagine', 'evidences': [{'evidenceCode': 'ECO:0000255'}], 'featureId': ''}, {'type': 'Disulfide bond', 'location': {'start': {'value': 142, 'modifier': 'EXACT'}, 'end': {'value': 219, 'modifier': 'EXACT'}}, 'description': '', 'evidences': [{'evidenceCode': 'ECO:0000255', 'source': 'PROSITE-ProRule', 'id': 'PRU00521'}]}]}
    # """
    # parse PTMs
    PTMs = []
    # each feature is a PTM instance
    for feature in data["features"]:
        # {'type': 'Chain', 'location': {'start': {'value': 1, 'modifier': 'EXACT'}, 'end': {'value': 400, 'modifier': 'EXACT'}}, 'description': 'Mu-type opioid receptor', 'featureId': 'PRO_0000069972'}
        if feature["type"] == "Chain":
            continue
        else:
            PTMs.append(feature)
    return PTMs


def read_GtP_csv(csv_p: pathlib.Path) -> pd.DataFrame:
    """Read the GtP CSV file and return a dataframe.
    # skip the header row
    """
    df = pd.read_csv(
        csv_p,
        # comments
        comment="#",
        # skip first header row, that starts with "#"
        skiprows=1,
    )

    return df


def get_GtP_peptides_df():
    script_dir = pathlib.Path(__file__).parent
    gtp_peptides = script_dir / "GtP_peptides3.csv"
    return read_GtP_csv(gtp_peptides)


def get_accession_from_gtp(gtp_id: int, gtp_pep_df: pd.DataFrame) -> str:
    """

    returns nan if set to nan in df
            0 if not found
            accession if found (str)
    """
    # use the "UniProt id" column
    matches = gtp_pep_df[gtp_pep_df["Ligand id"] == gtp_id]["UniProt id"].values
    if len(matches) == 0:
        logging.warning(f"No accession found for {gtp_id}")
        return np.nan

    elif len(matches) > 1:
        logging.error(f"Multiple accessions found for {gtp_id}")
        return "|".join(matches)
    return matches[0]


def get_PTMs_for_all_gpcrs():
    script_dir = pathlib.Path(__file__).parent
    gpcr_list_human = script_dir.parent / "gpcr_list_human.csv"
    df = pd.read_csv(gpcr_list_human)
    sleep_time = 0.5

    # get unique gpcrs
    df = df.drop_duplicates(subset=["gpcr"])
    logging.info(f"Unique GPCRs: {len(df)}")
    out_p = script_dir / "gpcr_ptms.csv"
    if out_p.exists():
        out_df = pd.read_csv(out_p)
        logging.info("Output file already exists, loading...")
    else:
        out_df = pd.DataFrame(columns=["gpcr", "accession", "PTMs"])
        logging.info("Output file does not exist, creating new.")

    # get already processed gpcrs
    processed_gpcrs = out_df["gpcr"].values
    if len(processed_gpcrs) > 0:
        logging.info(f"Already processed GPCRs: {len(processed_gpcrs)}")

    # fill the dataframe via append
    for i, row in df.iterrows():
        gpcr = row["gpcr"]
        uniprot_id = row["accession"]
        if gpcr in processed_gpcrs:
            continue
        logging.info(f"Processing {gpcr}, {uniprot_id}")

        try:
            PTMs = get_PTM_for_uniprot_id(uniprot_id)
        except KeyError as E:
            PTMs = []
            logging.error(f"Error for {gpcr}, {uniprot_id}, Error: {E}")

        # append to output
        row_df = pd.DataFrame(
            [[gpcr, uniprot_id, PTMs]], columns=["gpcr", "accession", "PTMs"]
        )
        out_df = pd.concat([out_df, row_df], ignore_index=True)
        out_df.to_csv(out_p, index=False)

        time.sleep(sleep_time)


def get_PTMs_for_all_peptides():
    script_dir = pathlib.Path(__file__).parent
    out_p = script_dir / "peptide_ptms.csv"
    if out_p.exists():
        logging.info("Output file already exists, loading...")
        out_df = pd.read_csv(out_p)
    else:
        logging.info("Output file does not exist, creating new.")
        out_df = pd.DataFrame(columns=["peptide", "has_accession", "accession", "PTMs"])

    # load peptides
    decoy_df = pd.read_csv(
        script_dir.parent.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    decoy_df = decoy_df[decoy_df["Decoy Type"] == "Principal Agonist"]
    peptides = decoy_df["Decoy ID"].values
    logging.info(f"Unique peptides: {len(peptides)}")

    # these peptides are the guide to pharma IDs, get accession
    gtp_peptides = get_GtP_peptides_df()

    # check which peptides are not gtp peptides
    not_found = [p for p in peptides if p not in gtp_peptides["Ligand id"].values]
    logging.info(f"Peptides not found in GtP: {len(not_found)}")
    if len(not_found) > 0:
        logging.info("\n".join([str(p) for p in not_found]))
        logging.info("\nConsider removing these from the subanalysis.")

    # get already processed peptides
    processed_peptides = out_df["peptide"].values
    if len(processed_peptides) > 0:
        logging.info(f"Already processed peptides: {len(processed_peptides)}")

    # for each peptide
    for candidate in peptides:
        if candidate in processed_peptides:
            continue

        # get accession (UniProt ID)
        accession = get_accession_from_gtp(candidate, gtp_peptides)
        logging.info(f"Processing {candidate}, with accession {accession}")
        if pd.isna(accession):
            has_accession = False
            PTMs = []
        else:
            has_accession = True
            if "|" in accession:
                accessions = accession.split("|")
            else:
                accessions = [accession]

            for accession in accessions:
                try:
                    PTMs = get_PTM_for_uniprot_id(accession)
                    # break if PTMs are found
                    break
                except KeyError as E:
                    PTMs = []
                    logging.error(f"Error for {candidate}, {accession}, Error: {E}")

        # append to output
        row_df = pd.DataFrame(
            [[candidate, has_accession, accession, PTMs]],
            columns=["peptide", "has_accession", "accession", "PTMs"],
        )
        out_df = pd.concat([out_df, row_df], ignore_index=True)
        out_df.to_csv(out_p, index=False)


if __name__ == "__main__":
    # log gpcrs
    SCRIPT_DIR = pathlib.Path(__file__).parent
    logging.basicConfig(
        level=logging.INFO, filemode="w", filename=SCRIPT_DIR / "get_ptm.log"
    )
    logging.info("Start GPCR PTM collection.")
    get_PTMs_for_all_gpcrs()

    logging.info("Start peptide PTM collection.")
    get_PTMs_for_all_peptides()
