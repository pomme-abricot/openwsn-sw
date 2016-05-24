#!/bin/bash



#options
#RPLMETRIC_LIST="1 3 4"
RPLMETRIC_LIST="1 3 4"
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
DURATION=90					#in minutes
DIRNAME="tracks"

#one experiment for debug
#export DEBUG=1
#nbnodes=15
#RPLMETRIC=4
#iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC test
#exit



#a list of experiments
for i in {0..1}
do
for nbnodes in {10..20..10}
do
	for TRACK in $TRACK_LIST
	do
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME
	done
done 
done

