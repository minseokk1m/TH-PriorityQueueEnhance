# /data/minseokk1m_logs/result_GETH_receiver_1.txt
# /data/minseokk1m_logs/result_ENHANCE_receiver_4.txt

import re
import numpy as np
import matplotlib.pyplot as plt

start_regex = re.compile(r"\s*@@@@@@@@@ msg.Code == NodeDataMsg:")
end_regex = re.compile(r"\s*END\(RECEIVER\) //////////////////////////////////////////////////////////////////////////// Time took (\d+.\d+)(\w+)")
push_regex = re.compile(r"\s*QUEUE PUSH TIME: (\d+\.?\d*)(\w+)?")
pop_regex = re.compile(r"\s*QUEUE POP TIME: (\d+\.?\d*)(\w+)?")

conversion_table = {'ns': 1e-9, 'µs': 1e-6, 'us': 1e-6, 'ms': 1e-3, 's': 1}

batch_times = []

with open('/data/minseokk1m_logs/result_ENHANCE_receiver_depth+blockNum.txt', 'r') as file:
    total_time = 0
    in_batch = False
    batch_count = 0

    for line in file:
        if start_regex.match(line):
            in_batch = True
            batch_count+=1
        elif end_regex.match(line):
            match = end_regex.match(line)
            time, unit = match.groups()
            total_time += float(time) * conversion_table[unit]
            batch_times.append(total_time)
            in_batch = False
            total_time = 0
        elif in_batch:
            if push_regex.match(line):
                match = push_regex.match(line)
            elif pop_regex.match(line):
                match = pop_regex.match(line)
            else:
                continue

            time, unit = match.groups()
            total_time += float(time) * conversion_table[unit]

if batch_times:
    batch_times = np.array(batch_times)
    with open('/home/minseokk1m/TH-PriorityQueueEnhance/scripts/depth+blockNum_output.txt', 'w') as output_file:
        output_file.write(f"Array: {len(batch_times)}\n")
        output_file.write(f"Mean of total Queue Operation Time per batch: {np.mean(batch_times)}s\n")
        output_file.write(f"Standard Deviation of total Queue Operation Time per batch: {np.std(batch_times)}s\n")

    # Plotting line plot
    plt.plot(batch_times)
    plt.title('Queue Operation Time per Batch')
    plt.xlabel('Batch Number')
    plt.ylabel('Time (s)')
    plt.savefig('/home/minseokk1m/TH-PriorityQueueEnhance/scripts/batch_times_plot_depth+blockNum.png')  # save figure to file
else:
    with open('/home/minseokk1m/TH-PriorityQueueEnhance/scripts/depth+blockNum_output.txt', 'w') as output_file:
        output_file.write("No batch times recorded.\n")
