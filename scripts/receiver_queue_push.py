import re
import numpy as np
from collections import defaultdict

# Initialize dictionary to store time values for each priority
priority_times = defaultdict(list)
overall_times = []

# Size threshold for detecting a drop
size_threshold = 1000000
reset_flag = False
previous_size = 0  # To store the previous size value


def parse_queue_push(lines):
    global reset_flag
    global previous_size

    time_line = lines[2]
    priority_line = lines[1]
    size_line = lines[3]

    time_match = re.search(r'(\d+(\.\d+)?)(µs|ns)', time_line)
    priority_match = re.search(r'Priority: (\d+)', priority_line)
    size_match = re.search(r'QUEUE PUSH SIZE: (\d+)', size_line)

    if time_match and priority_match and size_match:
        time_value, _, time_unit = time_match.groups()
        # Convert to nanoseconds if needed
        time_ns = float(time_value) * (1e3 if time_unit == 'µs' else 1)
        priority = int(priority_match.group(1))
        size = int(size_match.group(1))

        # If the difference between the previous size and current size is above the threshold, reset the data lists.
        if previous_size - size > size_threshold and not reset_flag:
            priority_times.clear()
            overall_times.clear()
            reset_flag = True  # Avoid resetting data multiple times

        priority_times[priority].append(time_ns)
        overall_times.append(time_ns)

        # Update the previous_size
        previous_size = size


with open('/data/minseokk1m_logs/result_GETH_receiver_1.txt', 'r') as file:
    queue_push_lines = []
    for line in file:
        if line.strip().startswith("QUEUE PUSH"):
            queue_push_lines.append(line.strip())
            if len(queue_push_lines) == 4:  # We have a complete QUEUE PUSH block
                parse_queue_push(queue_push_lines)
                queue_push_lines = []  # Reset for the next block

# After reading and processing the file, you can calculate mean and standard deviation
if overall_times:  # Check if overall_times is not empty to avoid division by zero
    overall_mean = np.mean(overall_times)
    overall_std = np.std(overall_times)
    print(
        f"Overall Occurrence: {len(overall_times)} times, Overall Average: {overall_mean} ns, Overall Standard Deviation: {overall_std} ns")
else:
    print("No data points after the size drop.")


# Calculate mean and std dev for each priority
# for priority, times in priority_times.items():
#     mean = np.mean(times)
#     std_dev = np.std(times)
#     print(
#         f"Priority {priority} - Occurence: {len(times)} times, Average: {mean} ns, Standard Deviation: {std_dev} ns")
