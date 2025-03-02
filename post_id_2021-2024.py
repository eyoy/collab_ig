import os
import pandas as pd
import json

brands = []
for i in os.listdir('/mnt/e/erya/collab_posts_ig/post_summary'):
    #print(i)
    if i.endswith('.csv') and not i.startswith('.'):
        brands.append(i.split('.')[0])

for b in brands:
    df = pd.read_csv('/mnt/e/erya/collab_posts_ig/post_summary/{}.csv'.format(b))
    df['create_date'] = pd.to_datetime(df.create_date, unit='s')
    df = df[df.create_date >='2021-01-01']
    goodids = df['id'].tolist()
    goodids = [str(i) for i in goodids]
    print(len(goodids))
    with open('/mnt/e/erya/collab_posts_ig/id_2021_2024/{}.json'.format(b), 'w') as f:
        json.dump(goodids, f)
    print('Sucessfully saved {}'.format(b))