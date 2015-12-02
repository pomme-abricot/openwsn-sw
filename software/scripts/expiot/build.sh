#!/bin/bash

#rsync synchro for the dagroot and node code
./git_mirroring.sh


#build for dag root
make build-openwsn-sink-m3-test
if [ $? -ne 0 ]
then
	exit 4
fi

#build for nodes
make build-openwsn-m3-test



