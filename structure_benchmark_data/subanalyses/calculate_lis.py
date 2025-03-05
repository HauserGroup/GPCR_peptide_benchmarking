import os
import json
import pickle
import glob
import numpy as np
import pandas as pd
from Bio import PDB
import os
import re
import json
import numpy as np
import pandas as pd
from collections import Counter
from scipy.spatial.distance import pdist, squareform

# Script to calculate AF2 and AF3 LIS scores
# From the original developers:
# AF3: https://github.com/flyark/AFM-LIS/blob/main/alphafold3_local_interaction_score.ipynb
# AF2: https://github.com/flyark/AFM-LIS/blob/main/alphafold_interaction_scores_for%20alphafold-multimer%20data_v0.31.ipynb

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

    # Read in ranking_debug.json
    ranking_debug_path = os.path.join(base_directory, "ranking_debug.json")
    ranking_debug = json.load(open(ranking_debug_path, 'rb'))
    best_model = ranking_debug["order"][0]
    
    # Initialize a list to hold the Pandas Series objects
    series_list = []

    # Loop over each model number and recycling number
    for model_num in range(1, int(model_numbers)+1):
        for recycling_num in range(0, recycling_numbers):
            pdb_name = f"unrelaxed_model_{model_num}_multimer_v3_pred_{recycling_num}.pdb"
            pdb_file_path = os.path.join(base_directory, pdb_name)
            if best_model not in pdb_file_path:
                continue

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

            pkl_name = f"result_model_{model_num}_multimer_v3_pred_{recycling_num}_filtered.pkl"
            pkl_file_path = os.path.join(base_directory, pkl_name)
            d = pickle.load(open(pkl_file_path,'rb'))
            iptm = d.get('iptm')
            ptm = d.get('ptm')
            # added on 2024/03/28 #
            pae = d.get('predicted_aligned_error')
            # added on 2024/03/28 #
            plddt = np.mean(d.get('plddt'))
            confidence = d.get('ranking_confidence')
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
    
    return result_df

def transform_pae_matrix(pae_matrix, pae_cutoff):
    # Initialize the transformed matrix with zeros
    transformed_pae = np.zeros_like(pae_matrix)

    # Apply transformation: pae = 0 -> score = 1, pae = cutoff -> score = 0, above cutoff -> score = 0
    # Linearly scale values between 0 and cutoff to fall between 1 and 0
    within_cutoff = pae_matrix < pae_cutoff
    transformed_pae[within_cutoff] = 1 - (pae_matrix[within_cutoff] / pae_cutoff)

    return transformed_pae

def calculate_mean_lis(transformed_pae, subunit_number):
    # Calculate the cumulative sum of protein lengths to get the end indices of the submatrices
    cum_lengths = np.cumsum(subunit_number)

    # Add a zero at the beginning of the cumulative lengths to get the start indices
    start_indices = np.concatenate(([0], cum_lengths[:-1]))

    # Initialize an empty matrix to store the mean LIS
    mean_lis_matrix = np.zeros((len(subunit_number), len(subunit_number)))

    # Iterate over the start and end indices
    for i in range(len(subunit_number)):
        for j in range(len(subunit_number)):
            # Get the start and end indices of the interaction submatrix
            start_i, end_i = start_indices[i], cum_lengths[i]
            start_j, end_j = start_indices[j], cum_lengths[j]

            # Get the interaction submatrix
            submatrix = transformed_pae[start_i:end_i, start_j:end_j]

            # Calculate the mean LIS, considering only non-zero values
            mean_lis = submatrix[submatrix > 0].mean()

            # Store the mean LIS in the matrix
            mean_lis_matrix[i, j] = mean_lis

    return mean_lis_matrix

def calculate_contact_map(cif_file, distance_threshold=8):
    def read_cif_lines(cif_path):
        with open(cif_path, 'r') as file:
            lines = file.readlines()

        residue_lines = []
        for line in lines:
            if line.startswith('ATOM') and ('CB' in line or 'GLY' in line and 'CA' in line):
                residue_lines.append(line.strip())  # Store the line if it meets the criteria for ATOM

            if line.startswith('ATOM') and 'P   ' in line:
                residue_lines.append(line.strip()) # Store the line if it meets the criteria for ATOM

            elif line.startswith('HETATM'):
                residue_lines.append(line.strip())  # Store all HETATM lines

        return residue_lines

    def lines_to_dataframe(residue_lines):
        # Split lines and create a list of dictionaries for each atom
        data = []
        for line in residue_lines:
            parts = line.split()
            # Correctly convert numerical values
            for i in range(len(parts)):
                try:
                    parts[i] = float(parts[i])
                except ValueError:
                    pass
            data.append(parts)

        df = pd.DataFrame(data)

        # Add line number column
        df.insert(0, 'residue', range(1, 1 + len(df)))

        return df

    # Read lines from CIF file
    residue_lines = read_cif_lines(cif_file)

    # Convert lines to DataFrame
    df = lines_to_dataframe(residue_lines)

    # Assuming the columns for x, y, z coordinates are at indices 11, 12, 13 after insertion
    coordinates = df.iloc[:, 11:14].to_numpy()

    distances = squareform(pdist(coordinates))

    # Assuming the column for atom names is at index 3 after insertion
    has_phosphorus = df.iloc[:, 3].apply(lambda x: 'P' in str(x)).to_numpy()

    # Adjust the threshold for phosphorus-containing residues
    adjusted_distances = np.where(has_phosphorus[:, np.newaxis] | has_phosphorus[np.newaxis, :],
                                  distances - 4, distances)

    contact_map = np.where(adjusted_distances < distance_threshold, 1, 0)
    return contact_map

def afm3_plot_average_to_df(af3_jsons, pae_cutoff=12, distance_cutoff=8, result_save = "True"):
    sum_pae_matrix = None
    sum_transformed_pae_matrix = None
    sum_mean_lis_matrix = None
    sum_contact_lia_map = None
    sum_iptm_matrix = None
    all_interactions = []

    for af3_json in af3_jsons:
        json_data = json.load(open(af3_json, 'rb'))
        json_confidence = af3_json.replace('full_data', 'summary_confidences')
        confidence_data = json.load(open(json_confidence, 'rb'))
        token_chain_ids = json_data['token_chain_ids']
        chain_residue_counts = Counter(token_chain_ids)
        subunit_number = list(chain_residue_counts.values())
        pae_matrix = np.array(json_data['pae'])
        subunit_sizes = subunit_number

        cif_file = af3_json.replace('_full_data_', '_model_').replace('.json', '.cif')

        transformed_pae_matrix = transform_pae_matrix(pae_matrix, pae_cutoff)
        transformed_pae_matrix = np.nan_to_num(transformed_pae_matrix)
        lia_map = np.where(transformed_pae_matrix > 0, 1, 0)

        mean_lis_matrix = calculate_mean_lis(transformed_pae_matrix, subunit_sizes)
        mean_lis_matrix = np.nan_to_num(mean_lis_matrix)

        contact_map = calculate_contact_map(cif_file, distance_cutoff)
        combined_map = np.where((transformed_pae_matrix > 0) & (contact_map == 1), transformed_pae_matrix, 0)

        mean_clis_matrix = calculate_mean_lis(combined_map, subunit_sizes)
        mean_clis_matrix = np.nan_to_num(mean_clis_matrix)

        lia_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        lir_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        clia_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        clir_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))

        for i in range(len(subunit_sizes)):
            for j in range(len(subunit_sizes)):
                start_i, end_i = sum(subunit_sizes[:i]), sum(subunit_sizes[:i+1])
                start_j, end_j = sum(subunit_sizes[:j]), sum(subunit_sizes[:j+1])
                interaction_submatrix = lia_map[start_i:end_i, start_j:end_j]

                lia_matrix[i, j] = int(np.count_nonzero(interaction_submatrix))
                residues_i = np.unique(np.where(interaction_submatrix > 0)[0]) + start_i
                residues_j = np.unique(np.where(interaction_submatrix > 0)[1]) + start_j
                lir_matrix[i, j] = int(len(residues_i) + len(residues_j))

                combined_submatrix = combined_map[start_i:end_i, start_j:end_j]
                clia_matrix[i, j] = int(np.count_nonzero(combined_submatrix))

                residues_i = np.unique(np.where(combined_submatrix > 0)[0]) + start_i
                residues_j = np.unique(np.where(combined_submatrix > 0)[1]) + start_j
                clir_matrix[i, j] = int(len(residues_i) + len(residues_j))

        iptm_matrix = confidence_data['chain_pair_iptm']
        iptm_matrix = np.array(iptm_matrix, dtype=float)
        iptm_matrix = np.nan_to_num(iptm_matrix)

        if sum_pae_matrix is None:
            sum_pae_matrix = pae_matrix
            sum_transformed_pae_matrix = transformed_pae_matrix
            sum_mean_lis_matrix = mean_lis_matrix
            sum_contact_lia_map = combined_map
            sum_iptm_matrix = iptm_matrix
        else:
            sum_pae_matrix += pae_matrix
            sum_transformed_pae_matrix += transformed_pae_matrix
            sum_mean_lis_matrix += mean_lis_matrix
            sum_contact_lia_map += combined_map
            sum_iptm_matrix += iptm_matrix

        model_number = re.search(r'full_data_(\d+)', af3_json).group(1)
        folder_name = os.path.basename(os.path.dirname(af3_json))
        for i in range(len(subunit_sizes)):
            for j in range(len(subunit_sizes)):
                interaction = {
                    'folder_name': folder_name,
                    'model_number': model_number,
                    'protein_1': i + 1,
                    'protein_2': j + 1,
                    'LIS': mean_lis_matrix[i, j],
                    'LIA': lia_matrix[i, j],
                    'LIR': lir_matrix[i, j],
                    'cLIS': mean_clis_matrix[i, j],
                    'cLIA': clia_matrix[i, j],
                    'cLIR': clir_matrix[i, j],
                    'iptm': iptm_matrix[i, j],
                }
                all_interactions.append(interaction)

    avg_pae_matrix = sum_pae_matrix / len(af3_jsons)
    avg_transformed_pae_matrix = sum_transformed_pae_matrix / len(af3_jsons)
    avg_mean_lis_matrix = sum_mean_lis_matrix / len(af3_jsons)
    avg_contact_lia_map = sum_contact_lia_map / len(af3_jsons)
    avg_iptm_matrix = sum_iptm_matrix / len(af3_jsons)

    avg_pae_matrix = np.nan_to_num(avg_pae_matrix)
    avg_transformed_pae_matrix = np.nan_to_num(avg_transformed_pae_matrix)
    avg_mean_lis_matrix = np.nan_to_num(avg_mean_lis_matrix)
    avg_iptm_matrix = np.nan_to_num(avg_iptm_matrix)

    df_interactions = pd.DataFrame(all_interactions)
    df_interactions['interaction'] = df_interactions.apply(lambda row: tuple(sorted((row['protein_1'], row['protein_2']))), axis=1)
    df_merged = df_interactions.groupby(['folder_name', 'model_number', 'interaction']).mean().reset_index()
    df_merged[['protein_1', 'protein_2']] = pd.DataFrame(df_merged['interaction'].tolist(), index=df_merged.index)
    df_merged = df_merged.drop(columns=['interaction'])

    # Calculate average values for each protein pair and add as new rows
    avg_rows = []
    interaction_pairs = df_merged.groupby(['protein_1', 'protein_2'])

    for (protein_1, protein_2), group in interaction_pairs:
        avg_row = {
            'folder_name': folder_name,
            'model_number': 'average',
            'protein_1': protein_1,
            'protein_2': protein_2,
            'LIS': group['LIS'].mean(),
            'LIA': group['LIA'].mean(),
            'LIR': group['LIR'].mean(),
            'cLIS': group['cLIS'].mean(),
            'cLIA': group['cLIA'].mean(),
            'cLIR': group['cLIR'].mean(),
            'iptm': group['iptm'].mean(),
        }
        avg_rows.append(avg_row)

    df_avg = pd.DataFrame(avg_rows)
    df_merged = pd.concat([df_merged, df_avg], ignore_index=True)

    df_merged['LIA'] = df_merged['LIA'].astype(int)
    df_merged['LIR'] = df_merged['LIR'].astype(int)
    df_merged['cLIA'] = df_merged['cLIA'].astype(int)
    df_merged['cLIR'] = df_merged['cLIR'].astype(int)

    # Save DataFrame to CSV
    output_folder = os.path.dirname(af3_jsons[0])
    output_path = os.path.join(output_folder, f"{folder_name}_lis_analysis.csv")
    if result_save == "True":
        df_merged.to_csv(output_path, index=False)
        print("Results saved to: ", output_path)
        print(f"{folder_name}_lis_analysis.csv")

    return df_merged

if __name__ == "__main__":
    # Get directory where the current script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_name = "GPRC_peptide_benchmarking"
    index = script_dir.find(repo_name)
    repo_dir = script_dir[:index + len(repo_name)]
    print(f"Repository directory: {repo_dir}")

    # Get paths to AF2 models
    af2_path = "/projects/ilfgrid/data/Interspecies_GPCR_pipeline/3_models/AF-2.3.1/AF_model_StructuralBenchmark/updated_structural_benchmark/processed_data/seed_1"
    af2_no_templates = "/projects/ilfgrid/data/Interspecies_GPCR_pipeline/3_models/AF-2.3.1/AF_model_StructuralBenchmark_no_templates/updated_structural_benchmark_no_templates/processed_data/seed_1"
    af2_paths = glob.glob(f"{af2_path}/*")
    af2_no_templates_paths = glob.glob(f"{af2_no_templates}/*")
    af2_lis_paths = []
    af2_lis_paths.extend(af2_paths)
    af2_lis_paths.extend(af2_no_templates_paths)
    af2_subfolders = [dir for dir in af2_lis_paths if os.path.isdir(dir)]
    print(f"Number of AF2 models: {len(af2_subfolders)}")

    # Get paths to AF3 jsons
    af3 = f"{repo_dir}/structure_benchmark/AF3_server"
    af3_lis_paths = glob.glob(f"{af3}/*")
    af3_jsons = {}
    for path in af3_lis_paths:
        model = path.split("/")[-1].split("_")[-1]
        json_files = glob.glob(f"{path}/*full_data*.json")
        af3_jsons[model] = json_files
    print(f"Number of AF3 models: {len(af3_jsons)}")
    print(af3_jsons)

    # Create a subdirectory for LIS results
    lis_results_dir = f"{repo_dir}/structure_benchmark_data/subanalyses/AFM-LIS_results"
    os.makedirs(lis_results_dir, exist_ok=True)
    print(f"LIS results directory: {lis_results_dir}")

    # Calculate LIS for AF2 models
    af2_results = []
    for model_dir in af2_subfolders:
        try: 
            model_name = model_dir.split("/")[-1]
            total_prediction =  process_alphafold_output(f"{model_dir}/{model_name}", model_numbers = 5, recycling_numbers = 5, Protein_1 = "A", Protein_2 = "B")
            af2_results.append(total_prediction)
        except Exception as e:
            print(f"Error processing {model_dir}: {e}", flush=True)

    af2_results_df = pd.concat(af2_results)
    af2_results_df = af2_results_df.sort_values(by='LIS', ascending=False)
    af2_results_df.to_csv(f"{lis_results_dir}/AF2_LIS_results.csv", index=False)
    print(f"AF2 LIS results saved to: {lis_results_dir}/AF2_LIS_results.csv")

    # Calculate LIS for AF3 models
    af3_results = []
    for model in af3_jsons.keys():
        total_prediction = afm3_plot_average_to_df(af3_jsons[model], result_save = False)
        af3_results.append(total_prediction)
    af3_results_df = pd.concat(af3_results)
    af3_results_df.to_csv(f"{lis_results_dir}/AF3_LIS_results.csv", index=False)
    print(f"AF3 LIS results saved to: {lis_results_dir}/AF3_LIS_results.csv")
