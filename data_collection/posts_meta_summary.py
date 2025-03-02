import os
import json
import pandas as pd



brands = [i for i in os.listdir('/mnt/f/ig/meta_new/') if not (i.endswith('.json') | i.startswith('.'))]
root_path = '/mnt/f/ig/meta/'
brands = ['jimmychoo',
 'louboutinworld',
 'maxmara',
 'miumiu',
 'myntra',
 'prada',
 'rolex',
 'sergiorossi',
 'stellamccartney',
 'tiffanyandco']
for b in brands:
    print(b, brands.index(b))
    # if os.path.exists(f'/mnt/f/ig/post_summary/{b}.csv'):
    #     print("Brand has existed")
    #     continue
    # else:
        #files = [i for i in os.listdir(f'/Volumes/erya/ig/meta_new/{b}') if not i.startswith('.')]
        
    meta_files = []
    for dirpath, dirnames, filenames in os.walk(root_path+b):
            for filename in filenames:
                if not filename.startswith('.'):
                # This will give you the full path to the file
                    file_path = os.path.join(dirpath, filename)
                    meta_files.append(file_path)
    #bad_f = []
    #author_list = []
    ids = []
    short_code_list = []
    create_dates = []
    likes = []
    comments = []
    description = []
    captions = []
    affiliates = []
    sponsored = []
    ads = []
    for file in meta_files:
        print(file)
        id = file.split('/')[-2]
        shortcode = file.split('/')[-1].split('_',1)[1].split('.')[0]
        try:
            with open(file, 'r') as f:
                df = json.load(f)
        except:
            ids.append(id)
            short_code_list.append(shortcode)
            create_dates.append(None)
            captions.append(None)
            likes.append(None)
            comments.append(None)
            affiliates.append(None)
            sponsored.append(None)
            ads.append(None)
            description.append(None)
        # if not bool(df):
        #     pass
        # elif ('status' in df.keys()) & ('message' in df.keys()):
        #     authors = None
        #     create_date = None
        #     ids.append(id)
        #     short_code_list.append(shortcode)
        #     create_dates.append(None)
        #     likes.append(None)
        #     comments.append(None)
        #     description.append(None)
        # else:
        if 'node' in df.keys():
            #authors = len(df['node']['coauthor_producers'])
            ids.append(id)
            short_code_list.append(shortcode)
            create_dates.append(df['node']['taken_at_timestamp'])
            if 'accessibility_caption' in df['node'].keys():
                captions.append(df['node']['accessibility_caption'])
            else:
                captions.append(None)
            likes.append(df['node']['edge_media_preview_like']['count'])
            comments.append(df['node']['edge_media_to_comment']['count'])
            affiliates.append(None)
            sponsored.append(None)
            ads.append(None)
            if len(df['node']['edge_media_to_caption']['edges']) == 0:
                description.append(None)
            else:
                description.append(df['node']['edge_media_to_caption']['edges'][0]['node']['text'].replace('\r',''))
        else:
            try:
                #authors = len(df['coauthor_producers'])
                ids.append(id)
                short_code_list.append(shortcode)
                create_dates.append(df['taken_at_timestamp'])
                captions.append(df['accessibility_caption'])
                likes.append(df['edge_media_preview_like']['count'])
                comments.append(df['edge_media_to_comment']['count'])
                affiliates.append(df['is_affiliate'])
                sponsored.append(df['is_paid_partnership'])
                ads.append(df['is_ad'])
                description.append(df['edge_media_to_caption']['edges'][0]['node']['text'].replace('\r',''))
            except:
                #authors = len(df['data']['shortcode_media']['coauthor_producers'])
                ids.append(id)
                short_code_list.append(shortcode)
                create_dates.append(df['data']['shortcode_media']['taken_at_timestamp'])
                captions.append(df['data']['shortcode_media']['accessibility_caption'])
                likes.append(df['data']['shortcode_media']['edge_media_preview_like']['count'])
                comments.append(df['data']['shortcode_media']['edge_media_to_comment']['count'])
                affiliates.append(df['data']['shortcode_media']['is_affiliate'])
                sponsored.append(df['data']['shortcode_media']['is_paid_partnership'])
                ads.append(df['data']['shortcode_media']['is_ad'])
                description.append(df['data']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text'].replace('\r',''))
                
    final = pd.DataFrame(zip(ids, short_code_list,create_dates,captions,likes,comments,affiliates,sponsored,ads,description), 
                            columns = ['id', 'shortcode', 'create_date', 'caption', 'likes', 'comments', 'affiliates', 'sponsored', 'ads', 'description'])
    final.to_csv(f'/mnt/f/ig/post_summary/{b}.csv', index=False)
    print('Success', b)