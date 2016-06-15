# Description of the different scripts and their role

## To plot the gnuplot graphs

* common.plt: common gnuplot options (style of lines, etc.)
* create_all_graphs.sh: execute scripts/stats_compute.sh and then plot all the graphs (i.e. walks in the directories, and generate the graph associated toeach .graph file)

Usage:
```bash
$ ./create_all_graphs.sh
```

## To compute the statistics

*scripts/stats_compute.sh** computes the aggregated set of values, directly used by gnuplot:
* for each .cnf file, retrieve the parameters (position of the first column, parameters, etc.)
* extracts the position of the first column (X_COORD_POS) and what is the tolerance for the x-axis (i.e. if two rows have a first value difference inferior than X_COORD_AGG, we consider this corresponds to the same parameters) 
* walks in the different subdirectories, extracts the results from the file '''result.csv''' and stores everything in a big matrix (FILE_OUT_AGGREGATED)
* calls '''first_col_move.awk''' and '''compute_avg_and_confidence_intervals.awk''' to order the staististics and to compute the confidence intervals


**scripts/first_col_move.awk** moves the corresponding column at the beginning (i.e. first column)


**scripts/compute_avg_and_confidence_intervals.awk** aggregates all the lines with the same first column value (more or less X_COORD_AGG), and computes the average value + the confidence intervals.


Usage:
```bash
$ cd scripts
$ ./stats!compute.sh
```

# new set of Experiments

You may modify the 


# new graphs & metrics 

