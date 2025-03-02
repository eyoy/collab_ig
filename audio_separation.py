from moviepy.editor import VideoFileClip
import os
import pandas as pd
import json

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    print("Audio extraction finished.", audio_path)

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
    mp4_files = []
    for root, dirs, files in os.walk("/mnt/e/erya/collab_posts_ig/media/{}".format(b), topdown=False):
        for name in files:
            if not name.startswith('.') and name.endswith('.mp4'):
                #print(name)
                #print(os.path.join(root, name))
                mp4_files.append(os.path.join(root, name))

    todo = [i for i in mp4_files if i.split('/')[-2] in goodids]
    print(b, len(todo))
    if len(todo) == 0:
        continue
    else:
        empty_audio_list = []
        for v in todo:
            video_path = v
            brand = video_path.split('/')[-3]
            id = video_path.split('/')[-1].split('.')[0]
            audio_filename = id + ".mp3"
            if not os.path.exists("/mnt/e/erya/collab_posts_ig/video/audio/{}".format(brand)):
                os.makedirs("/mnt/e/erya/collab_posts_ig/video/audio/{}".format(brand))
            else:
                pass
            audio_path = os.path.join("/mnt/e/erya/collab_posts_ig/video/audio", brand, audio_filename)
            if os.path.exists(audio_path):
                print(f"Audio file already exists for {id}.")
                continue
            else:
                try:
                    extract_audio(video_path, audio_path)
                    print(f"Audio extraction finished for {id}.")
                except:
                    empty_audio_list.append(id)
                    print(f"Audio extraction failed for {id}.")
        with open("/mnt/e/erya/collab_posts_ig/video/audio/{}/empty_audio.json".format(b), "w") as f:
            json.dump(empty_audio_list, f)
