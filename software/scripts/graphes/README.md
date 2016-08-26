# Description of the different scripts and their role

## To plot the gnuplot graphs

* common.plt: common gnuplot options (style of lines, etc.)
* [create_all_graphs.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/create_all_graphs.sh): execute scripts/stats_compute.sh and then plot all the graphs (i.e. walks in the directories, and generate the graph associated toeach .graph file)

Usage:
```bash
$ ./create_all_graphs.sh
```

## To compute the statistics

[scripts/stats_compute.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/scripts/stats_compute.sh) computes the aggregated set of values, directly used by gnuplot:
* for each .cnf file, retrieve the parameters (position of the first column, parameters, etc.)
* extracts the position of the first column (X_COORD_POS) and what is the tolerance for the x-axis (i.e. if two rows have a first value difference inferior than X_COORD_AGG, we consider this corresponds to the same parameters) 
* walks in the different subdirectories, extracts the results from the file '''result.csv''' and stores everything in a big matrix (FILE_OUT_AGGREGATED)
* calls [first_col_move.awk](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/scripts/first_col_move.awk) and [compute_avg_and_confidence_intervals.awk](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/scripts/compute_avg_and_confidence_intervals.awk) to order the staististics and to compute the confidence intervals


[scripts/first_col_move.awk](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/scripts/first_col_move.awk) moves the corresponding column at the beginning (i.e. first column)


[scripts/compute_avg_and_confidence_intervals.awk](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/graphes/scripts/compute_avg_and_confidence_intervals.awk) aggregates all the lines with the same first column value (more or less X_COORD_AGG), and computes the average value + the confidence intervals.


Usage:
```bash
$ cd scripts
$ ./stats_compute.sh
```


# new set of Experiments

You may want to define a new set of experiments. Let's imagine you want to chaneg the scheduling algo. You should first create a configuration file:
```bash
$ touch scripts/schedalgo.cnf
```

And you should fill the file with the typical following content:
```bash
#CONFIGURATION FILE TO COMPUTE STATS

#basename to construct filenames, directories, etc.
BASENAME|schedalgo

#go to the correct directory
SUBDIRS_LIST|raw          # all the log files are placed in $BASENAME/data/raw

#the algos
SCHEDALGO_LIST|1 2 3 4 5  # we have here 5 different algorithms to compare
RPLMETRIC_LIST|1          # consider only the ETX metric (default)
DISTRCELLS_LIST|1         # considers only DCELLS=1
TRACK_LIST|1              # considers only the track management method 1

#The column id for the x-coordinate of the graph (i.e. the parameter)
#the load
X_COORD_POS|5             # the x-axis (here, the number of nodes)
X_COORD_AGG|5             # 5 and 7 nodes are considered the same set of parameters (a few nodes have probably crashed)

#Number of columns that are fixed 
NB_FIXED_COLS|5           # the first 5 columns are parameters (and not metrics) -> they are fixed

#Nb of columns (discard lines with less or more values)
NB_OF_COLS|18             # the log file MUST report exactely 18 columns (else, this log file is discarded)

```

You just have now to:
```bash
$ cd scripts/graphes/
$ mkdir -p schedalgo/data
$ cp -Rf YOURSTATS schedalgo/data/raw
* cd ../scripts
$ ./compute_stats.sh
```

You can now verify the directory *schedalgo* contains valid XX.txt files (one file per scheduling algorithm). If someone went wrong, you should be able to notice errors in the stdout.


# new graphs & metrics 

You want to define new graphs to plot. Let's imagine you want to plot the average duplicate ratio (y-coordinates) and the number of nodes (x-coordinates), and you want to compare different scheduling algorithms. You just have to create a new file named *dupratio.graph*:
```bash
load "../common.plt"          #common gnuplot parameters

# legend, labels & axis
set xlabel "Number of nodes"
set ylabel "Duplicate ratio"

#the data
#only the scheduling algorithm changes, the other parameters are fixed
plot "distribshared=1,tracks=2,rplmetric=1,schedalgo=1.txt" using 1:13 title 'Algo 1' ls 1,\
"distribshared=1,tracks=2,rplmetric=1,schedalgo=2.txt" using 1:13 title 'Algo 2' ls 2
```

and the graphs will be automatically plotted when calling:
```bash
$ ./create_all_graphs.sh
```
