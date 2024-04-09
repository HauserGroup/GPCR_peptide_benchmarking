""" Get the decoys for each GPCR
"""
import pathlib
import os
import glob
import random
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
try:
    import cv2
except ImportError:
    print("cv2 not installed. Cannot create video")
    cv2 = None


from step1_get_valid_interactions import plt_pie_chart
from step5_get_node_graph import plot_interactions_network_components_style, create_igraph_graph_for_interactions_df
from step5_get_node_graph import get_subgraph_plot_grid_component, combine_images_of_different_sizes_left_to_right


def plot_decoy_dataset(df, plot_dir):
    """
    """
    # similarity to original target
    similarity_to_original_target_plot = plot_dir / "similarity_to_original_target.png"  
    decoy_rows = df[df["Acts as agonist"] == False]
    dissimilar_vals = decoy_rows[df["Decoy Type"] == "Dissimilar"]["Target Similarity to Original Target"].values
    similar_vals = decoy_rows[df["Decoy Type"] == "Similar"]["Target Similarity to Original Target"].values
    # matplotlib distribution of the two vals
    fig, ax = plt.subplots()
    # set xtickts steps of 5
    ax.set_xlabel("Binding pocket similarity to original GPCR target")
    ax.set_ylabel("Count")

    sns.histplot(dissimilar_vals, ax=ax, color="red", binwidth=5, binrange=(0, 100),
                 alpha=0.5, label="Dissimilar")
    sns.histplot(similar_vals, ax=ax, color="blue", binwidth=5, binrange=(0, 100),
                 alpha=0.5, label="Similar")
    ax.set_xticks(np.arange(0, 105, 5))

    plt.legend()
    plt.title("Similar and dissimilar decoys,\ndistribution of binding pocket similarity")
    # add total count
    count_label = f"Total: {len(df)}, Similar: {len(similar_vals)}, Dissimilar: {len(dissimilar_vals)}"
    ax.text(0.01, 0.97, count_label, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    fig.savefig(similarity_to_original_target_plot)
    plt.close()

    # how often 1 decoy is used
    plt_pie_chart(df=df, 
                  col="Decoy ID", 
                  transparent=False,
                  save_path=plot_dir / "how_often_decoy_is_used.png")

    # decoy counts bar plot
    fig,ax = plt.subplots()
    # fig size
    fig.set_size_inches(8, 6)
    decoy_counts_plot = plot_dir / "decoy_counts.png"
    decoy_counts_dissimilar = decoy_rows[df["Decoy Type"] == "Dissimilar"]["Decoy ID"].value_counts()
    decoy_counts_similar = decoy_rows[df["Decoy Type"] == "Similar"]["Decoy ID"].value_counts()
    print("UNIQUE SIMILAR DECOYS:", len(decoy_counts_similar))
    print("UNIQUE DISSIMILAR DECOYS:", len(decoy_counts_dissimilar))
    max_count = max(max(decoy_counts_similar), max(decoy_counts_dissimilar))
    # plot
    sns.histplot(decoy_counts_dissimilar, ax=ax, color="red", binwidth=5, binrange=(0, max_count),
                    alpha=0.5, label="Dissimilar")
    sns.histplot(decoy_counts_similar, ax=ax, color="blue", binwidth=5, binrange=(0, max_count),
                    alpha=0.5, label="Similar")
    ax.legend()
    # title
    ax.set_title("Distribution of decoy counts", fontsize=16)
    ax.set_xlabel("Number of times a decoy is used", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    ax.minorticks_on()
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)    
    # save
    fig.savefig(decoy_counts_plot)
    plt.close()
    print("Dissimilar decoy counts:", decoy_counts_dissimilar)
    print("Similar decoy counts:", decoy_counts_similar)


def get_vertex_order_for_separate_component_plot(g, components, get_vertex_name):
    """ Our plotting methods splits the subnetworks into individual plots, then combines them.
        To show the decoys, we want to go from the first appearing vertex to the last appearing vertex.
        This function returns the order of the vertices for each component in the final plot.
    """
    order_of_vertices = list()

    for component in components:
        subgraph = g.subgraph(component)
        original_vertex_ids = [component[j] for j in subgraph.vs.indices]
        original_vertex_names = [get_vertex_name(v) for v in original_vertex_ids]

        receptor_order_of_appearance = list()
        for vertex in subgraph.vs:
            v_name = original_vertex_names[vertex.index]
            if v_name.endswith("_human"):
                receptor_order_of_appearance.insert(0, v_name)
        
        order_of_vertices.extend(receptor_order_of_appearance)
    
    return order_of_vertices


def create_mp4_from_image_paths(image_paths, save_path, fps=5):
    """ Create a video from a list of image paths using cv2
    """
    # if the module couldn't be imported, don't create a video
    if cv2 is None:
        return None
    
    # get all images
    images = [cv2.imread(str(p)) for p in image_paths]
    # get shape
    height, width, layers = images[0].shape

    # Define the codec using 'mp4v' and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(str(save_path), fourcc, fps, (width,height))

    # write the images
    for image in images:
        video.write(image)

    # close the video
    cv2.destroyAllWindows()
    video.release()


def plot_decoy_video(interactions_df, decoy_df, plot_dir):
    """ Plot a video for each GPCR,
        showing the principal agonist as green,
        the decoys as red

        interactions_df: pandas df with columns "Target GPCRdb ID", "Ligand ID", "Principal Agonist"
        decoy_df: pandas df with columns "Target ID", "Decoy ID", ""Acts as agonist", "Decoy Type", "Decoy Rank", "Original Target", "Target Similarity to Original Target"
    """
    # data
    ligands = interactions_df["Ligand ID"].unique()
    receptors = interactions_df["Target GPCRdb ID"].unique()
    # make "Acts as agonist" column boolean
    decoy_df["Acts as agonist"] = decoy_df["Acts as agonist"].astype(bool)
    g, ligand_name_to_index, receptor_name_to_index = create_igraph_graph_for_interactions_df(interactions_df, ligands, receptors)
    ligand_index_to_name = {v:k for k,v in ligand_name_to_index.items()}
    receptor_index_to_name = {v:k for k,v in receptor_name_to_index.items()}
    get_vertex_name = lambda v: ligand_index_to_name.get(v, receptor_index_to_name.get(v, None))

    # save make
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    default_size = 1
    components = g.components()
    components = sorted(components, key=len, reverse=True)
    vertex_order = get_vertex_order_for_separate_component_plot(g, components, get_vertex_name=get_vertex_name)

    saved_plot_paths = list()
    for target_index, target_to_plot in enumerate(vertex_order):
        print(f"Plotting {target_to_plot} ({target_index+1}/{len(receptors)})")
        # make decoy_df "Acts as agonist" column boolean
        decoy_df["Acts as agonist"] = decoy_df["Acts as agonist"].astype(bool)
        # get target edges for this target_to_plot
        decoy_ligands = decoy_df.loc[(decoy_df["Acts as agonist"] == False) & (decoy_df["Target ID"] == target_to_plot), "Decoy ID"].unique().tolist()
        target_edge_targets = decoy_df.loc[(decoy_df["Acts as agonist"] == True) & (decoy_df["Target ID"] == target_to_plot), "Target ID"].unique().tolist()
        target_edge_ligands = decoy_df.loc[(decoy_df["Acts as agonist"] == True) & (decoy_df["Target ID"] == target_to_plot), "Decoy ID"].unique().tolist()
        target_edges = list(zip(target_edge_targets, target_edge_ligands))

        single_plot_path = plot_dir / f"{target_index}_{target_to_plot}.png"

        # sort components by size, get all images
        all_images = []
        for graph_index, component in enumerate(components):
            component_im = get_subgraph_plot_grid_component(g, component, default_size, ligand_name_to_index, receptor_name_to_index,
                                                             get_vertex_name,
                                                             target_edges=target_edges, decoy_ligands=decoy_ligands)
            all_images.append(component_im)

        # reverse all images
        grid = combine_images_of_different_sizes_left_to_right(all_images,
                                                            output_height=2000,
                                                            output_width=2500)
        
        grid.save(single_plot_path)
        saved_plot_paths.append(single_plot_path)

    # plot video
    video_save_path = plot_dir / "decoy_video.mp4"
    create_mp4_from_image_paths(saved_plot_paths, video_save_path)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--interactions_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--decoy_dataset_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--plot_dir", type=pathlib.Path, required=True)

    ARGS = PARSER.parse_args()

    INTERACTIONS_DF = pd.read_csv(ARGS.interactions_path)
    DECOY_DF = pd.read_csv(ARGS.decoy_dataset_path)

    plot_decoy_dataset(DECOY_DF, ARGS.plot_dir)

    plot_decoy_video(interactions_df=INTERACTIONS_DF,
                     decoy_df=DECOY_DF,
                     plot_dir=ARGS.plot_dir,
                     )
