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

    "Peptriever": "#9E005D",
}

# add markers to the rescoring tools (scatterplot). Default = 'o'
MARKER = {
    "RF-AA": ".",
    "RF-AA APPRAISE": "^",
    "RF-AA RIA energy": "P",
    "RF-AA RIA sc": "d",
    
    "AF2 (no templates)": ".",
    "AF2 APPRAISE (no templates)": "^",
    "AF2 RIA energy (no templates)": "P",
    "AF2 RIA sc (no templates)": "d",
    # LIS is only for AF2
    "AF2 LIS (no templates)": "X",

    'AF2 LIS (no templates) 1m' : 'X', 

    "Peptriever": ".",
}