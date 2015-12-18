#!/bin/bash

#default
CUR_DIR=`pwd`
#the international units
LANG=


#stats compute
cd scripts
./stats_compute.sh $1
cd $CUR_DIR

#for each directory
if [ -z $1 ]
then
    pattern="*"
else
    pattern="$1*"
fi

for DIR in "$1"*
do
    echo "Directory: $DIR"
	if [ -d "$DIR" ]
	then
		echo ".... Generating the graphs"
	   	cd $DIR
		create_graph.sh
		cd $CUR_DIR
	else
        echo "Unexisting directory"
	fi
done
