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


def parse_queue_pop(lines):
    global reset_flag
    global previous_size

    priority_line = lines[2]
    time_line = lines[3]
    size_line = lines[4]

    priority_match = re.search(r'QUEUE POP Priority: (\d+)', priority_line)
    time_match = re.search(r'QUEUE POP TIME: (\d+(\.\d+)?)(µs|ns)', time_line)
    size_match = re.search(r'QUEUE POP SIZE: (\d+)', size_line)

    if priority_match and time_match and size_match:
        priority = int(priority_match.group(1))
        time_value, _, time_unit = time_match.groups()
        # Convert to nanoseconds if needed
        time_ns = float(time_value) * (1e3 if time_unit == 'µs' else 1)
        size = int(size_match.group(1))

        if previous_size - size > size_threshold and not reset_flag:
            priority_times.clear()
            overall_times.clear()
            reset_flag = True  # Avoid resetting data multiple times

        priority_times[priority].append(time_ns)
        overall_times.append(time_ns)

        previous_size = size  # Update the previous size


with open('/data/minseokk1m_logs/result_ENHANCE_receiver_4.txt', 'r') as file:
    inside_queue_pop_block = False
    queue_pop_lines = []

    for line in file:
        stripped_line = line.strip()

        if "QUEUE POP #:" in stripped_line:
            inside_queue_pop_block = True
            queue_pop_lines = [stripped_line]
            continue

        if inside_queue_pop_block:
            queue_pop_lines.append(stripped_line)

            if len(queue_pop_lines) == 5:
                parse_queue_pop(queue_pop_lines)
                inside_queue_pop_block = False
                queue_pop_lines = []

# After reading and processing the file, calculate mean and standard deviation
if overall_times:
    overall_mean = np.mean(overall_times)
    overall_std = np.std(overall_times)
    print(
        f"Overall Occurrence: {len(overall_times)} times, "
        f"Overall Average: {overall_mean} ns, "
        f"Overall Standard Deviation: {overall_std} ns"
    )

    # for priority, times in priority_times.items():
    #     priority_mean = np.mean(times)
    #     priority_std = np.std(times)
    #     print(
    #         f"Priority: {priority}, "
    #         # if you also want to print occurrences per priority
    #         f"Occurrence: {len(times)} times, "
    #         f"Average: {priority_mean} ns, "
    #         f"Standard Deviation: {priority_std} ns"
    #     )
else:
    print("No valid 'QUEUE POP' entries found in the log file.")


# Calculate mean and std dev for each priority
# for priority, times in priority_times.items():
#     mean = np.mean(times)
#     std_dev = np.std(times)
#     print(f"Priority {priority} - Occurence: {len(times)} times, Average: {mean} ns, Standard Deviation: {std_dev} ns")
