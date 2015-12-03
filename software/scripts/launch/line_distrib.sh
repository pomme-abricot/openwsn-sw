#!/bin/bash


for nbnodes in {2..27..5}
do
	for algo_distrib_cells in {0..1}
	do
		#with tracks, line in Grenoble (on the left), node separation = 4 ids
		./launch_exp.sh $algo_distrib_cells 1 line $nbnodes 4 distrib_cells

	done
done 

