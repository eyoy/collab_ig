import os
import json
import pandas as pd
import numpy as np
import os
import pandas as pd
import subprocess

brands = [i.split('.')[0] for i in os.listdir('/mnt/e/erya/collab_posts_ig/id_2021_2024')]

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

    if not os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}".format(b)):
        os.makedirs("/mnt/e/erya/collab_posts_ig/image/{}".format(b))
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}".format(b),  " Created ")
    else:
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}".format(b),  " already exists")
    #os.chdir("/mnt/e/erya/collab_posts_ig/image/{}/".format(b))
    if os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}/nima/".format(b)):
        print("nima" + " already done")
    else:
        os.makedirs("/mnt/e/erya/collab_posts_ig/image/{}/nima/".format(b))
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}/nima/".format(b),  " Created ")
    failed = []
    for s in todo:
        if os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}/nima/{}.json".format(b,s.split('/')[-1].split('.')[0])):
            print(s + " already done")
            continue
        else:
            id = s.split('/')[-1].split('.')[0]
            output = "/mnt/e/erya/collab_posts_ig/image/{}/nima/{}.json".format(b, id)
            subprocess.run(["python", "/home/research/neural-image-assessment/evaluate_mobilenet.py", "-img", s, "-rank", "false", "-output_path", output])