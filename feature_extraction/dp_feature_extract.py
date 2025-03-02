from deepface import DeepFace
import os
import pandas as pd
import random
import json
# Using mp env

save_path = '/mnt/e/erya/collab_posts_ig/images'

brands = [i.split('.')[0] for i in os.listdir('/mnt/e/erya/collab_posts_ig/id_2021_2024')]
brands = brands[179:]

for b in brands:
    with open('/mnt/e/erya/collab_posts_ig/id_2021_2024/{}.json'.format(b)) as f:
        goodids = json.load(f)
    print(len(goodids))
    jpg_files = []
    for root, dirs, files in os.walk("/mnt/e/erya/collab_posts_ig/media/{}".format(b), topdown=False):
        for name in files:
            if not name.startswith('.') and name.endswith('.jpg'):
                #print(name)
                #print(os.path.join(root, name))
                jpg_files.append(os.path.join(root, name))

    todo = [i for i in jpg_files if i.split('/')[-2] in goodids]
    print(b, len(todo))
    if not os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}/deepface".format(b)):
        os.makedirs("/mnt/e/erya/collab_posts_ig/image/{}/deepface".format(b))
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}/deepface".format(b),  " Created ")
    else:
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}/deepface".format(b),  " already exists")
    failed= []
    for f in todo:
        print("Starting ... {}".format(f))
        name = f.split('/')[-1].split('.')[0]
        if os.path.exists('/mnt/e/erya/collab_posts_ig/image/{}/deepface/{}.json'.format(b,name)):
            print("Already done ")
        else:
            print("Processing ...")
            try:
                res = DeepFace.analyze(img_path = f, 
                actions = ['age', 'gender', 'race', 'emotion'])
                with open('/mnt/e/erya/collab_posts_ig/image/{}/deepface/{}.json'.format(b,name), 'w') as f:
                    json.dump(res, f)
                print("Successfully saved to " + os.path.join(save_path,'{}.csv'.format(name)))
            except:
                print("NO face is successfully identified!")
                failed.append(f)
            
    with open('/mnt/e/erya/collab_posts_ig/image/{}/deepface/failed.json'.format(b), 'w') as f:
        json.dump(failed, f)