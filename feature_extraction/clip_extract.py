import os
os.chdir('/home/research/Long-CLIP')
print(os.getcwd())
import random
import json
# Using multibench env
from model import longclip
import torch
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = longclip.load("./checkpoints/longclip-B.pt", device=device)

save_path = '/mnt/e/erya/collab_posts_ig/images'

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
    if not os.path.exists("/mnt/e/erya/collab_posts_ig/image/{}/clip".format(b)):
        os.makedirs("/mnt/e/erya/collab_posts_ig/image/{}/clip".format(b))
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}/clip".format(b),  " Created ")
    else:
        print("Directory ", "/mnt/e/erya/collab_posts_ig/image/{}/clip".format(b),  " already exists")
    failed= []
    for f in todo:
        print("Starting ... {}".format(f))
        name = f.split('/')[-1].split('.')[0]
        id = f.split('/')[-2]
        if os.path.exists('/mnt/e/erya/collab_posts_ig/image/{}/clip/{}.json'.format(b,name)):
            print("Already done ")
        else:
            print("Processing ...")
            file_path = '/mnt/e/erya/collab_posts_ig/text/{}/{}.txt'.format(b,id)

            with open(file_path, 'r') as file:
                file_contents = file.read()
            text = longclip.tokenize([file_contents]).to(device)
            image = preprocess(Image.open("/mnt/e/erya/collab_posts_ig/media/{}/{}.jpg".format(b,name))).unsqueeze(0).to(device)

            with torch.no_grad():
                image_features = model.encode_image(image)
                text_features = model.encode_text(text)
                
                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                similarity = text_features.cpu().numpy() @ image_features.cpu().numpy().T

            with open('/mnt/e/erya/collab_posts_ig/image/{}/clip/{}.json'.format(b,name), 'w') as f:
                json.dump({'Similarity':similarity.tolist()[0][0]}, f)
            
    with open('/mnt/e/erya/collab_posts_ig/image/{}/clip/failed.json'.format(b), 'w') as f:
        json.dump(failed, f)