#!/bin/bash 

cd openwsn

for file in  openwsn-fw openwsn-fw-sink openwsn-sw
do
	echo "git pull $file"
	cd $file 
	git pull
	cd ..
done
