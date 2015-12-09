#!/bin/bash



RPLMETRIC_LIST="1 2 3 4"
SCHEDALGO=2
TRACK=1
NODESEP=2
DCELLS=1


#one experiment for debug
export DEBUG=1
nbnodes=15
RPLMETRIC=1
iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared
exit



#a list of experiments
for nbnodes in {8..25..2}
do
	for RPLMETRIC in $RPLMETRIC_LIST
	do
		#with tracks, line in Grenoble (on the left), node separation = 4 ids
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP rplmetric"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP rplmetric
	done
done 


