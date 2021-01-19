import sys
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def parse_args():
    if len(sys.argv) == 4 and sys.argv[0] == '-m' and sys.argv[1] == 'pdb':
        print("DEBUGGING")
    elif len(sys.argv) != 2:
        print('USAGE: python3 plot.py LOG_FILE_PATH')
        sys.exit(1)
    log_filename = sys.argv[1]
    return log_filename


def load_dict(log_filename):
    tags = {}

    with open(log_filename) as f:
        for line in f:

            if line[0] == '#':
                continue

            timestamp, tag_id, distance = line.split()

            if int(distance) == 999999:
                continue

            timestamp = int(timestamp)
            tag_id = tag_id.split(':')[-1]
            distance = int(distance)
            #distance = int(round(distance / 100))

            if tag_id not in tags:
                tags[tag_id] = []
            tags[tag_id].append((timestamp,distance))

    return tags


def plot(tags):
    for tag, data in tags.items():
        print("Plotting data for", tag)
        x_axis, y_axis = zip(*data)
        print(x_axis)
        print(y_axis)

        smoothed_y_axis = savgol_filter(y_axis, window_length=9, polyorder=3)

        plt.plot(x_axis, y_axis)
        plt.title('TotTag data for device ' + str(tag))
        plt.xlabel('Timestamp')
        plt.ylabel('Distance in mm')
        plt.show()

        plt.plot(x_axis, smoothed_y_axis)
        plt.title('TotTag data for device ' + str(tag))
        plt.xlabel('Timestamp')
        plt.ylabel('Distance in mm')
        plt.show()


if __name__ == "__main__":
    log_filename = parse_args()
    tags = load_dict(log_filename)
    plot(tags)
