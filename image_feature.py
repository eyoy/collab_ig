import os
import json
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import ultralytics
ultralytics.checks()
from ultralytics import YOLO

brands = [i.split('.')[0] for i in os.listdir('/mnt/e/erya/collab_posts_ig/id_2021_2024')]
model = YOLO("yolov8n.pt")
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
        os.chdir("/mnt/e/erya/collab_posts_ig/image/{}/".format(b))
        failed = []
        for s in todo:
            if os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}/runs/detect/predicts/{}".format(b,s.split('/')[-1])):
                print(s + " already done")
                continue
            else:
                try:
                    model.predict(s, save=True, save_txt=True, save_conf = True, conf = 0.7, device = "1")
                except:
                    print(s + " failed")
                    failed.append(s)
                    continue
        with open("/mnt/e/erya/collab_posts_ig/image/{}/failed.json".format(b), "w") as f:
            json.dump(failed, f)

    else:
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}".format(b),  " already exists")
    
    # Run inference on the source
    