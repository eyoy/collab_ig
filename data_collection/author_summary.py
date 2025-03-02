import os
import json
import pandas as pd



brands = [i for i in os.listdir('/mnt/f/ig/meta_new/') if not (i.endswith('.json') | i.startswith('.'))]
root_path = '/mnt/f/ig/meta_new/'
brands = ['maccosmetics']
for b in brands:
    print(b, brands.index(b))
    # if os.path.exists(f'/mnt/f/ig/author_summary/{b}.csv'):
    #     print("Brand has existed")
    #     continue
    # else:
    files = [i for i in os.listdir(f'/mnt/f/ig/meta_new/{b}') if not i.startswith('.')]
    author_list = []
    ids = []
    create_dates = []
    meta_files = []
    for dirpath, dirnames, filenames in os.walk(root_path+b):
            for filename in filenames:
                if not filename.startswith('.'):
                # This will give you the full path to the file
                    file_path = os.path.join(dirpath, filename)
                    meta_files.append(file_path)
    bad_f = []
    for file in meta_files:
        print(file)
        with open(file, 'r') as f:
            df = json.load(f)
        if not bool(df):
            pass
        elif ('status' in df.keys()) & ('message' in df.keys()):
            authors = None
            create_date = None
            author_list.append(authors)
            ids.append(file)
        else:
            try:
                authors = len(df['coauthor_producers'])
                author_list.append(authors)
                ids.append(file)
                #create_dates.append(df['taken_at_timestamp'])
            except:
                try:
                    authors = len(df['data']['shortcode_media']['coauthor_producers'])
                    author_list.append(authors)
                    ids.append(file)
                except:
                    try:
                        authors = len(df['invited_coauthor_producers'])
                        author_list.append(authors)
                        ids.append(file)
                    except:
                        authors = None
                        author_list.append(authors)
                        ids.append(file)
    final = pd.DataFrame(zip(ids, author_list), columns = ['file', 'authors'])
    final.to_csv(f'/mnt/f/ig/author_summary/{b}.csv', index=False)
    print('Success', b)