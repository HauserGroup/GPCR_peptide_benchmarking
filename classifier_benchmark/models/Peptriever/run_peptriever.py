"""Try peptriever:
https://github.com/RoniGurvich/Peptriever

https://github.com/RoniGurvich/Peptriever/issues/18
"""

import pathlib
import torch
import requests
import os
import pandas as pd
from transformers import AutoModel, AutoTokenizer
from collections import OrderedDict


def get_tokenizer_and_model():
    tokenizer = AutoTokenizer.from_pretrained("ronig/protein_biencoder")
    model = AutoModel.from_pretrained("ronig/protein_biencoder", trust_remote_code=True)
    model.eval()
    return tokenizer, model


def get_distance(tokenizer, model, peptide_sequence, protein_sequence):
    encoded_peptide = tokenizer.encode_plus(peptide_sequence, return_tensors="pt")
    encoded_protein = tokenizer.encode_plus(protein_sequence, return_tensors="pt")

    with torch.no_grad():
        peptide_output = model.forward1(encoded_peptide)
        protein_output = model.forward2(encoded_protein)

    distance = torch.norm(peptide_output - protein_output, p=2)
    return distance


def load_input_df():
    """Load the classifier benchmark data and return the relevant columns"""
    script_dir = pathlib.Path(__file__).parent
    data_dir = script_dir.parent.parent.parent / "classifier_benchmark_data"
    df = data_dir / "output/6_interactions_with_decoys.csv"
    df = pd.read_csv(df)
    df = df[["Identifier", "GPCR Sequence", "Ligand Sequence"]]
    return df


def get_all_GPCR_names():
    base_url = "https://gpcrdb.org"
    url = f"{base_url}/services/receptorlist/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    gpcr_names = [x["entry_name"] for x in data]
    return gpcr_names


def get_chain_info_for_gpcr(gpcr_name):
    base_url = "https://gpcrdb.org"
    # /services/protein/{entry_name}/
    # Get a single protein instance by entry name
    # /services/residues/{entry_name}/
    # Get a list of residues of a protein
    url = f"{base_url}/services/residues/{gpcr_name}/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data


def parse_chain_info_data(data):
    """
    # raw data:
    [{'sequence_number': 1, 'amino_acid': 'M', 'protein_segment': 'N-term', 'display_generic_number': None}, {'sequence_number': 2, 'amino_acid': 'D', 'protein_segment': 'N-term', 'display_generic_number': None},


    # return
    (sequence, domains, lengths)
    """
    sequence = ""
    domain_lengths = OrderedDict()

    for d in data:
        sequence += d["amino_acid"]
        if d["protein_segment"] not in domain_lengths:
            domain_lengths[d["protein_segment"]] = 0
        domain_lengths[d["protein_segment"]] += 1

    return sequence, domain_lengths


def load_chain_info_df(chain_info_df_path, gpcr_names):
    if not os.path.exists(chain_info_df_path):
        # download chain info
        out_df = pd.DataFrame(columns=["GPCR", "Sequence", "Domains"])
        for name in gpcr_names:
            data = get_chain_info_for_gpcr(name)
            sequence, domain_lengths = parse_chain_info_data(data)
            print(name, domain_lengths)
            out_df = pd.concat(
                [
                    out_df,
                    pd.DataFrame(
                        {
                            "GPCR": [name],
                            "Sequence": [sequence],
                            "Domains": [domain_lengths],
                        }
                    ),
                ]
            )
        out_df.to_csv(chain_info_df_path, index=False)
    else:
        df = pd.read_csv(chain_info_df_path)
        return df


def trim_gpcr(chain_info_df, gpcr, gpcr_seq):
    """ """
    # find row info from df
    info = chain_info_df[chain_info_df["GPCR"] == gpcr]
    if len(info) != 1:
        raise ValueError("GPCR not found in chain info df")
    info = info.iloc[0]
    domains = info["Domains"]
    domains = eval(domains)

    # check sequence matches
    assert info["Sequence"] == gpcr_seq, "Sequence mismatch"

    # trim the sequence
    new_seq = gpcr_seq
    # remove N-terminal signal peptide
    if "N-term" in domains:
        n_term_len = domains["N-term"]
        new_seq = new_seq[n_term_len:]
    # remove C-terminal tail
    if "C-term" in domains:
        c_term_len = domains["C-term"]
        new_seq = new_seq[:-c_term_len]

    return new_seq


def filter_df_for_peptriever(df, chain_info_df):
    """Peptriever has certain limits (regarding sequence length)
    "We set the peptide and protein model input to 30 and 300"

    GPCRs are too long but can be shortened by:
        - trimming the N-terminal signal peptide
        - trimming the C-terminal tail

    Peptides won't be trimmed, just rejected or kept.

    chain_info_df_path: all GPCR chain info from GPCRdb
    """
    df = df.copy()
    print("Number of pairs before filtering for peptide length:", len(df))
    df["Ligand length"] = df["Ligand Sequence"].str.len()

    # remove peptides that are too long or short
    max_pep_len = 30
    df = df[(df["Ligand length"] <= max_pep_len)]
    print("Number of pairs after filtering for peptide length:", len(df))
    # trim the GPCR sequences
    df["GPCR"] = df["Identifier"].str.split("___").str[0]

    # remove GPCRs that are too long (even after trimming)
    max_prot_len = 300
    rows_to_drop = []
    for i, row in df.iterrows():
        gpcr = row["GPCR"]
        gpcr_sequence = row["GPCR Sequence"]
        gpcr_sequence = trim_gpcr(chain_info_df, gpcr, gpcr_sequence)
        if len(gpcr_sequence) > max_prot_len:
            rows_to_drop.append(i)
        # update gpcr sequence
        df.at[i, "GPCR Sequence"] = gpcr_sequence

    gpcrs_dropped = df.loc[rows_to_drop, "GPCR"].unique()
    print("GPCRs dropped:", gpcrs_dropped)
    df = df.drop(rows_to_drop)
    print("Number of pairs after filtering for protein length:", len(df))
    return df


def main():
    script_dir = pathlib.Path(__file__).parent
    tokenizer, model = get_tokenizer_and_model()
    df = load_input_df()
    df["GPCR"] = df["Identifier"].str.split("___").str[0]

    # get chain lengths of all unique GPCRs
    chain_info = load_chain_info_df(
        script_dir / "GPCR_chains_info.csv", df["GPCR"].unique()
    )
    df = filter_df_for_peptriever(df, chain_info)
    df = df.reset_index(drop=True)

    # predict
    out_df = pd.DataFrame(columns=["Identifier", "Distance"])
    for i, row in df.iterrows():
        identifier = row["Identifier"]
        peptide_sequence = row["Ligand Sequence"]
        protein_sequence = row["GPCR Sequence"]
        distance = get_distance(tokenizer, model, peptide_sequence, protein_sequence)
        distance = distance.item()
        distance = float(distance)
        out_df = pd.concat(
            [out_df, pd.DataFrame({"Identifier": [identifier], "Distance": [distance]})]
        )
        print(
            f"Peptriever distance for {i}/{len(df)}, {identifier}\t\t",
            end="\r",
        )
    # lower distance = better binder
    out_df["InteractionProbability"] = out_df["Distance"].apply(lambda x: 1 / (1 + x))
    # rename col header "Identifier" to "identifier"
    out_df = out_df.rename(columns={"Identifier": "identifier"})

    # save
    out_df.to_csv(script_dir / "predictions.csv", index=False)


if __name__ == "__main__":
    main()
