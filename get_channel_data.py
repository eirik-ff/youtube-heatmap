from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pprint import pprint

API_KEY_FILE = "api_key.txt"

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


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


def all_videos_by_channel(service, id_):
    """
    get all videos posted by a specific channel. Enter either id or user name.
    returns a list of video json from youtube api
    """
    list_args = {
        "part": "snippet",
        "order": "date",
        "maxResults": 50,
        "channelId": id_,
        "type": "video"
    }

    request = service.search().list(**list_args)
    results = request.execute()

    print("TOTAL RESULTS:", results['pageInfo']['totalResults'])

    videos = []  # list of 3-tuples: id,title,publish_date
    while request is not None:
        results = request.execute()
        len_ = len(results['items'])

        if len_ == 0:
            print(results)

        for vid in results['items']:
            videos.append(vid)

        request = service.search().list_next(
            previous_request=request,
            previous_response=results
        )

    return videos


def parse_videos(videos):
    """
    parses video json returned from all_videos_by_channel
    returns a list of 3-tuples: id, title, publish_date
    """
    parsed = []
    for vid in videos:
        if vid['id']['kind'] == "youtube#video":
            vid_id = vid['id']['videoId']
            title = vid['snippet']['title']
            date  = vid['snippet']['publishedAt']

            parsed.append( (vid_id, title, date) )

    return parsed


def main():
    service = get_authenticated_service()

    videos = all_videos_by_channel(service, "UCtinbF-Q-fVthA0qrFQTgXQ")
    parsed = parse_videos(videos)

    print("VIDEOS:", len(videos), len(parsed))
    for video in parsed:
        print(video)


if __name__ == '__main__':
    main()