queue_push_count = 0

with open('/data/minseokk1m_logs/result_ENHANCE_receiver_4.txt', 'r') as file:
    for line in file:
        if line.strip().startswith("CHILD HASH data of the Node, Child Number#:"):
            queue_push_count += 1

print(f"Total QUEUE PUSH count: {queue_push_count}")
