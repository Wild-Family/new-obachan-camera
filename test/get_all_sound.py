import os, sys
sys.path.append(os.getcwd())
import dialogue
import pandas as pd


csv_path = "./audio/dialogue.csv"
df = pd.read_csv(csv_path, index_col=0)
for index, row in df.iterrows():
        dialogue.request_aitalk(row['dialogue'], row['filename'])