cleanCacheHitTotalTime = 0
cleanCacheHitCount = 0

with open('file.txt') as f:
    for line in f:
        if 'CleanCacheHitData: true' not in line:
            continue
        time_str = line.split('Took time: ')[1].split()[0]
        time = int(time_str)
        cleanCacheHitTotalTime += time
        cleanCacheHitCount += 1

if cleanCacheHitCount == 0:
    print("No rows with CleanCacheHitData = true")
else:
    cleanCacheHitAvgTime = cleanCacheHitTotalTime / cleanCacheHitCount
    print(f"Average CleanCacheHit Retrieve time: {cleanCacheHitAvgTime}")
    print(f"Total CleanCacheHit cleanCacheHitCount: {cleanCacheHitCount}")
    