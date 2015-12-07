#!/bin/bash



RPLMETRIC=2
SCHEDALGO=2
TRACK=1
NODESEP=2


#./launch_exp.sh 1 1 2 2 line 5 2 distribshared
#exit

for nbnodes in {8..25..2}
do
	for algo_distrib_cells in {0..1}
	do
		#with tracks, line in Grenoble (on the left), node separation = 4 ids
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared"
		./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared
	done
done 


