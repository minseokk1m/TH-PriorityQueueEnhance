levelDbCacheMissTotalTime = 0
levelDbCacheMissCount = 0

with open('file.txt') as f:
    for line in f:
        if 'LevelDBCacheMiss: true' not in line:
            continue
        time_str = line.split('Took time: ')[1].split()[0]
        time = int(time_str)
        levelDbCacheMissTotalTime += time
        levelDbCacheMissCount += 1

if levelDbCacheMissCount == 0:
    print("No rows with LevelDBCacheMiss")
else:
    levelDbCacheMissAvgTime = levelDbCacheMissTotalTime / levelDbCacheMissCount
    print(f"Average LevelDBCacheMiss Retrieve time: {levelDbCacheMissAvgTime}")
    print(f"Total LevelDBCacheMiss levelDbCacheMissCount: {levelDbCacheMissCount}")