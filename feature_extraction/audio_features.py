import opensmile
import os
import pandas as pd
#use tf-ws env

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.emobase,
    feature_level=opensmile.FeatureLevel.Functionals,
)
brands = [i.split('.')[0] for i in os.listdir('/mnt/e/erya/collab_posts_ig/id_2021_2024')]
for b in brands:
    if not os.path.exists("/mnt/e/erya/collab_posts_ig/video/audio_features/{}".format(b)):
        os.makedirs("/mnt/e/erya/collab_posts_ig/video/audio_features/{}".format(b))
        print("Directory ", "/mnt/e/erya/collab_posts_ig/video/audio_features/{}".format(b),  " Created ")
    else:
        print("Directory ", "/mnt/e/erya/collab_posts_ig/video/audio_features/{}".format(b),  " already exists")
    mp3_files = []
    for root, dirs, files in os.walk("/mnt/e/erya/collab_posts_ig/video/audio/{}".format(b), topdown=False):
        for name in files:
            if not name.startswith('.') and name.endswith('.mp3'):
                #print(name)
                #print(os.path.join(root, name))
                mp3_files.append(os.path.join(root, name))
    failed= []
    for m in mp3_files:
        print(m, 'Processing')
        y = smile.process_file(m)
        y.to_csv("/mnt/e/erya/collab_posts_ig/video/audio_features/{}/{}.csv".format(b, m.split('/')[-1].split('.')[0]))