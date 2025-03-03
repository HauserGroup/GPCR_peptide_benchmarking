"""
AF2 (no templates)              Peptriever
AF2 APPRAISE (no templates)     RF-AA
AF2 LIS (no templates)          RF-AA APPRAISE
AF2 RIA energy                  RF-AA RIA energy
AF2 RIA sc                      RF-AA RIA sc

"""
# sns uses rgb values between 0 and 1
COLOR = {
    "RF-AA": "#A676D6",
    "RF-AA APPRAISE": "#A676D6",
    "RF-AA RIA energy": "#A676D6",
    "RF-AA RIA sc": "#A676D6",
    
    "AF2 (no templates)": "#008FD7",
    "AF2 APPRAISE (no templates)": "#008FD7",
    "AF2 LIS (no templates)": "#008FD7",
    'AF2 LIS (no templates) 1m' :  "#008FD7",
    "AF2 RIA energy (no templates)": "#008FD7",
    "AF2 RIA sc (no templates)": "#008FD7",
    'AF2 (no templates) DeepRank-GNN-esm': "#008FD7",

    # new color for AF3
    "AF3_local" : "#FF7F0E",

    "Peptriever": "#9E005D",

    "ColabFold (no MSAs)": "#5b616b",
    "ColabFold (no MSAs) LIS": "#5b616b",
}

# add markers to the rescoring tools (scatterplot). Default = 'o'
# BASE_MARKER = 'd'
# MARKER = {
#     "RF-AA":BASE_MARKER,
#     "RF-AA APPRAISE": "^",
#     "RF-AA RIA energy": "P",
#     "RF-AA RIA sc": "d",
    
#     "AF2 (no templates)": BASE_MARKER,
#     "AF2 APPRAISE (no templates)": "^",
#     "AF2 RIA energy (no templates)": "P",
#     "AF2 RIA sc (no templates)": "d",

#     # LIS is only for AF2
#     "AF2 LIS (no templates)": "X",
#     'AF2 LIS (no templates) 1m' : 'X', 

#     "Peptriever": BASE_MARKER,
# }


BASE_MARKER = None
APPRAISE_MARKER = '|'
RIA_ENERGY_MARKER = '2'
RIA_SC_MARKER = '3'
LIS_MARKER = '+'
DEEPRANK_MARKER = 'x'

MARKER = {
    "RF-AA":BASE_MARKER,
    "RF-AA APPRAISE": APPRAISE_MARKER,
    "RF-AA RIA energy": RIA_ENERGY_MARKER,
    "RF-AA RIA sc": RIA_SC_MARKER,
    
    "AF2 (no templates)": BASE_MARKER,
    "AF2 APPRAISE (no templates)": APPRAISE_MARKER,
    "AF2 RIA energy (no templates)": RIA_ENERGY_MARKER,
    "AF2 RIA sc (no templates)": RIA_SC_MARKER,
    'AF2 (no templates) DeepRank-GNN-esm': DEEPRANK_MARKER,

    "AF3_local" : BASE_MARKER,

    # LIS is only for AF2
    "AF2 LIS (no templates)": LIS_MARKER,
    'AF2 LIS (no templates) 1m' : LIS_MARKER,

    "Peptriever": BASE_MARKER,

    # ColabFold
    "ColabFold (no MSAs)": BASE_MARKER,
    "ColabFold (no MSAs) LIS": LIS_MARKER,
}


DEFAULT_STYLE="--"
RESCORING_STYLE=":"
STYLE = {
    "RF-AA":DEFAULT_STYLE,
    "RF-AA APPRAISE": RESCORING_STYLE,
    "RF-AA RIA energy": RESCORING_STYLE,
    "RF-AA RIA sc": RESCORING_STYLE,

    "AF2 (no templates)": DEFAULT_STYLE,
    "AF2 APPRAISE (no templates)": RESCORING_STYLE,
    "AF2 RIA energy (no templates)": RESCORING_STYLE,
    "AF2 RIA sc (no templates)": RESCORING_STYLE,
    'AF2 (no templates) DeepRank-GNN-esm': RESCORING_STYLE,

    "AF3_local" : DEFAULT_STYLE,

    # LIS is only for AF2
    "AF2 LIS (no templates)": RESCORING_STYLE,
    'AF2 LIS (no templates) 1m' : RESCORING_STYLE,

    "Peptriever": DEFAULT_STYLE,

    # ColabFold
    "ColabFold (no MSAs)": DEFAULT_STYLE,
    "ColabFold (no MSAs) LIS": RESCORING_STYLE,
}