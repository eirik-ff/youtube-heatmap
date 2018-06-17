from read_data import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    TEST_DATA_PATH = r"./test-data.csv"

    weekdays = ["monday", "tuesday", "wednesday", "thursday", 
                    "friday", "saturday", "sunday"]  # x
    hours = [str(i) for i in range(0, 24)]  # y


    lines = read_data(TEST_DATA_PATH)
    arr = parse_data(lines)
    data = make_np_array(arr)

    ax = sns.heatmap(data, linewidth=0, xticklabels=weekdays, center=0.5, 
                     annot=True, fmt=".2f", cmap="plasma")
    ax.xaxis.set_ticks_position("top")

    plt.show()


if __name__ == '__main__':
    main()