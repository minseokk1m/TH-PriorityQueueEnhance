# TH-PriorityQueueEnhance

This is a repository to conduct my(Twitter@minseokk1m)( Master's degree dissertation experiment. This project aims to see the effects of appending a block number prefix to the nodeHash structure of an account-based blockchain during fast-sync.

### 1. Run sender node

Sender node is the node containing the data. Run `run_sender_node.sh` to run the sender node.

### 2.Run receiver node

Receiver node is the node which starts with empty data. It receives data from the sender node by a process called _sync_.

#### (1) If you are dealing with not enhanced version.

Delete the any data of the past and initialize the node with `make_new_receiver_node.sh` and run the node with `run_receiver_node.sh`.

#### (2) If you are dealing with the enhanced version.

Delete the any data of the past and initialize the enhanced node with `make_new_receiver_enhanced_node.sh` and run the node with `run_receiver_enhanced_node.sh`.
