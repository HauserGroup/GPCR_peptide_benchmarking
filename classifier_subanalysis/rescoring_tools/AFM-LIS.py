"""
/projects/ilfgrid/apps/alphafold-2.3.1/AF2.3.1_cuda11.8_conda_env/bin/python "/projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/AFM-LIS.py" -i "/projects/ilfgrid/data/Luuk/Classifier_models/data/AF2_no_templates" -o "/projects/ilfgrid/data/Luuk/Classifier_models/stats/AFM-LIS"
"""
import os 
import pathlib
import argparse
import logging


# jupyter-notebook to handle data derived from original AlphaFold-Multimer. 
# pkl will be used to get iptm, ptm, plddt (thanks to Katerina Atallah-Yunes).
# pae information will be loaded from pkl instead of json (updated on 2024/03/28). 
# the lines for loadning pae-related json were disabled (thanks to Yaqing Cheng).

import os
import json
import pickle
import numpy as np
import pandas as pd
from Bio import PDB
import concurrent.futures


def reverse_and_scale_matrix(matrix: np.ndarray, pae_cutoff: float = 12.0) -> np.ndarray:
    """
    Scale the values in the matrix such that:
    0 becomes 1, pae_cutoff becomes 0, and values greater than pae_cutoff are also 0.
    
    Args:
    - matrix (np.ndarray): Input numpy matrix.
    - pae_cutoff (float): Threshold above which values become 0.
    
    Returns:
    - np.ndarray: Transformed matrix.
    """
    
    # Scale the values to [0, 1] for values between 0 and cutoff
    scaled_matrix = (pae_cutoff - matrix) / pae_cutoff
    scaled_matrix = np.clip(scaled_matrix, 0, 1)  # Ensures values are between 0 and 1
    
    return scaled_matrix


def process_alphafold_output(base_directory: str, model_numbers: int = 5, recycling_numbers: int = 5, Protein_1 = "A", Protein_2 = "B", pae_cutoff: float = 12.0, lis_threshold: float = 0.203, lia_threshold: float = 3432.0) -> pd.DataFrame:
    """
    Process AlphaFold output files and return a DataFrame containing relevant information.
    
    Args:
    - base_directory (str): Base directory where the AlphaFold output files are stored.
    - model_numbers (int): Number of models to process.
    - recycling_numbers (int): Number of recycling indices to process.
    - pae_cutoff (float): Threshold for PAE matrix above which values become 0.
    - lis_threshold (float): Threshold for LIS (Local Interaction Score) to filter results.
    - lia_threshold (float): Threshold for LIA (Local Interaction Area) to filter results.
    
    Returns:
    - pd.DataFrame: DataFrame containing processed data.
    """
    
    # Initialize a list to hold the Pandas Series objects
    series_list = []

    # Loop over each model number and recycling number
    for model_num in range(1, model_numbers+1):
        for recycling_num in range(0, recycling_numbers):
            # print(f"Model: {model_num}, Recycle: {recycling_num}")
            
            # pae_name = f"pae_model_{model_num}_multimer_v3_pred_{recycling_num}.json"
            # pae_file_path = os.path.join(base_directory, pae_name)
            # with open(pae_file_path, 'r') as file:
            #     json_data = json.load(file)


            pdb_name = f"unrelaxed_model_{model_num}_multimer_v3_pred_{recycling_num}.pdb"
            pdb_file_path = os.path.join(base_directory, pdb_name)


            parser = PDB.PDBParser(QUIET=True)
            structure = parser.get_structure("example", pdb_file_path)
            
            chain_lengths = {}
            
            for model in structure:
                for chain in model:
                    chain_id = chain.get_id()
                    chain_length = sum(1 for _ in chain.get_residues())  # Calculate chain length
                    chain_lengths[chain_id] = chain_length
                    # Accessing the length of chain 'A' from the dictionary
                    protein_a_len = chain_lengths.get('B', 0)  # Default to 0 if 'A' chain is not found
            # print(chain_lengths)
            # print(protein_a_len)

            pkl_name = f"result_model_{model_num}_multimer_v3_pred_{recycling_num}.pkl"
            pkl_file_path = os.path.join(base_directory, pkl_name)
            d = pickle.load(open(pkl_file_path,'rb'))
            iptm = d.get('iptm')
            ptm = d.get('ptm')
            # added on 2024/03/28 #
            pae = d.get('predicted_aligned_error')
            # added on 2024/03/28 #
            plddt = np.mean(d.get('plddt'))
            confidence = d.get('ranking_confidence')

            # print(pae_file_path)
            # print(pdb_file_path)
            # print(pkl_file_path)
            # print(iptm)
            # print(ptm)
            # print(plddt)

            # pae = np.array(json_data[0]['predicted_aligned_error'])
            # pae_data[f"model_{model_num}_recycle_{recycling_num}"] = pae_matrix

            pae_cutoff = 12

            thresholded_pae = np.where(pae < pae_cutoff, 1, 0)

            # Calculate the interaction amino acid numbers
            local_interaction_protein_a = np.count_nonzero(thresholded_pae[:protein_a_len, :protein_a_len])
            local_interaction_protein_b = np.count_nonzero(thresholded_pae[protein_a_len:, protein_a_len:])
            local_interaction_interface_1 = np.count_nonzero(thresholded_pae[:protein_a_len, protein_a_len:])
            local_interaction_interface_2 = np.count_nonzero(thresholded_pae[protein_a_len:, :protein_a_len])
            local_interaction_interface_avg = (
                local_interaction_interface_1 + local_interaction_interface_2
            )

            
            # Calculate average thresholded_pae for each region
            average_thresholded_protein_a = thresholded_pae[:protein_a_len,:protein_a_len].mean() * 100
            average_thresholded_protein_b = thresholded_pae[protein_a_len:,protein_a_len:].mean() * 100
            average_thresholded_interaction1 = thresholded_pae[:protein_a_len,protein_a_len:].mean() * 100
            average_thresholded_interaction2 = thresholded_pae[protein_a_len:,:protein_a_len].mean() * 100
            average_thresholded_interaction_total = (average_thresholded_interaction1 + average_thresholded_interaction2) / 2
            

            pae_protein_a = np.mean( pae[:protein_a_len,:protein_a_len] )
            pae_protein_b = np.mean( pae[protein_a_len:,protein_a_len:] )
            pae_interaction1 = np.mean(pae[:protein_a_len,protein_a_len:])
            pae_interaction2 = np.mean(pae[protein_a_len:,:protein_a_len])
            pae_interaction_total = ( pae_interaction1 + pae_interaction2 ) / 2

            # For pae_A
            selected_values_protein_a = pae[:protein_a_len, :protein_a_len][thresholded_pae[:protein_a_len, :protein_a_len] == 1]
            average_selected_protein_a = np.mean(selected_values_protein_a)

            # For pae_B
            selected_values_protein_b = pae[protein_a_len:, protein_a_len:][thresholded_pae[protein_a_len:, protein_a_len:] == 1]
            average_selected_protein_b = np.mean(selected_values_protein_b)

            # For pae_interaction1
            selected_values_interaction1 = pae[:protein_a_len, protein_a_len:][thresholded_pae[:protein_a_len, protein_a_len:] == 1]
            average_selected_interaction1 = np.mean(selected_values_interaction1) if selected_values_interaction1.size > 0 else pae_cutoff

            # For pae_interaction2
            selected_values_interaction2 = pae[protein_a_len:, :protein_a_len][thresholded_pae[protein_a_len:, :protein_a_len] == 1]
            average_selected_interaction2 = np.mean(selected_values_interaction2) if selected_values_interaction2.size > 0 else pae_cutoff

            # For pae_interaction_total
            average_selected_interaction_total = (average_selected_interaction1 + average_selected_interaction2) / 2

        # At this point, plddt_data and pae_data dictionaries will have the extracted data
            print_results = False
            if print_results:
                # Print the total results
                print("Total pae_A : {:.2f}".format(pae_protein_a))
                print("Total pae_B : {:.2f}".format(pae_protein_b))
                print("Total pae_i_1 : {:.2f}".format(pae_interaction1))
                print("Total pae_i_2 : {:.2f}".format(pae_interaction2))
                print("Total pae_i_avg : {:.2f}".format(pae_interaction_total))

                # Print the local results
                print("Local pae_A : {:.2f}".format(average_selected_protein_a))
                print("Local pae_B : {:.2f}".format(average_selected_protein_b))
                print("Local pae_i_1 : {:.2f}".format(average_selected_interaction1))
                print("Local pae_i_2 : {:.2f}".format(average_selected_interaction2))
                print("Local pae_i_avg : {:.2f}".format(average_selected_interaction_total))

                # Print the >PAE-cutoff area
                print("Local interaction area (Protein A):", local_interaction_protein_a)
                print("Local interaction area (Protein B):", local_interaction_protein_b)
                print("Local interaction area (Interaction 1):", local_interaction_interface_1)
                print("Local interaction area (Interaction 2):", local_interaction_interface_2)
                print("Total Interaction area (Interface):", local_interaction_interface_avg)


            # Transform the pae matrix
            scaled_pae = reverse_and_scale_matrix(pae, pae_cutoff)

            # For local interaction score for protein_a
            selected_values_protein_a = scaled_pae[:protein_a_len, :protein_a_len][thresholded_pae[:protein_a_len, :protein_a_len] == 1]
            average_selected_protein_a_score = np.mean(selected_values_protein_a)

            # For local interaction score for protein_b
            selected_values_protein_b = scaled_pae[protein_a_len:, protein_a_len:][thresholded_pae[protein_a_len:, protein_a_len:] == 1]
            average_selected_protein_b_score = np.mean(selected_values_protein_b)

            # For local interaction score1
            selected_values_interaction1_score = scaled_pae[:protein_a_len, protein_a_len:][thresholded_pae[:protein_a_len, protein_a_len:] == 1]
            average_selected_interaction1_score = np.mean(selected_values_interaction1_score) if selected_values_interaction1_score.size > 0 else 0

            # For local interaction score2
            selected_values_interaction2_score = scaled_pae[protein_a_len:, :protein_a_len][thresholded_pae[protein_a_len:, :protein_a_len] == 1]
            average_selected_interaction2_score = np.mean(selected_values_interaction2_score) if selected_values_interaction2_score.size > 0 else 0

            # For average local interaction score
            average_selected_interaction_total_score = (average_selected_interaction1_score + average_selected_interaction2_score) / 2

            # Append the data to the series list
            series_list.append(pd.Series({
                'Protein_1': Protein_1,
                'Protein_2': Protein_2,
                'LIS': round(average_selected_interaction_total_score, 3), # Local Interaction Score (LIS)
                'LIA': local_interaction_interface_avg, # Local Interaction Area (LIA)
                'ipTM': round(float(iptm), 3),
                'Confidence': round(float(iptm*0.8 + ptm*0.2),3),
                'pTM': round(float(ptm), 3),
                'pLDDT': round(plddt, 2),
                'Model': model_num,
                'Recycle': recycling_num,
                'saved folder': os.path.dirname(pdb_file_path),
                'pdb': os.path.basename(pdb_file_path),
                'pkl': os.path.basename(pkl_file_path),
            }))

    # Concatenate all Pandas Series objects into a single DataFrame
    result_df = pd.concat(series_list, axis=1).T
    
    # Filter rows based on the specified LIS and LIA thresholds
    result_df_filtered = result_df[(result_df['LIS'] >= lis_threshold) & (result_df['LIA'] >= lia_threshold)]
    
    return result_df, result_df_filtered


def run_pred_for_af_dir(base_directory :str,
                        protein_1 = "A",
                        protein_2 = "B"):
    """
    base_directory = 'YOUR ALPHAFOLD OUTPUT FOLDER'
    """
    # Example usage:
    model_numbers = 5
    recycling_numbers = 1
    pae_cutoff = 12 
    lis_threshold = 0.203 # might be too strict for weak or transient interaction
    lia_threshold = 3432.0 
    result_df, result_df_filtered = process_alphafold_output(base_directory, model_numbers, recycling_numbers, protein_1, protein_2, pae_cutoff, lis_threshold, lia_threshold,)
    return result_df, result_df_filtered


def run_main():
    args = argparse.ArgumentParser()
    args.add_argument("-i", "--af2_dir", type=pathlib.Path, required=True, help="The AF2 main dir, with subdirs for each prediction")
    args.add_argument("-o", "--output_dir", type=pathlib.Path, required=True, help="Output directory, will contain two .csv files")
    args = args.parse_args()

    # check args
    if not args.af2_dir.exists():
        raise ValueError(f"AF2 dir does not exist: {args.af2_dir}")
    # check out dir exists and is not empty
    if not os.path.exists(args.output_dir):
        args.output_dir.mkdir(parents=True, exist_ok=True)
    else:
        # if not empty (except for .log)
        if len(list(args.output_dir.iterdir())) > 1:
            raise ValueError(f"Output dir is not empty: {args.output_dir}")
    result_df_csv_p = args.output_dir / "result_df.csv"
    result_df_filtered_csv_p = args.output_dir / "result_df_filtered.csv"
    log_p = args.output_dir / "run.log"
    logging.basicConfig(filename=log_p, level=logging.INFO, filemode="w", format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")    
    logging.info(f"Starting run")
    
    # get all subd9irs
    subdirs = list(pathlib.Path(args.af2_dir).iterdir())
    subdirs = [str(subdir) for subdir in subdirs if subdir.is_dir()]
    
    logging.info(f"Found {len(subdirs)} subdirs")
    subdir_index = -1
    for subdir in subdirs:
        logging.info(f"Processing subdir: {subdir}")
        subdir_p = os.path.join(args.output_dir, subdir)

        try:
            result_df, result_df_filtered = run_pred_for_af_dir(subdir_p)
        except FileNotFoundError as e:
            logging.error(f"Error: {e}")
            continue

        # count the valid subdirs
        subdir_index += 1

        if subdir_index < 1:
            result_df.to_csv(result_df_csv_p, index=False)
            result_df_filtered.to_csv(result_df_filtered_csv_p, index=False)
        else:
            # append
            with open(result_df_csv_p, 'a') as f:
                result_df.to_csv(f, header=False, index=False)
            with open(result_df_filtered_csv_p, 'a') as f:
                result_df_filtered.to_csv(f, header=False, index=False)
        logging.info(f"Processed subdir: {subdir}")
    logging.info(f"Finished run")


if __name__ == "__main__":
    run_main()