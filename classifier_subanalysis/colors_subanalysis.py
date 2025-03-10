"""
AF2 (no templates)              Peptriever
AF2 APPRAISE (no templates)     RF-AA
AF2 LIS (no templates)          RF-AA APPRAISE
AF2 RIA energy                  RF-AA RIA energy
AF2 RIA sc                      RF-AA RIA sc

"""
# sns uses rgb values between 0 and 1
COLOR = {
    # AF2
    "AF2 (no templates)": "#008FD7",
    "AF2 (no templates) APPRAISE": "#008FD7",
    "AF2 (no templates) LIS": "#008FD7",
    'AF2 (no templates) LIS 1m' :  "#008FD7",
    "AF2 (no templates) RIA energy": "#008FD7",
    "AF2 (no templates) RIA sc": "#008FD7",
    'AF2 (no templates) DeepRank-GNN-esm': "#008FD7",
    'AF2 (no templates) GNN-DOVE' : "#008FD7",
    
    # RF-AA
    "RF-AA": "#A676D6",
    "RF-AA APPRAISE": "#A676D6",
    "RF-AA RIA energy": "#A676D6",
    "RF-AA RIA sc": "#A676D6",
    "RF-AA DeepRank-GNN-esm": "#A676D6",
    "RF-AA GNN-DOVE": "#A676D6",

    # AF3
    "AF3": "#061F4A",
    "AF3 APPRAISE": "#061F4A",
    "AF3 RIA energy": "#061F4A",
    "AF3 RIA sc": "#061F4A",
    "AF3 DeepRank-GNN-esm": "#061F4A",
    "AF3 GNN-DOVE": "#061F4A",
    "AF3 LIS" : "#061F4A",

    # Chai-1
    "Chai-1": "#855e40",
    "Chai-1 APPRAISE": "#855e40",
    "Chai-1 RIA energy": "#855e40",
    "Chai-1 RIA sc": "#855e40",
    "Chai-1 DeepRank-GNN-esm": "#855e40",
    "Chai-1 GNN-DOVE": "#855e40",

    # "ColabFold (no MSAs)": "#5b616b",
    # "ColabFold (no MSAs) LIS": "#5b616b",
    #"Peptriever": "#9E005D",
}


BASE_MARKER = None
APPRAISE_MARKER = '|'
RIA_ENERGY_MARKER = '2'
RIA_SC_MARKER = '3'
LIS_MARKER = '+'
DEEPRANK_MARKER = 'x'
GNN_DOVE_MARKER = '_'

MARKER = dict()
for M in COLOR.keys():
    if "APPRAISE" in M:
        MARKER[M] = APPRAISE_MARKER
    elif "RIA energy" in M:
        MARKER[M] = RIA_ENERGY_MARKER
    elif "RIA sc" in M:
        MARKER[M] = RIA_SC_MARKER
    elif "LIS" in M:
        MARKER[M] = LIS_MARKER
    elif "DeepRank" in M:
        MARKER[M] = DEEPRANK_MARKER
    elif "GNN-DOVE" in M:
        MARKER[M] = GNN_DOVE_MARKER
    else:
        MARKER[M] = BASE_MARKER

DEFAULT_STYLE="--"
RESCORING_STYLE=":"
STYLE = dict()
for M in COLOR.keys():
    if "APPRAISE" in M:
        STYLE[M] = RESCORING_STYLE
    elif "RIA energy" in M:
        STYLE[M] = RESCORING_STYLE
    elif "RIA sc" in M:
        STYLE[M] = RESCORING_STYLE
    else:
        STYLE[M] = DEFAULT_STYLE
        