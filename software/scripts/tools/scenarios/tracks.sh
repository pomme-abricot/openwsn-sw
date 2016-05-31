#!/bin/bash



#options
RPLMETRIC="1"
SCHEDALGO=2
TRACK=1
TRACK_LIST="0 1 2"
DCELLS=1

#topology
NODE_START=2
NODE_START=17
NODE_STEP=5
SITE=lille

#traffic
TRAFFIC_MSEC=1000		#ms between two packets (from ANY node) 


#experiment
DURATION=60					#in minutes
DIRNAME="tracks"

#one experiment for debug
#export DEBUG=1
#nbnodes=15
#RPLMETRIC=4
#iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC test
#exit



#a list of experiments
for i in {0..8}
do
for nbnodes in {5..50..10}
do
	for TRACK in $TRACK_LIST
	do
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME
	done
done 
done

