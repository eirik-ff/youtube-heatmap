from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


API_KEY_FILE = "api_key.txt"

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

DEBUG = True

################################################################################

def read_api_key(filename):
    with open(filename, "r") as f:
        key = f.read()
    return key


def get_authenticated_service():
    api_key = read_api_key(API_KEY_FILE)
    service = build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)
    return service


def channel_id_from_username(service, username):
    """
    returns the channel id for specified username
    """
    results = service.channels().list(
        part="id",
        forUsername=username
    ).execute()

    return results['items'][0]['id']


def upload_playlist_id(service, channel_id):
    """
    returns the upload playlist id for a specific channel
    """
    # not using playlist().list since it doesn't return upload id
    results = service.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    return results['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def all_videos_in_playlist(service, id_):
    """
    get all videos in specified playlist.
    returns a list of video json from youtube api
    """
    list_args = {
        "part": "snippet",
        "playlistId": id_,
        "maxResults": 50
    }

    request = service.playlistItems().list(**list_args)
    if DEBUG:
        results = request.execute()
        print("TOTAL RESULTS:", results['pageInfo']['totalResults'])

    videos = []  # list of 3-tuples: id,title,publish_date
    while request is not None:
        results = request.execute()
        len_ = len(results['items'])

        if DEBUG:
            print(len_)
            if len_ == 0:
                print(results)

        for vid in results['items']:
            videos.append(vid)

        request = service.playlistItems().list_next(
            previous_request=request,
            previous_response=results
        )

    return videos


def parse_videos(videos):
    """
    parses video json returned from all_videos_by_channel
    returns a list of 3-tuples: id, publish_date, title 
    """
    parsed = []
    for vid in videos:
        try:
            id_   = vid['snippet']['resourceId']['videoId']
            date  = vid['snippet']['publishedAt']
            title = vid['snippet']['title']

            parsed.append( (id_, date, title) )
        except KeyError as kerr:
            if DEBUG:
                print(kerr, vid)
            continue

    return parsed


def main():
    service = get_authenticated_service()

    CASEY_NEISTAT_ID = "UCtinbF-Q-fVthA0qrFQTgXQ"
    BON_APPETIT_ID   = "UCbpMy0Fg74eXXkvxJrtEn3w"
    upload_id = upload_playlist_id(service, BON_APPETIT_ID)

    videos = all_videos_in_playlist(service, upload_id)
    parsed = parse_videos(videos)

    print("VIDEOS:", len(videos), len(parsed))
    # for video in parsed:
    #     print(video[0], "\t", video[1], "\t", video[2])  # id, date, title


if __name__ == '__main__':
    main()