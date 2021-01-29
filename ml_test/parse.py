import sys
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from knn import classify_knn
from forest import classify_forest


def parse_args():
    if len(sys.argv) == 4 and sys.argv[0] == '-m' and sys.argv[1] == 'pdb':
        print("DEBUGGING")
    elif len(sys.argv) != 2:
        print('USAGE: python3 parse.py LOG_FILE_PATH')
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


def fill_buf(data, buf_size, start):
    old_start = start
    buf = []
    try:
        while len(buf) < buf_size:
            for i in range(0, buf_size):
                buf.append(data[start+i])
                if len(buf) > 1 and buf[i-1][0] != buf[i][0] - 1:
                    start += i
                    buf.clear()
                    break
        return (buf, start)

    except IndexError:
        print("Could not find valid window of length", buf_size, "starting at", old_start, "->", start)


def generate_sliding_windows(data, tag, window_length, window_shift):
    if tag in data:
        index = 0
        windows = []

        while index + window_length - 1 < len(data[tag]):
            curr_window, index = fill_buf(data[tag], window_length, index)
            index += window_shift
            windows.append(curr_window)

    return windows


def plot(tags):
    for tag, data in tags.items():
        print("Plotting data for", tag)
        x_axis, y_axis = zip(*data)
        # print(x_axis)
        # print(y_axis)

        smoothed_y_axis = savgol_filter(y_axis, window_length=9, polyorder=3)

        plt.figure(fig)
        fig += 1
        plt.scatter(x_axis, y_axis)
        plt.title('TotTag data for device ' + str(tag))
        plt.xlabel('Timestamp')
        plt.ylabel('Distance in mm')

        plt.figure(fig)
        fig += 1
        plt.scatter(x_axis, smoothed_y_axis)
        plt.title('TotTag data for device ' + str(tag))
        plt.xlabel('Timestamp')
        plt.ylabel('Distance in mm')
        plt.show()


def demo_sliding_window(tags):
    windows = generate_sliding_windows(tags, '41', 30, 30)
    
    half1 = windows[::2]
    half2 = windows[1::2]
    data1 = []
    data2 = []
    for window in half1:
        data1.extend(window)
    for window in half2:
        data2.extend(window)
    
    x_1, y_1 = zip(*data1)
    x_2, y_2 = zip(*data2)

    plt.title('TotTag sliding window demo')
    plt.xlabel('Timestamp')
    plt.ylabel('Distance in mm')
    plt.scatter(x_1, y_1)

    plt.scatter(x_2, y_2)

    for i in range(windows[0][0][0], windows[-1][-1][0], 30):
        plt.axvline(x=i)

    plt.show()


def label_events(windows, diary, event_labels):
    # diary :: [event]
    # event  :: (label, start, end)
    labels = []

    for window in windows:
        # make some decision about which event best represents this window
        # I'll just pick based off of which is most common during this window
        voting = []
        for event in event_labels:
            voting.append(0)
        
        for event in diary:
            start_event = max(event[1], window[0][0])
            end_event = min(event[2], window[-1][0])
            event_length = end_event - start_event

            if event_length < 0:
                continue
            
            window_length = window[-1][0] - window[0][0]

            voting[event[0]] += event_length / window_length
        
        label = voting.index(max(voting))

        labels.append(label)

    return labels


if __name__ == "__main__":
    log_filename = parse_args()
    tags = load_dict(log_filename)

    windows = generate_sliding_windows(tags, '41', 30, 5)

    diary = [
        (0, 0, 120),
        (1, 120, 240),
        (0, 240, 550)
    ]

    event_labels = [0, 1]

    labels = label_events(windows, diary, event_labels)

    for i in range(len(windows)):
        print(windows[i][0][0], windows[i][-1][0], labels[i])

    stripped_windows = []

    for window in windows:
        strip_win = []
        for tup in window:
            strip_win.append(tup[1])
        stripped_windows.append(strip_win)

    classify_knn(stripped_windows, labels)
    classify_forest(stripped_windows, labels)

    # demo_sliding_window(tags)

    # plot(tags)
