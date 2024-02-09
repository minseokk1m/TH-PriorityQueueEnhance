# /data/minseokk1m_logs/result_GETH_sender_1.txt

import pandas as pd

# conversion factors to convert time to milliseconds
time_conversion = {
    's': 1000,
    'ms': 1,
    'us': 0.001,
}

# Prepare data list
data = []

# Read file
with open('/data/minseokk1m_logs/result_ENHANCE_sender_4.txt', 'r') as f:
    for line in f:
        # Check if line starts with 'Batch - Total time for batch retrieval:'
        if line.startswith('Batch - Total time for batch retrieval:'):
            parts = line.split()
            time_str = parts[-1]

            # Check if the last character is a non-digit
            if not time_str[-1].isdigit():
                time_value = time_str[:-2]
                time_unit = time_str[-2:]
            else:
                time_value = time_str
                time_unit = None

            try:
                if time_unit == 's':
                    # Convert time value to milliseconds
                    time = float(time_value) * time_conversion['s']
                elif time_unit == 'ms':
                    # Convert time value to milliseconds
                    time = float(time_value) * time_conversion['ms']
                elif time_unit == 'us':
                    # Convert time value to milliseconds
                    time = float(time_value) * time_conversion['us']
                else:
                    # No unit specified, convert time value to milliseconds
                    time = float(time_value)

                data.append(time)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Occurred for line: {line}")

if len(data) == 0:
    print("No valid data found!")
else:
    # Convert to dataframe
    df = pd.DataFrame(data, columns=['time'])

    # Print results
    print(len(data))
    print('Batch retrieval(Read LEVELDB) average time:', df['time'].mean(), 'ms')
    print('Batch retrieval(Read LEVELDB) standard deviation:', df['time'].std(), 'ms')

