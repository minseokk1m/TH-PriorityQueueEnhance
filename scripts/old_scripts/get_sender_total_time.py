total_took_time = 0

with open("/data/trieHashimoto/th_experiment_data_3/logs/batch16/0316_setHead_100000_depth+[0:9]_sender.txt", "r") as file:
    for line in file:
        words = line.split()
        try:
            took_time = int(words[7])

        except (IndexError, ValueError):
            # Skip over any rows that are not formatted correctly
            continue
        total_took_time += took_time

print(f"The sum of all 'Took time' values is: {total_took_time}")