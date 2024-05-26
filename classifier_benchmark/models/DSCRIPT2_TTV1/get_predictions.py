import pathlib
import pandas


def run_main():
    script_dir = pathlib.Path(__file__).parent
    df = pandas.read_csv(script_dir / "scores.csv")
    out_p = script_dir / "predictions.csv"

    # keep only "identifier" and "InteractionProbability" columns
    df = df[["identifier", "InteractionProbability"]]
    df.to_csv(out_p, index=False)


if __name__ == "__main__":
    run_main()
