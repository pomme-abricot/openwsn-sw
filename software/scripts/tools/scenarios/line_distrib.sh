#!/bin/bash



#options
RPLMETRIC=2
SCHEDALGO=2
TRACK=1
DCELLS=1

#topology
NODE_START=210
NODE_STEP=2
SITE=grenoble

#traffic
TRAFFIC_MSEC=1000		#ms between two packets (from ANY node) 


#experiment
DURATION=30					#in minutes


#one experiment for debug
#export DEBUG=1
nbnodes=15
RPLMETRIC=4
iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC test
exit



#a list of experiments
for nbnodes in {8..25..2}
do
	for DCELLS in {0..1}
	do		
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC rplmetric"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC rplmetric
	done
done 







