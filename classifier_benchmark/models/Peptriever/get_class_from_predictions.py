"""
1. read predictions
2. get identifiers
3. get gpcr class

"""
import pathlib
import pandas as pd


def get_gpcr_list_info():
    # gpcr,name,accession,receptor_class,receptor_family,ligand_type,subfamily,endogenous_ligands,species
    script_dir = pathlib.Path(__file__).parent
    gpcr_list = script_dir.parent.parent / "gpcr_list_human.csv"
    gpcr_list = pd.read_csv(gpcr_list)
    return gpcr_list


def get_gpcr_class(gpcr, gpcr_info):
    gpcr_info = gpcr_info[gpcr_info["gpcr"] == gpcr]
    results = gpcr_info['receptor_class'].values
    assert len(results) > 0, f'No class found for {gpcr}'
    assert len(set(results)) == 1, f'Multiple classes found, {results}'
    return gpcr_info["receptor_class"].values[0]



def main():
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / "predictions.csv"
    df = pd.read_csv(df)
    gpcr_info = get_gpcr_list_info()
    
    df['gpcr'] = df['identifier'].apply(lambda x: x.split("___")[0])
    df['gpcr_class'] = df['gpcr'].apply(lambda x: get_gpcr_class(x, gpcr_info))

    print(df['gpcr_class'].value_counts())
    

if __name__ == "__main__":
    main()
