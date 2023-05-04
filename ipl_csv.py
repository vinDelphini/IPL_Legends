import pandas as pd

df = pd.read_csv(r'ipl.csv')


SCORE_MAPPING = {
    1: 200,
    2: 190,
    3: 180,
    4: 170,
    5: 160,
    6: 150,
    7: 140,
    0: 140,
}

# for i in df.score:
#     if i in SCORE_MAPPING.keys():
        

