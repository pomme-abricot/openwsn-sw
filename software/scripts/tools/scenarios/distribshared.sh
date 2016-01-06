#!/bin/bash




#options
#RPLMETRIC_LIST="1 3 4"
RPLMETRIC_LIST="1 3 4"
RPLMETRIC="3"
SCHEDALGO=2
TRACK=1
TRACK_LIST="0 1"
DCELLS=1

#topology (bottom)
NODE_START=220
NODE_STEP=2
SITE=grenoble

#traffic
TRAFFIC_MSEC=1000               #ms between two packets (from ANY node) 


#experiment
DURATION=30                                    #in minutes
DIRNAME="distribshared"



#one experiment for debug
#export DEBUG=1
#nbnodes=15
#RPLMETRIC=4
#iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC test
#exit



#a list of experiments

for EXP in {0..9}
do
for nbnodes in {8..25..2}
do
	for DCELLS in {0..1}
	do		
		echo "./launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME
	done
done 
done







