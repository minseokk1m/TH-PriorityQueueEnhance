import re
import numpy as np

# Regular expressions
start_regex = re.compile(r"START\(RECEIVER\) \\+ d.deliver() \\+")
end_regex = re.compile(r"END\(RECEIVER\) /+")
push_time_regex = re.compile(r'QUEUE PUSH TIME: (\d+)ns')
pop_time_regex = re.compile(r'QUEUE POP TIME: (\d+)ns')

# Initialize variables
in_batch = False
push_time_sum = 0
pop_time_sum = 0
total_time_sums = []  # to store the total queue operation time for each batch

with open('/data/minseokk1m_logs/result_ENHANCE_receiver_4.txt', 'r') as file:
    for line in file:
        if start_regex.search(line):
            # Reset sums at start of batch
            in_batch = True
            push_time_sum = 0
            pop_time_sum = 0
        elif end_regex.search(line):
            # Record total queue operation time at end of batch
            in_batch = False
            total_time_sums.append(push_time_sum + pop_time_sum)
        elif in_batch:
            # Add push and pop times to current batch sum
            push_match = push_time_regex.search(line)
            if push_match:
                push_time_sum += int(push_match.group(1))
            pop_match = pop_time_regex.search(line)
            if pop_match:
                pop_time_sum += int(pop_match.group(1))

# Convert list to NumPy array for easy calculation
total_time_sums = np.array(total_time_sums)

# Calculate the mean and standard deviation
mean_total_time_sum = np.mean(total_time_sums)
std_total_time_sum = np.std(total_time_sums)

print(f"How many batches: {len(total_time_sums)}")
print(f"Mean of total Queue Operation Time per batch: {mean_total_time_sum}ns")
print(f"Standard Deviation of total Queue Operation Time per batch: {std_total_time_sum}ns")
