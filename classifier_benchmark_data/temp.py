import pandas as pd 
import csv 
import requests
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

def get_GPCRdb_receptor_data(receptor_id):
    """
    Returns a dict that contains the information for a GPCR receptor
           with these keys:
            'entry_name', 'name', 'accession', 'family', 'genes',
            'species', 'source', 'residue_numbering_scheme', 'sequence'

    example:  get_GPCRdb_receptor_data('nk2r_human')
    """
    # fetch a protein
    url = f'https://gpcrdb.org/services/protein/{receptor_id}/'
    response = requests.get(url)
    protein_data = response.json()
    return protein_data


def get_fam_html(fam_id):
    """
    """
    url = f"https://gpcrdb.org/family/{fam_id}/"
    response = requests.get(url)
    fam_html = response.text

    return fam_html


def get_classification_from_html(html):
    """


    find this div:

    <div class="row">
        <div class="col-md-2 text-right text-info">
            <h4>CLASSIFICATION</h4>
        </div>
        <div class="col-md-10">
        Other GPCRs <span class='glyphicon glyphicon-arrow-right' aria-hidden='true'></span> Orphan receptors <span class='glyphicon glyphicon-arrow-right' aria-hidden='true'></span> Other GPCR orphans <span class='glyphicon glyphicon-arrow-right' aria-hidden='true'></span> <i>GPR107</i>
        </div>
    </div>
    """

    soup = BeautifulSoup(html, 'html.parser')

    # Find the div containing the classification
    classification_div = soup.find("div", {"class": "col-md-10"})

    # Extract and print the classification
    classification = classification_div.text.strip()

    return classification


if not os.path.exists("./temp_output.csv"):
    df = pd.read_csv("/Users/kcd635/Documents/GitHub/Interspecies_GPCR_pipeline/classifier_benchmark_data/output/6_interactions_with_decoys.csv")
    # print the lowest binding pocket similarity score for the similar decoys
    df = df[df["Decoy Type"] == "Similar"]
    # sort on similarity score
    df = df.sort_values(by=["Target Similarity to Original Target", "Decoy Rank"], ascending=[True, False])
    df = df.drop_duplicates(subset=["Target ID"])
    df["Family"] = None
    df["Classification"] = None

    for i, row in df.iterrows():
        fam = get_GPCRdb_receptor_data(row["Target ID"])["family"]
        df.at[i, "Family"] = fam
        fam_html = get_fam_html(fam)
        classification = get_classification_from_html(fam_html)
        classification = f"{classification.split('  ')[0]} > {classification.split('  ')[2]}"
        df.at[i, "Classification"] = classification

    # reorder so that classification comes earlier
    df = df[["Original Target", "Target ID", "Classification", "Target Similarity to Original Target", "Decoy ID", "Decoy Rank"]]
    # rename "Target Similarity to Original Target" to the shorter "SimToOrig"
    df = df.rename(columns={"Target Similarity to Original Target": "SimToOrig"})

    df.to_csv('./temp_output.csv')
else:
    df = pd.read_csv("./temp_output.csv")


print(df)
# split classification on " > "
df["Classification"] = df["Classification"].apply(lambda x: x.split(" > ")[1])
# sns scatter plot of Classification vs SimToOrig
sns.scatterplot(data=df, x="Classification", y="SimToOrig")
# set xlim and ylim
plt.ylim(0, 100)
plt.xticks(rotation=75)
plt.tight_layout()
plt.show()



