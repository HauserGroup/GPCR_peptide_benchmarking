import pandas as pd 
import numpy as np
import os
import pathlib
import math
import io
import random
import argparse

import matplotlib.pyplot as plt
from matplotlib import gridspec
import PIL
from PIL import Image

import igraph as ig
ig.config["plotting.backend"] = "matplotlib"


def get_layouts():
    # all igraph layouts for plotting
    return ["auto", "bipartite", "circle", "circular", "dh", "davidson_harel", "drl", "drl_3d", "fr", "fruchterman_reingold", "fr_3d", "fr3d", "fruchterman_reingold_3d", "grid", "grid_3d", "graphopt", "kk", "kamada_kawai", "kk_3d", "kk3d", "kamada_kawai_3d", "lgl", "large", "large_graph", "mds", "random", "random_3d", "rt", "tree", "reingold_tilford", "rt_circular", "reingold_tilford_circular", "sphere", "spherical", "circle_3d", "circular_3d", "star", "sugiyama"]


def get_ligand_receptor_index_mapping(ligands, receptors):
    """ Igraph requires that the nodes are integers.
        This function creates a mapping from ligand name to index (0, 1, 2, ...)
        and from receptor name to index (start from the index after the last ligand)

        returns:
            ligand_name_to_index: dict that maps ligand name to index
            receptor_name_to_index: dict that maps receptor name to index
    """
    # create dict that maps ligands to an index (0, 1, 2, ...), because igraph requires it
    ligand_name_to_index = dict()
    for i, ligand in enumerate(ligands):
        ligand_name_to_index[str(ligand)] = i
    
    # create dict that maps receptors to an index, start from the index after the last ligand
    start_receptor_index = i + 1
    receptor_name_to_index = dict()
    for i, receptor in enumerate(receptors):
        receptor_name_to_index[str(receptor)] = start_receptor_index + i

    return ligand_name_to_index, receptor_name_to_index


def create_igraph_graph_for_interactions_df(df, ligands, receptors):
    """ Create an igraph graph from the dataframe with interactions (not a plot).

    df: dataframe with columns "Ligand ID", "Target GPCRdb ID", "Principal Agonist"
    ligands: list of ligand names
    receptors: list of receptor names
    """
    # create dict that maps ligands to an index (0, 1, 2, ...), because igraph requires it
    ligand_name_to_index, receptor_name_to_index = get_ligand_receptor_index_mapping(ligands, receptors)

    # add two new columns to the dataframe, "Ligand ID index" and "Target GPCRdb ID index"
    df["Ligand ID index"] = list(map(lambda x: ligand_name_to_index[str(x)], df["Ligand ID"]))
    df["Target GPCRdb ID index"] = list(map(lambda x: receptor_name_to_index[str(x)], df["Target GPCRdb ID"]))

    # reorder the columns so that the first column is Ligand ID and the second column is Target GPCRdb ID
    all_columns = df.columns.tolist()
    # reorder all columns
    all_columns = ["Ligand ID index", "Target GPCRdb ID index"] + [c for c in all_columns if c not in ["Ligand ID index", "Target GPCRdb ID index"]]

    df = df[all_columns]

    # create graph from dataframe (must be undirected graph, because we want to get subgraphs (disconnected))
    g = ig.Graph.DataFrame(df, directed=False)

    return g, ligand_name_to_index, receptor_name_to_index


def plot_subgraph(subgraph, ax, layout_name,
                  colors, shapes, vertex_labels, edge_colors):
    """ Plot a subgraph of the full network.

    subgraph: igraph subgraph
    ax: matplotlib axis
    layout_name: str, name of the layout to use
    colors: list of colors for each vertex
    shapes: list of shapes for each vertex
    """
    n_vertices = len(subgraph.vs)
    layout = subgraph.layout(layout_name)
    vertex_labels = [l.replace("_human", "") for l in vertex_labels]
    plt.axis('off')
    plt.margins(0.2) # so the labels are not cut off
    ig.plot(
        subgraph,
        layout=layout,
        target=ax,
        vertex_size=30,
        edge_width=4,
        vertex_colors=colors,
        # color if receptor or ligand. if index in ligand_name_to_index, then it is a ligand
        vertex_color=colors,
        # vertex shapes
        vertex_shape=shapes,
        # vertex labels
        vertex_label=vertex_labels,
        # place labels above the vertices
        vertex_label_dist= -1.1,
        # principal agonists have a black edge, others have a grey edge
        edge_color=edge_colors,
        # edge opacity
        edge_curved=0.25,
        # edge style (dotteed if not principal agonist)
        edge_style=["solid" if e["Principal Agonist"] == 1 else "dotted" for e in subgraph.es],
        # add labels,
        vertex_label_size=15,    
        )    
    # make sure the labels fit (otherwise they are cut off), dont use tight layout because it makes the image too small
    plt.tight_layout(pad=0.0)


def images_have_overlap(image1, image2):
    """ Check if two images overlap

    image1: tuple with (x, y, width, height)
    image2: tuple with (x, y, width, height)
    """
    x1, y1, width1, height1 = image1
    x2, y2, width2, height2 = image2

    # Check if image1 is to the right of image2 or image2 is to the right of image1
    if x1 > x2 + width2 or x2 > x1 + width1:
        return False

    # Check if image1 is below image2 or image2 is below image1
    if y1 > y2 + height2 or y2 > y1 + height1:
        return False

    return True


def combine_images_of_different_sizes_left_to_right(all_images, output_height = 2000, output_width = 2000,
                                                    xpad=10, ypad=10):
    """ The plan is to plot individual 'grid layouts' plots of each component of the network,
    then combine these into 1 image. This function combines a list of numpy arrays of images into 1 large image.
    """
    # all_images = all_images[::-1]
    images = [PIL.Image.fromarray(im) for im in all_images]
    grid = Image.new('RGB', size=(output_width, output_height), color=(255, 255, 255))

    active_x = 0
    active_y = 0
    row_height = 0

    images_handled = list()
    images_in_row = list()
    for image in images:
        # get size of image
        width, height = image.size   

        # see if we can place the image on the current row
        if active_x + width > output_width:
            # go to next row
            active_x = 0
            active_y = active_y + row_height + ypad
            images_in_row = list()
            row_height = 0
        
        # update row height
        row_height = max(row_height, height)

        # if the image is shorter than the row height, lower it
        if height < row_height:
            y_difference = row_height - height
        else:
            y_difference = 0

        # paste image
        grid.paste(image, (active_x, active_y + int(0.75*y_difference)))

        # if pasted out of bounds, raise error
        if active_x + width > output_width or active_y + height > output_height:
            raise ValueError("Image pasted out of bounds")
        # if image didnt fit fully, raise error
        if active_x + width > output_width:
            raise ValueError("Image didnt fit fully")
        if active_y + height > output_height:
            raise ValueError("Image didnt fit fully")
        # check overlap
        for image_handled in images_handled:
            if images_have_overlap(image_handled, (active_x, active_y, width, height)):
                raise ValueError("Images overlap")
               
        # update images handled
        images_handled.append((active_x, active_y, width, height))
        images_in_row.append(image)

        # update active_x
        active_x += width         

        # padding
        active_x += xpad

    return grid


def get_subgraph_plot_grid_component(g, component, default_size,
                                     ligand_name_to_index, receptor_name_to_index,
                                     get_vertex_name,
                                     target_edges=[], decoy_ligands=[]):
    """ Returns a numpy array of the image of the subgraph

    g: igraph graph
    component: list of vertex indices
    default_size: float, default size of the plot, so the plots scale with the number of nodes
    ligand_name_to_index: dict that maps ligand name to index
    get_vertex_name: function that returns the name of a vertex given its index

    target_edges: list of tuples with (target id, ligand id) 
                  these edges will be colored green
    decoy_ligands: list of ligand ids (str), these ligands will be colored red

    """
    # subplot size
    size = math.sqrt(len(component)) * default_size
    # create plot
    fig, ax = plt.subplots()
    fig.set_size_inches(size, size)

    # get subgraph to plot
    subgraph = g.subgraph(component)
    original_vertex_ids = [component[j] for j in subgraph.vs.indices]
    original_vertex_names = [get_vertex_name(v) for v in original_vertex_ids]

    # color the edges
    edge_colors = list()
    for e in subgraph.es:
            if e["Principal Agonist"] == 1:
                edge_colors.append((0, 0, 0, 1.0))
            else:
                edge_colors.append((0, 0, 0, 0.2))

    decoy_ligands = list(map(str, decoy_ligands))
    target_ligands = [str(e[1]) for e in target_edges]
    targets = [str(e[0]) for e in target_edges]

    # color the vertices
    colors = list()
    for v in original_vertex_ids:
        v_name = get_vertex_name(v)
        # if it is a decoy ligand, color it red
        if v_name in decoy_ligands:
            colors.append("red")
        # if it is a target ligand, color it green
        elif v_name in target_ligands:
            colors.append("green")
        # if it is a target GPCR, color it green
        elif v_name in targets:
            colors.append("green")
        # if it is a ligand, color it cyan
        elif v in ligand_name_to_index.values():
            colors.append("cyan")
        # if it is a receptor, color it blue
        elif v in receptor_name_to_index.values():
            colors.append("blue")
        else:
            raise ValueError("Vertex not a receptor or ligand")
        
    shapes = ["circle" if v in ligand_name_to_index.values() else "square" for v in original_vertex_ids]


    # do the plotting
    plot_subgraph(subgraph, ax, layout_name="grid", colors=colors, shapes=shapes, vertex_labels=original_vertex_names, edge_colors=edge_colors)

    # store the image of this subgraph into a list, so we can later combine them into one image
    buff = io.BytesIO()
    plt.savefig(buff, format="jpeg",  pad_inches=0.1, dpi=200)
    buff.seek(0)
    im = PIL.Image.open(buff)
    im = np.asarray(im)
    plt.close()
    return im


def plot_interactions_network_components_style(g, ligand_name_to_index, receptor_name_to_index, get_vertex_name, save_path):
    """ Plot the full network, but each component is plotted in a 'grid' style,
        as this is the only style that looks organized.
    """
    default_size = 1
    # get components
    components = g.components()
    print(f"Creating a graph with {len(components)} components")
    
    # sort components by size, get all images
    all_images = []
    for graph_index, component in enumerate(sorted(components, key=len, reverse=True)):
        component_im = get_subgraph_plot_grid_component(g, component, default_size, ligand_name_to_index, receptor_name_to_index, get_vertex_name)
        all_images.append(component_im)

    # reverse all images
    grid = combine_images_of_different_sizes_left_to_right(all_images,
                                                           output_height=4000,
                                                           output_width=5000)
    
    grid.save(save_path,
                format="png",
                # use high quality
                quality=1000)


def run_main(interactions_with_principal_agonists_path,
             network_plot_path):
    """ Load the interactions df, create a graph from it, and plot it.
    """
    # load data
    df = pd.read_csv(interactions_with_principal_agonists_path)
    ligands = df["Ligand ID"].unique().tolist()
    receptors = df["Target GPCRdb ID"].unique().tolist()

    # get graph
    g, ligand_name_to_index, receptor_name_to_index = create_igraph_graph_for_interactions_df(df, ligands, receptors)
    # invert the mappings
    ligand_index_to_name = {v: k for k, v in ligand_name_to_index.items()}
    receptor_index_to_name = {v: k for k, v in receptor_name_to_index.items()}
    # get name from index
    get_vertex_name = lambda v: ligand_index_to_name.get(v, receptor_index_to_name.get(v, None))

    plot_interactions_network_components_style(g, ligand_name_to_index, receptor_name_to_index, get_vertex_name, network_plot_path)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--interactions_with_principal_agonists_path", type=pathlib.Path, required=True)
    PARSER.add_argument("--network_plot_path", type=pathlib.Path, required=True)
    ARGS = PARSER.parse_args()

    run_main(ARGS.interactions_with_principal_agonists_path,
             ARGS.network_plot_path)
    
