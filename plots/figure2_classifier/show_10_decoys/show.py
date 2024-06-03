"""Create show.pm"""

import pathlib
import pandas as pd
import sys
import numpy as np

sys.path.append(".")
from colors import COLOR, hex_to_rgb


def get_decoy_df():
    script_dir = pathlib.Path(__file__).parent.absolute()
    decoy_p = (
        script_dir.parent.parent.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    decoy_df = pd.read_csv(decoy_p)
    return decoy_df


def write_ray_settings(f):
    settings = """set ray_trace_mode, 1
    set ray_trace_gain, 0.1
    set ray_shadows, 1
    set ray_trace_fog, 0
    set antialias, 2
    set ambient, 0.2  # Reduced ambient light for darker overall image
    set reflect, 0.3  # Slightly reduced reflectivity
    set specular, 0.5  # Reduced specularity for less shiny surfaces
    set shininess, 10
    set depth_cue, 1
    set ray_opaque_background, off

    # Ambient Occlusion settings
    set ray_trace_depth_factor, 0.6
    set ray_trace_disco, 1.3
    set ray_trace_shadow, 1

    # Light settings - adjusted for a darker effect
    set light_count, 8
    set light2, -0.3, 0.5, 1
    set light3, 0.5, -0.5, 0.6  # Reduced intensity
    set light4, -0.8, 0.3, 0.3  # Reduced intensity
    set light5, 0.5, 0.5, 0.5   # Reduced intensity
    set light6, 0.3, -0.7, 0.3
    set light7, 0.5, 0.5, -0.5
    set light8, -0.5, -0.5, 0.5

    # settings to make the receptor look more like chimerax
    set cartoon_side_chain_helper, 1
    set cartoon_tube_radius, 0.4
    set cartoon_tube_width, 1.0
    set orthoscopic, on
    set ray_trace_mode, 1
    set ray_shadows, 0
    """
    f.write(settings + "\n")


def set_view(f):
    view = """### cut below here and paste into script ###
    set_view (\
        0.846652448,    0.043910827,   -0.530334532,\
        -0.092061721,    0.993649125,   -0.064698182,\
        0.524124205,    0.103599437,    0.845313013,\
        0.000000000,   -8.000000000, -308.572143555,\
        1.567100525,   -6.109443665,   -5.748374939,\
    -179078.390625000, 179695.531250000,   20.000000000 )
    ### cut above here and paste into script ###
    """
    f.write(view + "\n")


def create_show_py():
    script_dir = pathlib.Path(__file__).parent.absolute()
    out_p = script_dir / "show.pm"
    model_dir = script_dir / "models"
    models = [m for m in model_dir.iterdir()]
    models = [m for m in models if m.is_file() and m.suffix == ".pdb"]
    short_names = [m.stem.replace("_human", "") for m in models]
    short_names = [m.replace("___", "_") for m in short_names]

    decoy_df = get_decoy_df()
    # make "Identifier" short
    gpcr = "glr"
    decoy_df["Identifier"] = decoy_df["Identifier"].str.replace("_human", "")
    decoy_df["Identifier"] = decoy_df["Identifier"].str.replace("___", "_")
    decoy_df = decoy_df[decoy_df["Identifier"].str.contains(gpcr)]
    # get principal agonist
    principal_agonist = decoy_df[decoy_df["Decoy Type"] == "Principal Agonist"]
    principal_agonist = principal_agonist["Identifier"].values[0]

    # get decoy types for each model
    id_to_rank = {}
    for i, row in decoy_df.iterrows():
        if np.isnan(row["Decoy Rank"]):
            id_to_rank[row["Identifier"]] = f"{row['Decoy Type']}"
        else:
            id_to_rank[row["Identifier"]] = (
                f"{row['Decoy Type']}{int(row['Decoy Rank'])}"
            )

    gpcr_type = "cartoon"
    transparency = 0.5

    with open(out_p, "w") as f:
        f.write("reinitialize\n")
        # load all
        for name, model in zip(short_names, models):
            f.write(f"load {model}, {name}\n")
            # color by decoy type
            rank = id_to_rank[name]
            color = COLOR.get(rank)
            color = hex_to_rgb(color)
            # create custom color
            f.write(f"set_color {rank}, {color}\n")
            # color chain A gray80
            f.write(f"color grey80, {name} and chain B\n")
            # color chain B
            f.write(f"color {rank}, {name} and chain C\n")

        # align to PA
        for name, model in zip(short_names, models):
            f.write(
                f"align {name} and chain B and resi 50-350, {principal_agonist} and chain B and resi 50-350\n"
            )

        # f.write(f"hide {gpcr_type}, chain B and resi 1-50\n")
        f.write(f"hide {gpcr_type}, chain B and resi 440-700\n")

        # write ray settings
        ray_script = script_dir.parent.parent.parent / "ray.pm"
        f.write(f"@{ray_script.resolve()}\n")
        set_view(f)

        # set background white
        f.write("bg_color white\n")
        f.write("hide cartoon, chain B\n")
        # set transparency
        f.write(f"set {gpcr_type}_transparency, {transparency}, chain B\n")
        f.write(f"show {gpcr_type}, chain B\n")

        for name, model in zip(short_names, models):
            if name != principal_agonist:
                f.write(f"hide {gpcr_type}, {name} and chain B\n")

        # ray
        f.write("ray 800, 800\n")
        # save
        f.write(f"save {script_dir}/show.png\n")

    # also plot the scores
    print(decoy_df)


if __name__ == "__main__":
    create_show_py()
