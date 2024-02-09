import re
import matplotlib.pyplot as plt

# Regular expressions
time_regex = re.compile(r'QUEUE PUSH TIME: ([\d.]+)(µs|ns)')
size_regex = re.compile(r'QUEUE PUSH SIZE: (\d+)')

# Moving average parameters
window = 100

# Lists to store values
push_time_values = []
push_size_values = []

# Lists to store moving averages
push_time_avg = []
push_size_avg = []

# Downsampling parameter
N = 10000

# Size threshold for reset
size_threshold = 1000000
reset_flag = False
prev_size = 0  # To store the previous size value

# Read log file and gather queue push data
with open('/data/minseokk1m_logs/result_ENHANCE_receiver_4.txt', 'r') as f:
    time = None
    counter = 0
    for line in f:
        if counter % N == 0 or (time is not None and "QUEUE PUSH SIZE:" in line):
            if "QUEUE PUSH TIME:" in line:
                time_match = time_regex.search(line)
                if time_match is not None:
                    # Convert the time to microseconds
                    time = float(time_match.group(1))
                    if time_match.group(2) == 'ns':
                        time /= 1000  # 1 ns = 0.001 µs

            elif "QUEUE PUSH SIZE:" in line and time is not None:
                size_match = size_regex.search(line)
                if size_match is not None:
                    size = int(size_match.group(1))

                    # If the difference between the previous size and current size is above the threshold, reset the data lists.
                    if prev_size - size >= size_threshold and not reset_flag:
                        push_time_values = []
                        push_size_values = []
                        push_time_avg = []
                        push_size_avg = []
                        reset_flag = True

                    # Add data to lists
                    push_time_values.append(time)
                    push_size_values.append(size)

                    # Calculate moving averages if enough data is available
                    if len(push_time_values) > window:
                        push_time_avg.append(
                            sum(push_time_values[-window:]) / window)
                        push_size_avg.append(
                            sum(push_size_values[-window:]) / window)

                    time = None  # Reset time to ensure proper pairing
                    prev_size = size  # Update the previous size
        counter += 1

# Plotting
plt.figure(figsize=(10, 5))

# Plot for Queue Push Size
plt.plot(push_size_values, label='Size')
plt.plot(push_size_avg, label='Size (Moving Avg.)', color='red')
plt.title('Queue Push - Size')
plt.xlabel('Queue Push Operation Index (x' + str(N) + ')')
plt.ylabel('Size')
plt.legend()
plt.savefig('push_plot_size_ENHANCE_4.png')  # Save the plot to a file

plt.figure(figsize=(10, 5))

# Plot for Queue Push Time
plt.plot(push_time_values, label='Time')
plt.plot(push_time_avg, label='Time (Moving Avg.)', color='red')
plt.title('Queue Push - Time')
plt.xlabel('Queue Push Operation Index (x' + str(N) + ')')
plt.ylabel('Time (µs)')
plt.legend()
plt.savefig('push_plot_time_ENHANCE_4.png')  # Save the plot to a file
