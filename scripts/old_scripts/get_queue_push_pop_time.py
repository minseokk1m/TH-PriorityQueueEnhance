import re
import statistics

# Read the file and store the values of "Took time" in a list
took_times = []
with open("/data/trieHashimoto/th_experiment_data_3/logs/batch16/0316_setHead_100000_depth+[0:9]_push.txt", 'r') as f:
    for line in f:
        match = re.search(r'Took time: (\d+)', line)
        if match:
            took_times.append(int(match.group(1)))

# Calculate the average, standard deviation, and maximum
average = statistics.mean(took_times)
stdev = statistics.stdev(took_times)
maximum = max(took_times)

print('Average:', average)
print('Standard deviation:', stdev)
print('Maximum:', maximum)