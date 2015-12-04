#!/bin/bash



RPLMETRIC=2
SCHEDALGO=2
TRACK=1
NODESEP=4

for zz in {1..3..1}
do

for nbnodes in {12..27..5}
do
	for algo_distrib_cells in {0..1}
	do
		#with tracks, line in Grenoble (on the left), node separation = 4 ids
		echo "./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared"
		./launch_exp.sh $algo_distrib_cells $TRACK $RPLMETRIC $SCHEDALGO line $nbnodes $NODESEP distribshared
	done
done 

done
