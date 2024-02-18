cd go-ethereum
make geth
cd /data/THEnhanceSyncData/
rm -r THEnhanceblkchain2
geth --datadir THEnhanceblkchain2 init genesis.json
