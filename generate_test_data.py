from random import random


def write_header(f):
    """
    f is file object
    """
    HEADER = """# x:    time of week (0..6)
# y:    time of day (0..23)
# prob: probability (0..1)
# x,y,prob
"""
    f.write(HEADER)


def next_data(prev):
    """
    to get a more "natural" transition
    """
    return sum(prev) / len(prev)


def make_data_arr():
    """
    makes data array
    """
    HOURS = 24
    DAYS  = 7
    arr = [[0 for _ in range(DAYS)] for __ in range(HOURS)]

    # make initial border with random numbers
    arr[0] = [random() for _ in range(DAYS)]
    for y in range(1, len(arr)):
        arr[y][0] = random()

    # generate data based on previous data
    for y in range(1, len(arr)):
        for x in range(1, len(arr[y])):
            arr[y][x] = next_data([ arr[y][x-1], arr[y-1][x], arr[y-1][x-1] ])

    return arr


def write_data(arr, f):
    """
    arr is data array from make_data_arr
    f is file object to be written to
    """
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            data = arr[y][x]

            line = "{},{},{}\n".format(x, y, data)
            f.write(line)


def main():
    TEST_DATA_PATH = r"./test-data.csv"
    f = open(TEST_DATA_PATH, "w")

    write_header(f)
    arr = make_data_arr()
    write_data(arr, f)

    f.close()


if __name__ == '__main__':
    main()