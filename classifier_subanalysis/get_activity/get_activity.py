""" """

import pathlib
import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns

# append parent dir for imports
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
sys.path.append(".")
from parse_predictions import get_gpcr_class
from colors import COLOR


def get_activity_df() -> pd.DataFrame:
    """
    return columns:
    'Target GPCRdb ID', 'Peptide Sequence', 'Target ID', 'Ligand ID', 'Interaction parameter', 'Interaction units']
    """
    script_dir = pathlib.Path(__file__).parent
    # load the data
    activity_p = f"{script_dir.parent.parent}/classifier_benchmark_data/output/3b_experimental_values.csv"
    activity_df = pd.read_csv(activity_p)
    return activity_df


def get_decoy_df() -> pd.DataFrame:
    """
    return columns:
    'Original Target', 'Decoy Rank', 'Target Similarity to Original Target',
    'Ligand Sequence', 'GPCR Sequence', 'Identifier', 'Target ID',
    'Decoy ID', 'Acts as agonist', 'Decoy Type'
    """
    script_dir = pathlib.Path(__file__).parent
    # load the data
    decoy_p = f"{script_dir.parent.parent}/classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    decoy_df = pd.read_csv(decoy_p)
    return decoy_df


def get_activity_rows_for_pair(gpcr_id, ligand_id, activity_df):
    # match "Target ID" and "Ligand ID"
    return activity_df[
        (activity_df["Target GPCRdb ID"] == gpcr_id)
        & (activity_df["Ligand ID"] == ligand_id)
    ]


def fix_activity_value(activity_value):
    """
    examples:
    nan
    10.0|8.5|9.4|7.9|9.3|8.9
    7.3
    '9.6 - 10.0'
    ['9.7 - 10.0', '6.5 - 6.8']

    ----------------
    nan stays nan
    string with multiple values separated by "|", return mean
    string with "-" indicating a range, return mean
    string with multiple ranges, return mean of all ranges
    string with single value, return float
    """
    if pd.isna(activity_value):
        return activity_value
    # if it is a non na float
    elif isinstance(activity_value, float):
        return activity_value
    # if it is a string
    elif not isinstance(activity_value, str):
        raise NotImplementedError(f"Unexpected type: {type(activity_value)}")
    elif isinstance(activity_value, str):
        # first get all the individual values
        values = activity_value.split("|")
        for i, v in enumerate(values):
            # if it is a range
            if "-" in v:
                range_values = v.split("-")
                range_values = [float(rv) for rv in range_values]
                values[i] = sum(range_values) / len(range_values)
            else:
                values[i] = float(v)
        mean = sum(values) / len(values)
        logging.info(f"Got mean activity: {mean} for {activity_value}")
        return mean


def get_parameter_dfs(
    principal_agonists: pd.DataFrame, activity_df: pd.DataFrame, parameter: str
):
    """Get all the activity values for a given parameter for each principal agonist
    Returns a df with columns: 'identifier', 'activity'
    """
    # empty output df
    parameter_df = pd.DataFrame(columns=["identifier", "mean_activity"])
    logging.info(f"Getting activity for parameter: {parameter}")
    # init all identifiers with nan
    parameter_df["identifier"] = principal_agonists.apply(
        lambda x: f"{x['Target ID']}___{x['Decoy ID']}", axis=1
    )
    parameter_df.set_index("identifier", inplace=True)

    # for each row
    for i, (absolute_i, pa) in enumerate(principal_agonists.iterrows()):
        # get identifier
        gpcr_id = pa["Target ID"]
        ligand_id = pa["Decoy ID"]
        identifier = f"{gpcr_id}___{ligand_id}"
        logging.info(
            f"Processing interaction {i}/{len(principal_agonists)}, GPCR: {gpcr_id}, Ligand: {ligand_id}"
        )

        # get the activity rows for this pair
        activity_rows = get_activity_rows_for_pair(gpcr_id, ligand_id, activity_df)
        activity_rows = activity_rows[
            activity_rows["Interaction parameter"] == parameter
        ]
        assert len(activity_rows) == 1, f"Expected 1 row, got {len(activity_rows)}"

        # parse the activity value
        activity_value = activity_rows["Interaction units"].values[0]
        activity_value = fix_activity_value(activity_value)

        # set the activity value
        parameter_df.loc[identifier, "mean_activity"] = activity_value

    # set identifier as index

    return parameter_df


def plot_mean_activity(title: str, parameter_df: pd.DataFrame, plot_p: pathlib.Path):
    """small scatter plot, with identifier and mean_activity
    also show nans
    """
    # figsize 8,4
    plt.figure(figsize=(8, 4))
    # sort
    parameter_df = parameter_df.copy()
    parameter_df.sort_values("mean_activity", inplace=True)
    # nan percent
    nan_count = parameter_df["mean_activity"].isna().sum()
    non_nan_count = len(parameter_df) - nan_count
    nan_percent = nan_count / len(parameter_df) * 100
    # assert there are no natural 0 values
    assert not (parameter_df["mean_activity"] == 0).any()
    # if nan, replace with zero. Do NOT use fillna(0) as it will replace all nans
    parameter_df["mean_activity"] = parameter_df["mean_activity"].apply(
        lambda x: 0 if pd.isna(x) else x
    )
    # replace _human in identifier
    parameter_df.index = parameter_df.index.str.replace("_human", "")
    # plot
    title = f"{title}, {nan_percent:.2f}% nans"
    # calculate count of nans and non-nans
    title = f"{title},\n{non_nan_count} non-nans"

    sns.scatterplot(data=parameter_df, x="identifier", y="mean_activity")
    plt.title(title)
    # rotate x labels
    plt.xticks(rotation=90, fontsize=6)
    # add padding for x labels
    plt.tight_layout()
    plt.xlim(-0.5, len(parameter_df) - 0.5)
    plt.savefig(plot_p)
    plt.close()


def plot_nan_ratio_per_class(
    title: str, parameter_df: pd.DataFrame, plot_p: pathlib.Path
):
    """ """
    # plot a piechart for each unique class
    classes = parameter_df["class"].unique()
    plt.subplots(len(classes), 1, figsize=(8, 8))

    for i, c in enumerate(classes):
        class_df = parameter_df[parameter_df["class"] == c]
        nan_count = class_df["mean_activity"].isna().sum()
        non_nan_count = len(class_df) - nan_count
        plt.subplot(len(classes), 1, i + 1)
        plt.pie(
            [nan_count, non_nan_count],
            labels=["nans", "non-nans"],
            colors=["red", "green"],
            # show absolute counts in pie chart
            autopct=lambda p: "{:.0f}".format(p * len(class_df) / 100),
        )

        nan_percent = nan_count / len(class_df) * 100
        plt.title(f"{c}, {nan_percent:.2f}% nans")
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(plot_p)
    plt.close()


def plot_pKi(parameter_df: pd.DataFrame, plot_p: pathlib.Path):
    """ """
    # get classes
    parameter_df = parameter_df.copy()
    parameter_df = parameter_df.sort_values("mean_activity")
    classes = parameter_df["class"].unique()
    class_colors = {c: COLOR[c] for c in classes}
    # plot
    plt.figure(figsize=(4, 4))
    sns.scatterplot(
        data=parameter_df,
        x="identifier",
        y="mean_activity",
        hue="class",
        palette=class_colors,
        # make the points bigger
        s=50,
        # outline the points
        edgecolor="black",
        # draw contour lines
        linewidth=0.5,
    )
    # move legend to bottom right
    plt.legend(loc="lower right")
    plt.title("Binding affinity")
    plt.ylabel("mean pKi")
    plt.xlabel("")
    plt.xticks(rotation=90)
    plt.xticks([])
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(plot_p)
    plt.close()


def run_main():
    # load data
    activity_df = get_activity_df()
    decoy_df = get_decoy_df()
    script_dir = pathlib.Path(__file__).parent
    log_p = script_dir / "activity.log"

    # setup logging with times
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="w",
        filename=log_p,
    )

    # get principal agonists from decoy_df
    principal_agonists = decoy_df[decoy_df["Acts as agonist"].astype(int) == 1]
    gpcrs = principal_agonists["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}

    # from activity df, print types of interactions for each principal agonist
    counts = activity_df["Interaction parameter"].value_counts()
    parameters = counts.keys()
    logging.info(f"Interaction parameters: {parameters}")

    for parameter in parameters:
        parameter_df = get_parameter_dfs(principal_agonists, activity_df, parameter)
        # add class
        parameter_df["class"] = (
            parameter_df.index.str.split("___").str[0].map(gpcr_to_class_dict)
        )
        # with nans
        plot_mean_activity(parameter, parameter_df, script_dir / f"{parameter}.png")
        plot_nan_ratio_per_class(
            parameter, parameter_df, script_dir / f"{parameter}_nan_ratio.png"
        )

        # save df
        parameter_df.to_csv(script_dir / f"{parameter}.csv", index=True)
        # create better plot for pKi
        if parameter == "pKi":
            plot_pKi(parameter_df.dropna(), script_dir / f"{parameter}_scale.png")

    logging.info("Done")


if __name__ == "__main__":
    run_main()
