import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import textdescriptives as td
import spacy

from textdescriptives.utils import load_sms_data



path = '/mnt/e/erya/collab_posts_ig/post_summary'

for i in os.listdir(path)[209:]:
    print(i)
    if i.endswith('.csv') and not i.startswith('.'):
        df = pd.read_csv(os.path.join(path, i), lineterminator='\n')
        df['brands'] = i.split('.csv')[0]
        df['description'] = df['description'].astype(str)
        metrics = td.extract_metrics(
            text=df["description"],spacy_model="en_core_web_sm", metrics=None)
        metrics_df = df.join(metrics.drop(columns=["text"]))
        metrics_df.to_csv(os.path.join(path, i), index=False)
        print('done', i, os.listdir(path).index(i), 'out of', len(os.listdir(path)))
        