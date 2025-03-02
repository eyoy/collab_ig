import json
import re
import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote_plus

import pandas as pd
import requests
from tqdm.notebook import tqdm
from retry.api import retry_call
import os
os.chdir('/mnt/e/erya/socialmedia_ads/IG')

sf_api_key = "INhGdYFecrKghvYft3BTGPQxYgP27oobSIaM74zvehIWJWuAEKhkXVE3dVpWgaFjBx90YDwaVxPFyRyUTO"
usernames = [
    "chickfila", "olivegarden", "dominos", "pizzahut", "wendys", "subway",
    "burgerking", "kfc", "mcdonalds", "applebees", "tacobell", "cheesecakefactory",
    "panerabread", "chipotle", "redlobster", "popeyes", "sonicdrivein", "jerseymikes",
    "chilis", "ihop", "littlecaesars", "crackerbarrel", "fiveguys", "innout", "papajohns",
    "arbys", "bwwings", "wafflehouseofficial", "dennysdiner", "redrobinburgers",
    "whataburger", "officialpandaexpress", "wingstop", "raisingcanes", "steaknshake",
    "daveandbusters", "goldencorral", "papamurphys", "starbucks", "realzaxbys",
    "famousdaves", "jimmyjohns", "dunkin", "dairyqueen", "krispykreme", "culver",
    "baskinrobbins", "tgifridays", "hardees", "coldstone", "peetscoffee",
    "smoothieking", "tropicalsmoothiecafe", "whitecastle", "timhortons", "jambajuice",
    "bojangles", "veggiegrill", "sweetgreen", "honeygrow", "cava", "pfchangs",
    "lemonadela", "eddievs_", "carlsjr", "modpizza", "firehousesubs", "bjsrestaurants",
    "longhornsteaks", "outback", "jackinthebox", "texasroadhouse", "twinpeaksrestaurants",
    "originalnathans", "captaindsseafood", "qdoba", "habitburgergrill", "auntieannespretzels",
    "ruthschris", "noodlescompany", "cheddarskitchen", "yardhouse", "einsteinbros",
    "shakeshack", "firstwatch", "deltaco", "crumblcookies", "tiltedkiltpub", "rubioscoastalgrill",
    "hooters", "kungfuteausa", "fuddruckers", "carrabbas", "churchschicken", "freddysusa",
    "mcalistersdeli", "checkersrallys", "elpolloloco", "dutchbroscoffee", "pinkberryswirl"
]
usernames = ["culver","modpizza", "yardhouse","shakeshack"]


def parse_posts(response_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    top_level_key = "graphql" if "graphql" in response_json else "data"
    user_data = response_json[top_level_key].get("user", {})
    post_edges = user_data.get("edge_owner_to_timeline_media", {}).get("edges", [])
    posts = []
    for node in post_edges:
        post_json = node.get("node", {})
        shortcode = post_json.get("shortcode")
        image_url = post_json.get("display_url")
        caption_edges = post_json.get("edge_media_to_caption", {}).get("edges", [])
        description = caption_edges[0].get("node", {}).get("text") if len(caption_edges) > 0 else None
        n_comments = post_json.get("edge_media_to_comment", {}).get("count")
        likes_key = "edge_liked_by" if "edge_liked_by" in post_json else "edge_media_preview_like"
        n_likes = post_json.get(likes_key, {}).get("count")
        timestamp = post_json.get("taken_at_timestamp")
        posts.append({
            "shortcode": shortcode,
            "image_url": image_url,
            "description": description,
            "n_comments": n_comments,
            "n_likes": n_likes,
            "timestamp": timestamp,
        })
    return post_edges

def parse_page_info(response_json: Dict[str, Any]) -> Dict[str, Union[Optional[bool], Optional[str]]]:
    top_level_key = "graphql" if "graphql" in response_json else "data"
    user_data = response_json[top_level_key].get("user", {})
    page_info = user_data.get("edge_owner_to_timeline_media", {}).get("page_info", {})
    return page_info

def download_media(url, media_type, post_id, short_code, username):
    save_path = '/mnt/e/erya/socialmedia_ads/IG/media/{}/{}'.format(username,post_id)
    if media_type == 'GraphImage':
        img_data = requests.get(url).content
        with open(save_path+'/{}_{}.jpg'.format(post_id, short_code), 'wb') as handler:
            handler.write(img_data)
    elif media_type == 'video':
        video_data = requests.get(url).content
        with open(save_path+'/{}_{}.mp4'.format(post_id, short_code), 'wb') as handler:
            handler.write(video_data)
    else:
        for i in url:
            if ".jpg" in i:
                img_data = requests.get(i).content
                with open(save_path+'/{}_{}_{}.jpg'.format(post_id,short_code,url.index(i)), 'wb') as handler:
                    handler.write(img_data)
            else:
                video_data = requests.get(i).content
                with open(save_path+'/{}_{}_{}.mp4'.format(post_id,short_code, url.index(i)), 'wb') as handler:
                    handler.write(video_data)
for username in usernames:
    print(username)
    params = {
            "api_key": sf_api_key,
            "url": f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            "headers": json.dumps({"x-ig-app-id": "936619743392459"}),
        }

    def request_json(url, params) -> Dict[str, Any]:
        response = requests.get(url, params=params, timeout=110)
        response.raise_for_status()
        return response.json()

    try:
        response_json = request_json(url="https://scraping.narf.ai/api/v1/", params=params)
        if response_json.getcode() == 200:
            print('Success')
            break
    except:
        pass
    user_id = response_json.get("data", {}).get("user", {}).get("id")
    if not user_id:
        print(f"User {username} not found.")
        #return []
    # parse the first batch of posts from user profile response
    posts = parse_posts(response_json=response_json)
    page_info = parse_page_info(response_json=response_json)
    # get next page cursor
    end_cursor = page_info.get("end_cursor")
    if os.path.exists('meta/{}'.format(username)):
        pass
    else:
        os.mkdir('meta/{}'.format(username))
    if os.path.exists('media/{}'.format(username)):
        pass
    else:
        os.mkdir('media/{}'.format(username))
    for i in posts:
        print(posts.index(i))
        post_response = i['node']
        post_id = i['node']['id']
        short_code = i['node']['shortcode']
        media_type = i['node']['__typename']
        if os.path.exists('meta/{}/{}'.format(username,post_id)):
            pass
        else:
            os.mkdir('/mnt/e/erya/socialmedia_ads/IG/meta/{}/{}'.format(username,post_id))
            with open('/mnt/e/erya/socialmedia_ads/IG/meta/{}/{}/{}_{}.json'.format(username,post_id,post_id,short_code), 'w') as f:
                json.dump(i, f)
        # if os.path.exists('media/{}/{}'.format(username,post_id)):
        #     pass
        # else:
        #     os.mkdir('media/{}/{}'.format(username,post_id)) 
        #     if media_type == 'GraphSidecar':
        #         multimedia = post_response.get("edge_sidecar_to_children", {}).get("edges", [])
        #         num_media = len(multimedia)
        #         media_id = [i.get("node", {}).get('id') for i in multimedia]
        #         media_url = [i.get("node", {}).get('display_url') if i.get("node", {}).get("__typename") == "GraphImage" else i.get("node", {}).get('video_url') for i in multimedia]
        #         download_media(media_url, media_type,post_id, short_code, username)
        #         #n_view = [-1 if i.get("node", {}).get("__typename") == "GraphImage" else i.get("node", {}).get('video_view_count') for i in multimedia]
        #     elif media_type == "GraphImage":
        #         num_media = 1
        #         media_id = post_id
        #         media_url = post_response.get("display_url")
        #         download_media(media_url, media_type,post_id, short_code, username)
        #         #n_view = -1
        #     else:
        #         num_media = 1
        #         media_id = post_id
        #         media_url = post_response.get("video_url")
        #         #print(media_url)
        #         download_media(media_url, "video",post_id, short_code, username)  
    #end_cursor = 'QVFETWxYclU1SWZ4MnhLeF83MWF5bHY0dUhCbHB1SkVDdERhcUxKV3oyUk5yYmNBMjJacHRHbFV4c1FLWm9BRWI1UjNaOXJBR0psUnQ0NHd4WWhYdlJoVA'
    #end_cursor = 'QVFBbWV5a1FQd0NzbVplRTB4SXl4MXRTY01uN0czRHRjZHNzUEIwTUJlU25Kbk9RNlpzVWdueC1xZE9oU0JYLTkwLWFxdVlhVVdPeHd2dGpIRzVGd21ITg=='
    #end_cursor = 'QVFCRjNabFVaSldDR3BDZnhYX2dKbkRyUDdYUWp2WG5MNTZxU0JZRmlCaWVoblg1dEIwajdxbnpFTWtOeVR4RmJua1BNZndWYnRrRlZBUXBEYmJRalBkaQ=='
    while end_cursor:
        params = {
            "api_key": sf_api_key,
            #"url": f"https://instagram.com/graphql/query/?query_id=17888483320059182&id={user_id}&first=24&after={end_cursor}",
            "url":f"https://instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&id={user_id}&first=24&after={end_cursor}"
            #"url":f"https://instagram.com/graphql/query/?query_hash=56a7068fea504063273cc2120ffd54f3&id={user_id}&first=24&after={end_cursor}"
        }
        try:
            response_json = request_json(url="https://scraping.narf.ai/api/v1/", params=params)
            if response_json.getcode() == 200:
                break
        except:
            pass
        posts = parse_posts(response_json=response_json)
        page_info = parse_page_info(response_json=response_json)
        end_cursor = page_info.get("end_cursor")
        print(end_cursor)
        for i in posts:
            print(posts.index(i))
            post_response = i['node']
            post_id = i['node']['id']
            short_code = i['node']['shortcode']
            media_type = i['node']['__typename']
            if os.path.exists('meta/{}/{}'.format(username,post_id)):
                pass
            else:
                os.mkdir('/mnt/e/erya/socialmedia_ads/IG/meta/{}/{}'.format(username,post_id))
                with open('/mnt/e/erya/socialmedia_ads/IG/meta/{}/{}/{}_{}.json'.format(username,post_id,post_id,short_code), 'w') as f:
                    json.dump(i, f)
            # if os.path.exists('media/{}/{}'.format(username,post_id)):
            #     pass
            # else:
            #     os.mkdir('media/{}/{}'.format(username,post_id)) 
            #     if media_type == 'GraphSidecar':
            #         multimedia = post_response.get("edge_sidecar_to_children", {}).get("edges", [])
            #         num_media = len(multimedia)
            #         media_id = [i.get("node", {}).get('id') for i in multimedia]
            #         media_url = [i.get("node", {}).get('display_url') if i.get("node", {}).get("__typename") == "GraphImage" else i.get("node", {}).get('video_url') for i in multimedia]
            #         download_media(media_url, media_type,post_id, short_code, username)
            #         #n_view = [-1 if i.get("node", {}).get("__typename") == "GraphImage" else i.get("node", {}).get('video_view_count') for i in multimedia]
            #     elif media_type == "GraphImage":
            #         num_media = 1
            #         media_id = post_id
            #         media_url = post_response.get("display_url")
            #         download_media(media_url, media_type,post_id, short_code, username)
            #         #n_view = -1
            #     else:
            #         num_media = 1
            #         media_id = post_id
            #         media_url = post_response.get("video_url")
            #         #print(media_url)
            #         download_media(media_url, "video",post_id, short_code, username)


                