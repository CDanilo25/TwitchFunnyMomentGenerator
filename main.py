import os.path
import shutil
import signal
import subprocess

import videoUtils
from twitchdl import twitch
from pathlib import Path

from translations import Translations

STREAMER_CHANNEL = ''
STREAMER_TYPE = -1
STREAMER_HOWMANY = ''

labels = Translations()


def download_elements(info_func, twitch_get_func, util_func, end_func):
    global STREAMER_HOWMANY, STREAMER_CHANNEL
    end_repeat = '1'
    transition_funny = ''
    twitch_resultFunc = info_func()

    for i in range(STREAMER_HOWMANY):
        video_id = twitch_resultFunc["edges"][i]["node"]["id"] if STREAMER_TYPE == 0 else \
        twitch_resultFunc["edges"][i]["node"]["slug"]
        video_title = twitch_resultFunc["edges"][i]["node"]["title"]

        print(labels.get("main_download").format(video_title))

        util_func(video_id, twitch_get_func, i)

    while (transition_funny != '0') and (transition_funny != '1'):
        transition_funny = input(labels.get("main_transition_ask"))

    if STREAMER_TYPE == 1:
        end_func(STREAMER_CHANNEL, transition_funny)

    while end_repeat != '0' and STREAMER_TYPE == 0:
        end_func(STREAMER_CHANNEL, transition_funny)
        end_repeat = input(labels.get("main_repeatOperation_ask"))


def twitch_vibe_check():
    global STREAMER_CHANNEL
    try:
        twitch.get_channel_videos(STREAMER_CHANNEL, 1, "time")
    except:
        if STREAMER_CHANNEL != '':
            print(labels.get("main_vibe_check_error"))
        return -1


def exit_cleanup(sig, frame):
    print(labels.get("main_exit_cleanup"))
    shutil.rmtree("twitchtmp")
    exit(1)


def ffmpeg_check():
    try:
        subprocess.run(["ffmpeg", "-version"], shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        print(labels.get("main_error_ffmpeg"))
        exit(404)
    stuff_check()


def stuff_check():
    if not os.path.exists("stuff/staticTransition.mp4"):
        print(labels.get("main_error_stuff"))
        exit(500)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_cleanup)
    ffmpeg_check()
    Path("twitchtmp/output").mkdir(parents=True, exist_ok=True)
    Path("result").mkdir(parents=True, exist_ok=True)

    while (STREAMER_TYPE != '0') and (STREAMER_TYPE != '1'):
        STREAMER_TYPE = input(labels.get("main_start_streamerTypeAsk"))

    STREAMER_TYPE = int(STREAMER_TYPE)

    while type(STREAMER_HOWMANY) != int:
        STREAMER_HOWMANY = input(labels.get("main_start_streamerManyAsk"))
        try:
            STREAMER_HOWMANY = int(STREAMER_HOWMANY)
        except ValueError:
            STREAMER_HOWMANY = ''

    while twitch_vibe_check() == -1:
        STREAMER_CHANNEL = input(labels.get("main_start_streamerNameAsk"))

    if STREAMER_TYPE == 0:
        download_elements(lambda: twitch.get_channel_videos(STREAMER_CHANNEL, STREAMER_HOWMANY, "time"),
                          twitch.get_video, videoUtils.twitchVideoDownload, videoUtils.twitchVideoEndFunc)
    elif STREAMER_TYPE == 1:
        clip_period = ''
        clip_period_selection = {'0': 'all_time', '1': 'last_day', '2': 'last_week', '3': 'last_month'}
        while clip_period not in clip_period_selection:
            clip_period = input(labels.get("main_start_streamerClipPeriodAsk"))

        download_elements(lambda: twitch.get_channel_clips(STREAMER_CHANNEL, clip_period_selection[clip_period], STREAMER_HOWMANY),
                          twitch.get_clip, videoUtils.twitchClipDownload, videoUtils.twitchClipEndFunc)

    exit_cleanup(signal.SIGTERM, 0)
