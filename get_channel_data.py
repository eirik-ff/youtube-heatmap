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


def main():
    service = get_authenticated_service()

    request = service.search().list(
        part="snippet",
        channelId="UCtinbF-Q-fVthA0qrFQTgXQ",
        order="date"
    )

    results = request.execute()

    print(results, end="\n\n")
    
    next_page = service.search().list_next(
        previous_request=request,
        previous_response=results
    )

    print(next_page.execute())
    return

    max_results = results['pageInfo']['totalResults']
    print(max_results)

    videos = []  # list of 3-tuples: id,title,publish_date
    others = []  # everything that's not youtube#video

    searched_results = 0
    while searched_results < max_results:  # loop to get all results
        # find max_results
        if abs(max_results - searched_results) >= 50:  # 50 is max per search
            max_ = 50
        else:
            max_ = max_results - searched_results

        request = service.search().list(
            part="snippet",
            channelId="UCtinbF-Q-fVthA0qrFQTgXQ",
            order="date",
            maxResults=max_
        )

        results = request.execute()

        searched_results += max_

        # parse results
        for vid in results['items']:
            vid_id = vid['id']['videoId']
            title = vid['snippet']['title']
            date  = vid['snippet']['publishedAt']

            if vid['id']['kind'] == "youtube#video":
                videos.append( (vid_id, title, date) )
            else:
                kind = vid['id']['kind']
                others.append( (vid_id, kind, title, date) )


    print("VIDEOS:", len(videos))
    for video in videos:
        print(video)

    print("OTHERS:", len(others))
    for other in others:
        print(other)




if __name__ == '__main__':
    main()