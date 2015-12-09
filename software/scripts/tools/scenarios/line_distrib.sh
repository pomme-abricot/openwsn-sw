#!/bin/bash



RPLMETRIC=2
SCHEDALGO=2
TRACK=1
NODESEP=2
#DCELLS=1


#nbnodes=10
#algo_distrib_cells=1
#RPLMETRIC=3
#./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared
#exit

for nbnodes in {8..25..2}
do
	for DCELLS in {0..1}
	do
		#with tracks, line in Grenoble (on the left), node separation = 4 ids
		echo "iotlab_launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared"
		iotlab_launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared
	done
done 


