from PIL import Image
import numpy as np
import os
import json

def hue_proportions_brightness_contrast_clarity(image):
    """Calculate the proportion of warm to cold hues in an image."""
    # Convert the image to RGB and then to HSV
    hsv_image = image.convert('RGB').convert('HSV')
    hsv_array = np.array(hsv_image)

    # Extract Hue channel
    hue = hsv_array[:, :, 0]  # Hue channel

    # Define hue ranges for warm and cold
    warm_hue_mask = (hue >= 0) & (hue <= 90)  # Warm hues (reds and oranges)

    # Calculate saturation
    saturation = np.mean(hsv_array[:, :, 1]) / 255

    # Count warm and cold hues
    proportion_warm = np.mean(warm_hue_mask)
    # Calculate brightness
    brightness = np.mean(hsv_array[:, :, 2]) / 255

    # Calculate contrast of brightness
    contrast = np.std(hsv_array[:, :, 2]) / 255

    # Scale pixel brightness to [0, 1]
    scaled_brightness = hsv_array[:, :, 2] / 255

    # Count pixels with brightness greater than 0.7
    bright_pixels = scaled_brightness[scaled_brightness > 0.7]
    num_bright_pixels = len(bright_pixels)

    # Calculate clarity
    clarity = num_bright_pixels / (hsv_array.shape[0] * hsv_array.shape[1])

    return proportion_warm, saturation, brightness, contrast, clarity


#brands = [i.split('.')[0] for i in os.listdir('/mnt/e/erya/collab_posts_ig/id_2021_2024')]

# failed_files = []
# for b in brands:
#     with open('/mnt/e/erya/collab_posts_ig/id_2021_2024/{}.json'.format(b)) as f:
#         goodids = json.load(f)
#     print(b,len(goodids))
#     jpg_files = []
#     for root, dirs, files in os.walk("/mnt/e/erya/collab_posts_ig/media/{}".format(b), topdown=False):
#         for name in files:
#             if not name.startswith('.') and name.endswith('.jpg'):
#                 #print(name)
#                 #print(os.path.join(root, name))
#                 jpg_files.append(os.path.join(root, name))

#     todo = [i for i in jpg_files if i.split('/')[-2] in goodids]
#     print(b, len(todo))
for brand in os.listdir(r"F:\erya\collab_posts_ig\video\scene\images"):
    print(brand)
    if not os.path.exists(r"G:\ig\video\color\{}".format(brand)):
        os.makedirs(r"G:\ig\video\color\{}".format(brand))
        print("Directory ", r"G:\ig\video\color\{}".format(brand),  " Created ")
    else:
        print("Directory ", r"G:\ig\video\color\{}".format(brand),  " already exists")
    for s in os.listdir(r"F:\erya\collab_posts_ig\video\scene\images\{}".format(brand)):
        if os.path.exists(r"G:\ig\video\color\{}\{}".format(brand, s)):
            print(s + " already done")
            continue
        else:
            os.makedirs(r"G:\ig\video\color\{}\{}".format(brand, s))
        failed_files = []
        for img in os.listdir(r"F:\erya\collab_posts_ig\video\scene\images\{}\{}".format(brand,s)):
            id = img.split('.')[0]
            try:
                im = Image.open(r"F:\erya\collab_posts_ig\video\scene\images\{}\{}\{}".format(brand,s,img))
                warm_hue, saturation, brightntess, contrast, clarity = hue_proportions_brightness_contrast_clarity(im)
                with open(r"G:\ig\video\color\{}\{}\{}.json".format(brand, s, id), "w") as f:
                    json.dump({"warm_hue": warm_hue, "saturation": saturation, "brightness": brightntess, "contrast": contrast, "clarity": clarity}, f)
                print("Done with ", s)
            except:
                print(s + " failed")
                failed_files.append(s)
            
            

