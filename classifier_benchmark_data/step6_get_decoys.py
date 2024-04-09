import pathlib
import argparse
import csv
import pandas as pd
import numpy as np


def get_similarity_df(sim_df, iden_df, target_gpcrdb_id):
    """Get a df of all other GPCRdb IDs and their similarity and identity scores.
    Sorted high to low by similarity score, then by identity score.
    """
    out_df = pd.DataFrame(
        columns=["Target GPCRdb ID", "Similarity Score", "Identity Score"]
    )

    all_gpcrdb_ids = sim_df.index.tolist()
    all_gpcrdb_ids = list(set(all_gpcrdb_ids))

    # remove the target GPCRdb ID
    query_gpcrdb_ids = [g for g in all_gpcrdb_ids if g != target_gpcrdb_id]

    # get the similarity scores for the target GPCRdb ID
    for query_id in query_gpcrdb_ids:
        similarity_score = sim_df.loc[target_gpcrdb_id, query_id]
        identity_score = iden_df.loc[target_gpcrdb_id, query_id]
        out_df.loc[query_id, "Similarity Score"] = similarity_score
        out_df.loc[query_id, "Target GPCRdb ID"] = query_id
        out_df.loc[query_id, "Identity Score"] = identity_score

    # sort by similarity score, then by identity score
    out_df = out_df.sort_values(
        by=["Similarity Score", "Identity Score"], ascending=False
    )

    return out_df


def get_similar_decoys_df(
    sim_df, iden_df, principal_agonist_pairs, target_gpcrdb_id, all_edges
):
    """Get a list of similar decoys"""
    # sort GPCRs on similarity to target
    similarity_df = get_similarity_df(sim_df, iden_df, target_gpcrdb_id)

    # add the principal agonist for each candidate receptor to the df
    receptor_to_pa = {k: v for k, v in principal_agonist_pairs.values.tolist()}
    similarity_df["Principal Agonist"] = similarity_df["Target GPCRdb ID"].map(
        receptor_to_pa
    )

    # check if there is an edge between the target and the principal agonists,
    # this would mean that the peptide isn't a decoy, but a non-principal agonist for the target
    has_no_edge = lambda x: False if [target_gpcrdb_id, x] in all_edges else True
    similarity_df["NoEdge"] = similarity_df["Principal Agonist"].apply(has_no_edge)
    similarity_df = similarity_df[similarity_df["NoEdge"] == True]

    # Each decoy should only be used once, so remove rows from the df that are principal agonist duplicates
    similarity_df = similarity_df.drop_duplicates(subset=["Principal Agonist"])

    return similarity_df


def get_dissimilar_decoys_df(
    sim_df,
    iden_df,
    principal_agonist_pairs,
    target_gpcrdb_id,
    all_edges,
    max_similarity=30,
):
    """Get a list of dissimilar decoys"""
    # sort GPCRs on similarity to target
    similarity_df = get_similarity_df(sim_df, iden_df, target_gpcrdb_id)
    # reverse (dissimilar GPCRs first)
    similarity_df = similarity_df.iloc[::-1]
    # remove rows with similarity score above the threshold
    similarity_df = similarity_df[similarity_df["Similarity Score"] <= max_similarity]

    receptor_to_pa = {k: v for k, v in principal_agonist_pairs.values.tolist()}
    similarity_df["Principal Agonist"] = similarity_df["Target GPCRdb ID"].map(
        receptor_to_pa
    )

    # check if there is an edge between the target and the principal agonists,
    # this would mean that the peptide isn't a decoy, but a non-principal agonist for the target
    has_no_edge = lambda x: False if [target_gpcrdb_id, x] in all_edges else True
    similarity_df["NoEdge"] = similarity_df["Principal Agonist"].apply(has_no_edge)
    similarity_df = similarity_df[similarity_df["NoEdge"] == True]

    # Each decoy should only be used once, so remove rows from the df that are principal agonist duplicates
    similarity_df = similarity_df.drop_duplicates(subset=["Principal Agonist"])

    return similarity_df


def create_decoy_dataset(
    similarity_df_path,
    identity_df_path,
    interactions_df_path,
    out_path,
    use_oversampling=True,
    similar_count=5,
    dissimilar_count=5,
    dissimilarity_threshold=30,
):
    """ """
    # load data
    similarity_matrix_df = pd.read_csv(similarity_df_path, index_col=0)
    identity_matrix_df = pd.read_csv(identity_df_path, index_col=0)
    interactions_df = pd.read_csv(interactions_df_path, index_col=0)
    all_edges = interactions_df[["Target GPCRdb ID", "Ligand ID"]].values.tolist()
    principal_agonist_pairs = interactions_df[
        interactions_df["Principal Agonist"] == True
    ][["Target GPCRdb ID", "Ligand ID"]]

    get_pep_seq = lambda x: interactions_df[interactions_df["Ligand ID"] == x][
        "Ligand Sequence"
    ].iloc[0]
    get_gpcr_seq = lambda x: interactions_df[interactions_df["Target GPCRdb ID"] == x][
        "GPCR Sequence"
    ].iloc[0]

    # open the output file
    with open(out_path, "w") as out_file:
        # init file
        fieldnames = [
            "Target ID",
            "Decoy ID",
            "Acts as agonist",
            "Decoy Type",
            "Decoy Rank",
            "Original Target",
            "Target Similarity to Original Target",
            "Ligand Sequence",
            "GPCR Sequence",
        ]
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        # for each GPCR, get the similar decoys
        for gpcr, pa in principal_agonist_pairs.values.tolist():
            # similar
            similarity_df = get_similar_decoys_df(
                similarity_matrix_df,
                identity_matrix_df,
                principal_agonist_pairs,
                gpcr,
                all_edges=all_edges,
            )
            similar_chosen_df = similarity_df.head(similar_count)

            # dissimilar
            dissimilarity_df = get_dissimilar_decoys_df(
                similarity_matrix_df,
                identity_matrix_df,
                principal_agonist_pairs,
                gpcr,
                all_edges=all_edges,
                max_similarity=dissimilarity_threshold,
            )
            # get rid of dissimilar rows if the ligand is in the similar df
            dissimilarity_df = dissimilarity_df[
                ~dissimilarity_df["Principal Agonist"].isin(
                    similar_chosen_df["Principal Agonist"].tolist()
                )
            ]
            # use numpy to randomly choose rows
            if len(dissimilarity_df) < dissimilar_count:
                print(
                    f"WARNING: Not enough dissimilar decoys for GPCR {gpcr}, {len(dissimilarity_df)} < {dissimilar_count}"
                )
                dissimilar_chosen_indexes = np.random.choice(
                    dissimilarity_df.index, len(dissimilarity_df), replace=False
                )
            else:
                dissimilar_chosen_indexes = np.random.choice(
                    dissimilarity_df.index, dissimilar_count, replace=False
                )
            dissimilar_chosen_df = dissimilarity_df.loc[dissimilar_chosen_indexes]

            # write the similar decoys to file
            for decoy_rank, (_, row) in enumerate(similar_chosen_df.iterrows()):
                csv_writer.writerow(
                    {
                        "Target ID": gpcr,
                        "Decoy ID": row["Principal Agonist"],
                        "Acts as agonist": False,
                        "Decoy Type": "Similar",
                        "Decoy Rank": decoy_rank,
                        "Original Target": row["Target GPCRdb ID"],
                        "Target Similarity to Original Target": row["Similarity Score"],
                        "Ligand Sequence": get_pep_seq(row["Principal Agonist"]),
                        "GPCR Sequence": get_gpcr_seq(gpcr),
                    }
                )
            # write the dissimilar decoys to file
            for decoy_rank, (_, row) in enumerate(dissimilar_chosen_df.iterrows()):
                csv_writer.writerow(
                    {
                        "Target ID": gpcr,
                        "Decoy ID": row["Principal Agonist"],
                        "Acts as agonist": False,
                        "Decoy Type": "Dissimilar",
                        "Decoy Rank": decoy_rank,
                        "Original Target": row["Target GPCRdb ID"],
                        "Target Similarity to Original Target": row["Similarity Score"],
                        "Ligand Sequence": get_pep_seq(row["Principal Agonist"]),
                        "GPCR Sequence": get_gpcr_seq(gpcr),
                    }
                )
            # write the original pair (the principal agonist and the target GPCR) to file
            csv_writer.writerow(
                {
                    "Target ID": gpcr,
                    "Decoy ID": pa,
                    "Acts as agonist": True,
                    "Decoy Type": "Principal Agonist",
                    "Decoy Rank": None,
                    "Original Target": gpcr,
                    "Target Similarity to Original Target": 100,
                    "Ligand Sequence": get_pep_seq(pa),
                    "GPCR Sequence": get_gpcr_seq(gpcr),
                }
            )


def check_decoy_dataset(path_to_decoy_dataset):
    df = pd.read_csv(path_to_decoy_dataset)
    # check that there are no duplicates (Target ID, Decoy ID)
    duplicates = df[df.duplicated(subset=["Target ID", "Decoy ID"])]
    if len(duplicates) > 0:
        raise ValueError(f"Duplicate rows found in decoy dataset: {duplicates}")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--similarity_df_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--identity_df_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--interactions_df_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--out_path", type=pathlib.Path, required=True)

    ARGS = PARSER.parse_args()

    create_decoy_dataset(
        ARGS.similarity_df_path,
        ARGS.identity_df_path,
        ARGS.interactions_df_path,
        ARGS.out_path,
    )
    check_decoy_dataset(ARGS.out_path)
