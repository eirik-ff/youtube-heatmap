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


gcd.DEBUG = True


def main_testing():
    root = tk.Tk()
    root.withdraw()  # hide root window
    file_path = filedialog.askopenfilename()
    print(file_path)

    TEST_DATA_PATH = r"./data/test-data.csv"

    weekdays = ["monday", "tuesday", "wednesday", "thursday", 
                    "friday", "saturday", "sunday"]  # x
    hours = [str(i) for i in range(0, 24)]  # y


    lines = read_lines(file_path)
    arr = parse_data_from_csv(lines)
    data = make_np_array(arr)

    ax = sns.heatmap(data, linewidth=0, xticklabels=weekdays, center=0.5, 
                     annot=True, fmt=".2f", cmap="plasma")
    ax.xaxis.set_ticks_position("top")

    plt.show()

################################################################################

def display_heatmap(data, xlabels, colormap="plasma"):
    """
    data is a 2d array with x-index as weekday (0..6), y-index as hour (0..23)
    and entry as probability (0..1)
    """
    ax = sns.heatmap(data, linewidth=0, xticklabels=xlabels,
                     annot=True, fmt=".2f", cmap=colormap)
    ax.xaxis.set_ticks_position("top")
    plt.show()


def get_videos(channel_id):
    """
    returns a list of parsed videos
    """
    youtube = get_authenticated_service()

    upload_id = upload_playlist_id(youtube, channel_id)
    videos = all_videos_in_playlist(youtube, upload_id)
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

    return probs


def main():
    YOUTUBE_ID = "UCtinbF-Q-fVthA0qrFQTgXQ"  # Casey Neistat
    WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", 
                    "friday", "saturday", "sunday"]

    videos = get_videos(YOUTUBE_ID)
    print("Downloaded YouTube data...")
    data = videos_to_weekday_hour_probabilites(videos)
    print("Displaying heatmap...")
    display_heatmap(data, WEEKDAYS)


if __name__ == '__main__':
    main()