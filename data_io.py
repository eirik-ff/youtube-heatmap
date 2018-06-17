import numpy as np
from datetime import datetime

def read_lines(path):
    """
    read data from csv file
    """
    with open(path, "r") as f:
        lines = f.readlines()

    return lines


def parse_data_from_csv(lines, sep=","):
    """
    parses data with header x,y,prob. where x: int, y: int, prob: float
    return 2-dim array with x,y as indices and prob as value
    """
    HOURS = 24
    DAYS  = 7
    arr = [[0 for _ in range(DAYS)] for __ in range(HOURS)]  # TODO: remove consts

    for line in lines:
        line = line.strip()
        if not line.startswith("#") and line != "":  # not comments or empty
            x, y, prob = line.split(sep)

            x = int(x)
            y = int(y)
            prob = float(prob.strip())  # remove trailing whitespace

            arr[y][x] = prob

    return arr


def make_np_array(arr):
    return np.array(arr)


def write_videos_to_csv(videos, username, id_, filename=None):
    """
    writes parsed data to csv file.
    returns filename/filepath
    """
    SEP = ";"
    HEADER = "# Video data for {name} ({id})\n# id{sep}publishedAt{sep}" \
             "title\n".format(
        name=username, 
        id=id_,
        sep=SEP
    )

    if filename is None:
        username = username.replace(" ", "-")
        fmode = "w"
        filename = r"./data/{name}_{date}.csv".format(name=username,
                                                date=str(datetime.now().date()))
    else:
        fmode = "a"

    f = open(filename, fmode, encoding="UTF-8")
    f.write(HEADER)

    for video in videos:
        id_, date, title = video

        if SEP in title:
            title.replace(SEP, "")  # just remove 

        line = "{id}{sep}{date}{sep}{title}\n".format(
            id=id_,
            date=date,
            title=title,
            sep=SEP
        )
        f.write(line)

    f.close()

    return filename


def read_videos_from_csv(filename, sep=";"):
    """
    reads csv file with data from write_videos_to_csv.
    returns a list of 3-tuples: id, publish_date, title
    """
    with open(filename, "r", encoding="UTF-8") as f:
        lines = f.readlines()

    videos = []
    for line in lines:
        line = line.strip()
        if not line.startswith("#") and line != "":
            videos.append( (line.split(sep)) )

    return videos


def main():
    TEST_DATA_PATH = r"./data/test-data.csv"

    lines = read_data(TEST_DATA_PATH)
    arr = parse_data(lines)

    for y in arr:
        for x in y:
            print(x, end="\t")
        print()


if __name__ == '__main__':
    main()