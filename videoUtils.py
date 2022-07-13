import math
import os
import random
import re
import subprocess
import time
from urllib.parse import urlencode

import m3u8
import requests
from twitchdl import twitch, download
from moviepy.editor import *

import aux
import main
from main import labels

STREAMER_HOWMUCH = ''


def twitchVideoDownload(video_id, twitch_get_func, video_number):
    global STREAMER_HOWMUCH

    print(labels.get("vutils_video_auth"))
    twitch_download = twitch_get_func(video_id)
    twitch_access_token = twitch.get_access_token(video_id)
    twitch_playlist_uri = list(aux.parse_playlists(twitch.get_playlists(video_id, twitch_access_token)))[1][2]
    twitch_playlist_response = requests.get(twitch_playlist_uri)
    twitch_playlist_response.raise_for_status()
    twitch_playlist = m3u8.loads(twitch_playlist_response.text)
    twitch_vod_list = aux.get_vod_paths(twitch_playlist)

    print(labels.get("vutils_video_download"))
    twitch_downloaded_vods = download.download_files(re.sub("/[^/]+$", "/", twitch_playlist_uri), "twitchtmp/", twitch_vod_list, 3)
    print("... completato")
    print(labels.get("vutils_video_merge"))
    ffmpegFusion(twitch_downloaded_vods, video_number, '', 0, False)
    print(labels.get("vutils_video_clean"))
    cleanVodFolder()


def twitchVideoEndFunc(streamer_name, transition=0):
    global STREAMER_HOWMUCH

    while type(STREAMER_HOWMUCH) != int:
        STREAMER_HOWMUCH = input(labels.get("vutils_video_howMuchAsk"))
        try:
            STREAMER_HOWMUCH = int(STREAMER_HOWMUCH)
        except ValueError:
            STREAMER_HOWMUCH = ''

    print(labels.get("vutils_generatingFunny"))
    generateFunny(streamer_name, transition)


def twitchClipDownload(clip_slug, twitch_get_func, clip_number):
    print(labels.get("vutils_clip_urlGen"))
    twitch_access_token = twitch.get_clip_access_token(clip_slug)
    clip_url = twitch_access_token["videoQualities"][1]["sourceURL"]
    clip_query = urlencode({
        "sig": twitch_access_token["playbackAccessToken"]["signature"],
        "token": twitch_access_token["playbackAccessToken"]["value"]
    })
    clip_final_url = "{}?{}".format(clip_url, clip_query)

    print(labels.get("vutils_clip_download"))
    clip_request = requests.get(clip_final_url, allow_redirects=True)
    open("twitchtmp/{}.mp4".format(clip_number), 'wb').write(clip_request.content)


def twitchClipEndFunc(streamer_name, transition=0):
    print(labels.get("vutils_generatingFunny"))
    ffmpegFusion('', -1, streamer_name, 1, transition)


def ffmpegFusion(video_list, video_number, streamer_name, streamer_type, transition):
    list_file = open("twitchtmp/video.playlist", 'w')
    for file in os.listdir("twitchtmp"):
        if (".ts" if streamer_type == 0 else ".mp4") in file:
            list_file.write("file '{}'\n".format(file))
            if streamer_type == 1 and transition == '1':
                list_file.write("file '../stuff/staticTransition.mp4'\n")

    file_output = "twitchtmp/output/{}.mp4".format(video_number) if streamer_type == 0 else "result/{}_clip_{}.mp4".format(streamer_name, random.randint(1000, 9999))

    list_file.flush()
    list_file.close()
    time.sleep(2)

    try:
        subprocess.run(["ffmpeg",
                            "-safe", "0",
                            "-f", "concat",
                              "-i", "twitchtmp/video.playlist",
                              "-c", "copy",
                              file_output], shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(labels.get("vutils_ffmpeg_error"))
        exit(405)


def cleanVodFolder():
    for file in os.listdir("twitchtmp"):
        file_path = os.path.join("twitchtmp", file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def generateFunny(streamer_name, transition):
    global STREAMER_HOWMUCH, STREAMER_CHANNEL
    inputClips = []
    funnyClips = []
    funnyClips_final = []
    transitionVideo = VideoFileClip("stuff/staticTransition.mp4")
    index = 0

    for video in os.listdir("twitchtmp/output"):
        inputClips.append(VideoFileClip("twitchtmp/output/{}".format(video)))
        video_duration = math.floor(inputClips[index].duration)-31
        for x in range(int(STREAMER_HOWMUCH)):
            video_startClip = random.randint(0, video_duration)
            video_endClip = video_startClip + random.randint(2, 7)
            funnyClips.append(inputClips[index].subclip(video_startClip, video_endClip))
            print(labels.get("vutils_genFunny_stats").format(x, video_startClip, video_endClip))
        index = index + 1

    random.shuffle(funnyClips)

    if transition == '1':
        for element in funnyClips:
            funnyClips_final.append(element)
            funnyClips_final.append(transitionVideo)
    else:
        funnyClips_final = funnyClips

    video_final = concatenate_videoclips(funnyClips_final)
    video_final.write_videofile("result/{}_video_{}.mp4".format(streamer_name, random.randint(1000, 9999)), codec='libx264')
    time.sleep(5)

    for video in inputClips:
        video.close()
    transitionVideo.close()

    time.sleep(3)

