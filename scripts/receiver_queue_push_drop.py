import re

size_regex = re.compile(r'QUEUE POP SIZE: (\d+)')

previous_size = None
decrease_found = False

# Read log file and gather queue pop data
with open('/data/minseokk1m_logs/result_ENHANCE_receiver_2.txt', 'r') as f:
    line_number = 0
    for line in f:
        line_number += 1
        if "QUEUE POP SIZE:" in line:
            size_match = size_regex.search(line)
            if size_match is not None:
                size = int(size_match.group(1))

                # Check if the current size is smaller than the previous one by more than 1e7
                if previous_size is not None and previous_size - size > 1e7:
                    print(f"The queue size decreased by more than 1e7 for the first time at line {line_number}.")
                    print(f"Previous size: {previous_size}, Current size: {size}")
                    decrease_found = True
                    break
                
                # Update previous_size
                previous_size = size

    if not decrease_found:
        print("The queue size never decreased by more than 1e7 in the log file.")
