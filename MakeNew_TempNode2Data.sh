cd go-ethereum
make geth
cd /data/THEnhanceSyncData/
rm -r tempblkchain2
geth --datadir tempblkchain2 init genesis.json
