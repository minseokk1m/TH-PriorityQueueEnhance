cd go-ethereum
make geth
cd /data/THEnhanceSyncData/
rm -r THblkchain2
geth --datadir THblkchain2 init genesis.json
