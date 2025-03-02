import os
import json
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from scenedetect import detect, open_video, ContentDetector, SceneManager, StatsManager, AdaptiveDetector
from scenedetect.scene_manager import save_images
from scenedetect.scene_manager import write_scene_list

brands = []
for i in os.listdir('/mnt/e/erya/collab_posts_ig/post_summary'):
    #print(i)
    if i.endswith('.csv') and not i.startswith('.'):
        brands.append(i.split('.')[0])
brands = [b for b in brands if 'abercrombie' not in b]
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
    

    # load sampled videos
    # samplefile_list = []
    # for path, subdirs, files in os.walk('/large_data_storage2/SVD-data/sample'):
    #     for name in files:
    #         samplefile_list.append(os.path.join(path, name))
    if len(todo) == 0:
        continue
    else:
        bad_video_list = []
        for i in todo:
            video_path = i
            print(video_path)
            brand = video_path.split('/')[-3]
            id = video_path.split('/')[-1].split('.')[0]
            if os.path.exists('/mnt/e/erya/collab_posts_ig/video/scene/stats/{}/{}_stats.csv'.format(brand, id)):
                print(id + " already done")
                continue
            else:
                try:
                    video_stream = open_video(video_path)
                    stats_manager = StatsManager()
                    # Construct our SceneManager and pass it our StatsManager.
                    scene_manager = SceneManager(stats_manager)

                    # Add ContentDetector algorithm (each detector's constructor
                    # takes various options, e.g. threshold).
                    scene_manager.add_detector(AdaptiveDetector())

                    # Save calculated metrics for each frame to {VIDEO_PATH}.stats.csv.
                    stats_savepath = '/mnt/e/erya/collab_posts_ig/video/scene/stats'
                    if not os.path.exists(stats_savepath+ '/'+ brand):
                        os.makedirs(stats_savepath+ '/'+ brand)
                        stats_savepath = stats_savepath+ '/'+ brand
                    else:
                        stats_savepath = stats_savepath+ '/'+ brand
                    stats_file_path = os.path.join(stats_savepath, '{}_stats.csv'.format(id) )
                    
                    # Perform scene detection.
                    scene_manager.detect_scenes(video=video_stream)
                    scene_list = scene_manager.get_scene_list()
                    # write scene csv file
                    try:
                        stats_manager.save_to_csv(csv_file=stats_file_path)
                    except:
                        pass

                #plot scene csv file
                # plot_savepath = '/large_data_storage2/SVD-data/scene/plots'
                # plot_file_path =  os.path.join(plot_savepath, '{}.png'.format(id))
                # sta = pd.read_csv(stats_file_path)
                # plt.plot(sta["Frame Number"], sta.content_val)
                # plt.xlabel("Frame")
                # plt.ylabel("Content_val")
                # plt.axhline(y=30, color='black', linestyle='--')
                # plt.savefig(plot_file_path)

                # save scene images
                    image_savepath = '/mnt/e/erya/collab_posts_ig/video/scene/images'
                    if not os.path.exists(image_savepath+ '/'+ brand):
                        os.makedirs(image_savepath+ '/'+ brand)
                        image_savepath = image_savepath+ '/'+ brand
                    else:
                        image_savepath = image_savepath+ '/'+ brand
                    image_file_path =  os.path.join(image_savepath, id)
                    try:
                        save_images(scene_list, video_stream, num_images = 3, image_extension = 'jpg', output_dir = image_file_path)
                    except:
                        pass

                    # save scene list to csv
                    scenelist_savepath = '/mnt/e/erya/collab_posts_ig/video/scene/scene_list'
                    if not os.path.exists(scenelist_savepath+ '/'+ brand):
                        os.makedirs(scenelist_savepath+ '/'+ brand)
                        scenelist_savepath = scenelist_savepath+ '/'+ brand
                    else:
                        scenelist_savepath = scenelist_savepath+ '/'+ brand
                    scenelist_file_path = os.path.join(scenelist_savepath, '{}_scene.csv'.format(id))
                    try:
                        with open( scenelist_file_path, mode='w') as new_file:
                            write_scene_list(new_file, scene_list)
                    except:
                        pass

                    print(id + " done")
                except:
                    
                    bad_video_list.append(id)
                    print(id + " failed")
        if os.path.exists('/mnt/e/erya/collab_posts_ig/video/scene/stats/{}'.format(b)):
            print("Directory ", "/mnt/e/erya/collab_posts_ig/video/scene/stats/{}".format(b),  " already exists")
        else:
            os.makedirs("/mnt/e/erya/collab_posts_ig/video/scene/stats/{}".format(b))
            print("Directory ", "/mnt/e/erya/collab_posts_ig/video/scene/stats/{}".format(b),  " Created ")
        with open("/mnt/e/erya/collab_posts_ig/video/scene/stats/{}/bad_video.json".format(b), "w") as f:
            json.dump(bad_video_list, f)
        print("Saved {} bad video list for {}".format(len(bad_video_list),b))