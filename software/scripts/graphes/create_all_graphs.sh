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
	if [ -d $DIR ] && [ -e $DIR/create_graph.sh ]
	then
		echo "Generating the graphs for $DIR"
	   	 cd $DIR
	    	./create_graph.sh
	fi
done
