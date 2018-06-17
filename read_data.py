import numpy as np


def read_data(path):
    """
    read data from csv file
    """
    with open(path, "r") as f:
        lines = f.readlines()

    return lines


def parse_data(lines):
    """
    parses data with header x,y,prob. where x: int, y: int, prob: float
    will return 2-dim array with x,y as indices and prob as value
    """
    HOURS = 24
    DAYS  = 7
    arr = [[0 for _ in range(DAYS)] for __ in range(HOURS)]  # TODO: remove consts

    for i, line in enumerate(lines):
        line = line.strip()
        if not line.startswith("#") and line != "":  # not comments or empty
            x, y, prob = line.split(",")

            x = int(x)
            y = int(y)
            prob = float(prob.strip())  # remove trailing whitespace

            arr[y][x] = prob

    return arr


def make_np_array(arr):
    return np.array(arr)


def main():
    from pprint import pprint
    TEST_DATA_PATH = r"./test-data.csv"

    lines = read_data(TEST_DATA_PATH)
    arr = parse_data(lines)

    for y in arr:
        for x in y:
            print(x, end="\t")
        print()


if __name__ == '__main__':
    main()