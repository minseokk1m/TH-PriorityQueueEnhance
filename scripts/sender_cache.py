# /data/minseokk1m_logs/result_GETH_sender_1.txt

import re
import numpy as np

cache_miss_times = []
cache_hit_times = []

def process_node_read_lines(node_read_lines):
    is_cache_miss = any('CacheMiss: true' in line for line in node_read_lines)
    get_time_line = next((line for line in node_read_lines if 'Gettime elapsed:' in line), None)
    if get_time_line is not None:  # Proceed only if we found a get_time_line
        read_time = parse_get_time(get_time_line)

        if is_cache_miss:
            cache_miss_times.append(read_time)
        else:
            cache_hit_times.append(read_time)


def parse_get_time(line):
    # This will capture any number followed by either 's', 'ms' or 'µs'
    match = re.search(r'(\d+(\.\d+)?)(s|ms|µs)', line)
    if match:
        time, unit = float(match.group(1)), match.group(3)
        if unit == 's':  # convert to ms
            time *= 1000
        elif unit == 'µs':  # convert to ms
            time /= 1000
    return time


with open('/data/minseokk1m_logs/result_ENHANCE_sender_4.txt', 'r') as file:
    node_read_lines = []
    for line in file:
        if "NODE READ from" in line:
            if node_read_lines:  # If we have lines from previous node read, process them
                process_node_read_lines(node_read_lines)
            node_read_lines = []  # Start a new node read
        node_read_lines.append(line.strip())

    # Don't forget to process the last node read
    if node_read_lines:
        process_node_read_lines(node_read_lines)

# After reading and processing the file, you can calculate mean and standard deviation
miss_mean = np.mean(cache_miss_times)
miss_std = np.std(cache_miss_times)
hit_mean = np.mean(cache_hit_times)
hit_std = np.std(cache_hit_times)

print(f"Cache Miss - Occurence: {len(cache_miss_times)} times, Average: {miss_mean} ms, Standard Deviation: {miss_std} ms")
print(f"Cache Hit - Occurence: {len(cache_hit_times)} times, Average: {hit_mean} ms, Standard Deviation: {hit_std} ms")
