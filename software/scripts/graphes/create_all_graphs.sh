#!/bin/bash

#default
CUR_DIR=`pwd`
#the international units
LANG=


#stats compute
cd scripts
./stats_compute.sh 
cd $CUR_DIR

#for each directory
for DIR in *
do
	if [ -d "$DIR" ]
	then
		echo "Generating the graphs for $DIR"
	   	cd $DIR
		create_graph.sh
		cd $CUR_DIR
	else
		echo "does not handle $DIR (non existing)"
	fi
done
