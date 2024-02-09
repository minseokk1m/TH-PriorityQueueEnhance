import re
import numpy as np

queue_pop_count = 0
time_regex = re.compile(r'QUEUE POP TIME: (\d+)ns')
pop_time_values = []

with open('/data/minseokk1m_logs/result_ENHANCE_receiver_4.txt', 'r') as file:
    for line in file:
        if line.strip().startswith("QUEUE POP #:"):
            queue_pop_count += 1
        elif "QUEUE POP TIME:" in line:
            time_match = time_regex.search(line)
            if time_match is not None:
                time = int(time_match.group(1))
                pop_time_values.append(time)

print(f"Total QUEUE POP count: {queue_pop_count}")

# Calculate the mean and standard deviation
mean_pop_time = np.mean(pop_time_values)
std_pop_time = np.std(pop_time_values)

print(f"Mean QUEUE POP Time: {mean_pop_time}ns")
print(f"Standard Deviation of QUEUE POP Time: {std_pop_time}ns")
