from data_io import *
import get_channel_data as gcd
from get_channel_data import *

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import tkinter as tk
from tkinter import filedialog

import dateutil.parser


gcd.DEBUG = False


def display_heatmap(data, xlabels, colormap="plasma"):
    """
    data is a 2d array with x-index as weekday (0..6), y-index as hour (0..23)
    and entry as probability (0..1)
    """
    ax = sns.heatmap(data, linewidth=0, xticklabels=xlabels,
                     annot=False, fmt=".2f", cmap=colormap)
    ax.xaxis.set_ticks_position("top")
    plt.xticks(rotation=45)
    plt.show()


def get_videos(service, channel_id):
    """
    returns a list of parsed videos
    """
    upload_id = upload_playlist_id(service, channel_id)
    videos = all_videos_in_playlist(service, upload_id)
    parsed = parse_videos(videos)

    return parsed


def ISO8601_to_datetime(s):
    return dateutil.parser.parse(s)


def videos_to_weekday_hour_probabilites(videos):
    """
    count and calculate probability for upload on what hour of weekdays.
    
    returns list with weekdays (0..6) as x-index, hour (0..23) as y-index
    and probability (0..1) as entry. 
    """
    HOURS = 24
    DAYS  = 7
    probs = [[0 for _ in range(DAYS)] for __ in range(HOURS)]
    total = len(videos)  # total number of videos

    for video in videos:
        id_, date, title = video
        date = ISO8601_to_datetime(date)

        weekday = date.weekday()
        hour = date.hour

        probs[hour][weekday] += 1.0 / total

    return make_np_array(probs)


def user_input():
    """
    returns 2-tuple: is_id,id/username
    """
    name = input("Enter YouTube ID. If you can't find the ID, press "
                "return and enter username: ")

    is_id = True
    if name.strip() == "":
        is_id = False
        name = input("Enter username: ")

    return (is_id, name)


def main():
    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                    "Friday", "Saturday", "Sunday"]

    youtube = get_authenticated_service()

    is_id, name = user_input()

    if is_id:
        channel_id = name
    else:
        channel_id = channel_id_from_username(youtube, name)

    print("Downloading from YouTube...")
    videos = get_videos(youtube, channel_id)
    print("Done!")

    print("Saving data...")
    fname = write_videos_to_csv(videos, 
                        channel_username_from_id(youtube, channel_id),
                        channel_id)
    print("Done! Saved to", fname)

    data = videos_to_weekday_hour_probabilites(videos)

    print("Displaying heatmap...")
    username = channel_username_from_id(youtube, channel_id)
    plt.figure(username)
    display_heatmap(data, WEEKDAYS)


if __name__ == '__main__':
    main()