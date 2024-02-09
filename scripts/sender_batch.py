# /data/minseokk1m_logs/result_GETH_sender_1.txt

import pandas as pd

# Prepare data list
data = []

# Read file
with open('/data/minseokk1m_logs/result_ENHANCE_sender_4.txt', 'r') as f:
    batch_time_line = ''
    for line in f:
        if line.startswith('Batch - current Time:'):
            # Store the batch time line
            batch_time_line = line.strip()
        elif line.startswith('END(Sender)') and batch_time_line:
            # Extract the time from the END(Sender) line
            time_parts = line.split()
            time_str = time_parts[-1]

            try:
                # Remove the 'ms' suffix from the time string
                time_value = time_str[:-2]

                # Convert time value to milliseconds
                time = float(time_value)

                data.append(time)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Occurred for line: {line}")

            # Reset the batch time line
            batch_time_line = ''

if len(data) == 0:
    print("No valid data found!")
else:
    # Convert to dataframe
    df = pd.DataFrame(data, columns=['time'])

    # Print results
    print(len(data))
    print('Time took average time:', df['time'].mean(), 'ms')
    print('Time took standard deviation:', df['time'].std(), 'ms')
