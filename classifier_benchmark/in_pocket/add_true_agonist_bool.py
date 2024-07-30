import pathlib
import pandas


def get_ground_truth_df():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df_p = (
        script_dir.parent.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    df = pandas.read_csv(df_p)

    # Original Target,Decoy Rank,Target Similarity to Original Target,Ligand Sequence,GPCR Sequence,Identifier,Target ID,Decoy ID,Acts as agonist,Decoy Type
    # mtlr_human,0.0,16.0,FVPIFTYGELQRMQEKERNKGQ,MGNCLHRAELSPSTENSSQLDFEDVWNSSYGVNDSFPDGDYGANLEAAAPCHSCNLLDDSALPFFILTSVLGILASSTVLFMLFRPLFRWQLCPGWPVLAQLAVGSALFSIVVPVLAPGLGSTRSSALCSLGYCVWYGSAFAQALLLGCHASLGHRLGAGQVPGLTLGLTVGIWGVAALLTLPVTLASGASGGLCTLIYSTELKALQATHTVACLAIFVLLPLGLFGAKGLKKALGMGPGPWMNILWAWFIFWWPHGVVLGLDFLVRSKLLLLSTCLAQQALDLLLNLAEALAILHCVATPLLLALFCHQATRTLLPSLPLPEGWSSHLDTLGSKS,ackr1_human___1458,ackr1_human,1458,False,Dissimilar
    # nmur2_human,1.0,16.0,FRVDEEFQSPFASQSRGYFLFRPRN,MGNCLHRAELSPSTENSSQLDFEDVWNSSYGVNDSFPDGDYGANLEAAAPCHSCNLLDDSALPFFILTSVLGILASSTVLFMLFRPLFRWQLCPGWPVLAQLAVGSALFSIVVPVLAPGLGSTRSSALCSLGYCVWYGSAFAQALLLGCHASLGHRLGAGQVPGLTLGLTVGIWGVAALLTLPVTLASGASGGLCTLIYSTELKALQATHTVACLAIFVLLPLGLFGAKGLKKALGMGPGPWMNILWAWFIFWWPHGVVLGLDFLVRSKLLLLSTCLAQQALDLLLNLAEALAILHCVATPLLLALFCHQATRTLLPSLPLPEGWSSHLDTLGSKS,ackr1_human___1470,ackr1_human,1470,False,Dissimilar
    # ednra_human,2.0,21.0,CSCSSLMDKECVYFCHLDIIW,MGNCLHRAELSPSTENSSQLDFEDVWNSSYGVNDSFPDGDYGANLEAAAPCHSCNLLDDSALPFFILTSVLGILASSTVLFMLFRPLFRWQLCPGWPVLAQLAVGSALFSIVVPVLAPGLGSTRSSALCSLGYCVWYGSAFAQALLLGCHASLGHRLGAGQVPGLTLGLTVGIWGVAALLTLPVTLASGASGGLCTLIYSTELKALQATHTVACLAIFVLLPLGLFGAKGLKKALGMGPGPWMNILWAWFIFWWPHGVVLGLDFLVRSKLLLLSTCLAQQALDLLLNLAEALAILHCVATPLLLALFCHQATRTLLPSLPLPEGWSSHLDTLGSKS,ackr1_human___989,ackr1_human,989,False,Dissimilar

    # rename 'Identifier' to 'identifier'
    df = df.rename(columns={"Identifier": "identifier"})

    return df


def is_agonist(identifier, ground_truth_df) -> bool:
    """Check if the identifier is an agonist"""
    assert "identifier" in ground_truth_df.columns
    assert "Acts as agonist" in ground_truth_df.columns

    assert (
        len(ground_truth_df[ground_truth_df["identifier"] == identifier]) == 1
    ), f"identifier {identifier} not found in ground_truth_df"

    return ground_truth_df[ground_truth_df["identifier"] == identifier][
        "Acts as agonist"
    ].values[0]


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = pandas.read_csv(script_dir / "in_pocket_results.csv")
    # model,identifier,shortest_distance
    # ESMFold,vipr2_human___1152,6.243615627288818
    # ESMFold,ccr6_human___2257,34.36741638183594
    # ESMFold,ssr5_human___3700,36.4244384765625

    # goal is to add a new column 'agonist' to the dataframe
    out_p = script_dir / "distances.csv"
    ground_truth_df = get_ground_truth_df()
    df["agonist"] = df["identifier"].apply(lambda x: is_agonist(x, ground_truth_df))
    df.to_csv(out_p, index=False)


if __name__ == "__main__":
    run_main()
