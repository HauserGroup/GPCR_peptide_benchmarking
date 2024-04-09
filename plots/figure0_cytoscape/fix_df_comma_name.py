import pathlib
import pandas as pd

# get dir of this script
dirpath = pathlib.Path(__file__).parent.absolute()
csv_old = dirpath / "4_principal_agonists_interactions.csv"
csv_new = dirpath / "4_principal_agonists_interactions_fix_commas.csv"

# read old csv
df = pd.read_csv(csv_old)

# replace commas that are WITHIN a cell with a ";"
df = df.replace({",": ";"}, regex=True)

# in the "Target ID" column, replace "_human" with ""
df["Target GPCRdb ID"] = df["Target GPCRdb ID"].str.replace("_human", "")

df.to_csv(csv_new, index=False)
print(f"Fixed commas in {csv_old} and saved to {csv_new}")
