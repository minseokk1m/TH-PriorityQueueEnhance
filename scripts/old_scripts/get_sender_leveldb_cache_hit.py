levelDbCacheHitTotalTime = 0
levelDbCacheHitCount = 0

with open('file.txt') as f:
    for line in f:
        if 'CleanCacheHitData: true' in line:
            continue
        if 'LevelDBCacheMiss: true' in line:
            continue
        time_str = line.split('Took time: ')[1].split()[0]
        time = int(time_str)
        levelDbCacheHitTotalTime += time
        levelDbCacheHitCount += 1

if levelDbCacheHitCount == 0:
    print("No rows with LevelDBCacheHit")
else:
    levelDbCacheHitAvgTime = levelDbCacheHitTotalTime / levelDbCacheHitCount
    print(f"Average LevelDBCacheHit Retrieve time: {levelDbCacheHitAvgTime}")
    print(f"Total LevelDBCacheHit levelDbCacheHitCount: {levelDbCacheHitCount}")