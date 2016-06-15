# Description of the different scripts and their role



## Scenarios 

A scenario corresponds to a set of experiments one variable parameter (=the x-coordinate) and a set of algorithms/parameters to compare (one curve by algorithm/parameter).

Typically, [tools/scenarios/tracks.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/scenarios/tracks.sh) consists in:
* a list of values for each parameters (several values for the x-coordinate, and the algorithms to compare)
* the experiment description (site, the first id to reserve (and the separation between two consecutive motes), the duration)
* the number of exepriments for each set of parameters (to plot confidence intervals and have accurate results)
```bash
for i in {0..8}
do
  [...]
done
``` 
* the parameters which change:
```bash
for nbnodes in {10..60..10}
do
	for TRACK in $TRACK_LIST
  do
      [...]
  done
done
``` 
* the call to [iotlab_launch_exp.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/iotlab_launch_exp.sh) to start the experiment with the correct parameters


## To start an experiment

The script [iotlab_launch_exp.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/iotlab_launch_exp.sh) starts an experiment:

### Preparation

* kill the previous on-going experiments (openvisualizer, ssh, etc.)
* retrieves the parameters from the arguments


### Compilation

* prepares the arguments for the compilation (used by scons to make the corresponding #define)
```bash
HOMEEXP="$HOME/exp-iotlab"
export OPTIONS="distribshared=$DCELL tracks=$TRACK rplmetric=$RPLMETRIC schedalgo=$SCHEDALGO cex_period=$CEXAMPLE_PERIOD printf=$PRINTF"
```
* removes the previous logfile in the build directory
* mirroring the two gits (openwsn-fw + openwsn-fw-sink) to be sure to compile the same version for the DAGroot and the motes
* Compilation of the firmware for the DAG root + the motes

### Logs

The log file is stored in *$HOME/stats/BASENAME* so that a collection of subdirectories contains all the experiments:
* one subdirectoy per set of parameter (the name is directly constructed with the parameters values)
* one subsubdirectory per experiment (the name is randomly generated)


### List of nodes to reserve

The script constructs the list of nodes to reserve:
* the first id is *$NODE_START*
* the difference between the ids of two consecutive motes is equal to *$NODE_STEP*
* we blacklist the dead nodes (different for each site) to be sure to not reserve a dead node (it blocks the experiment)
* reserves the experiment in IoT-Lab (with this list of ids, the site name, the duration, etc.). Uses the standard experiment-cli of the [cli-tools](https://github.com/iot-lab/iot-lab/wiki/CLI-Tools) provided by the IoTLab staff

### Flash

The script calls the Adjih's script to flash the nodes with the correct firmware, re-using automatically the last experiment (we just reserved it)
```bash
$ cd $HOME/expiot/tools
$ python ExpOpenWSN.py
```

### Controls the experiment

* it retrieves the experiment-id (to control it)
* uses Adjih's script for ssh port forwarding
* creates a child to execute openVisualizer in the background (it will automatically use the ssh ports)
* reflashes the motes (unfrequently, the previous flashing procedure failed)
* asks periodically the status of the experiment to IoTLab. While it is not terminated, it loops

### End

* kill the ssh tunnels, openvisualizer, etc.
* calls [owsn_extract_stats_from_log.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/owsn_extract_stats_from_log.sh) to parse the logfile to compute the statistics




## To extract the statistics

[owsn_extract_stats_from_log.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/owsn_extract_stats_from_log.sh} parses a logfile to extract the statistics:
* it retrieves the parameters (should be printed in the logfile)
* extracts the list of nodes with at least one entry (short and long addresses)
* It extracts the stats for each node, considering each packet (sequence number individually)
	* remembers the smallest and largest sequence number
	* aggregates the packets in time intervals (the ASN for the generation is comprised between a min and max value)
		* saves in a vector (with the ASN interval) all the metrics (reception/generation time, etc.)
		* saves in a matric all these values for 
		* a cell in the vector is common to *all* the nodes (e.g. array_pktx[] and array_pkrx[])
	* for each node, saves the metrics for the whole experiments (nb. of packets generated, delay, etc.)
	* it also prints the statistics for each node to have a comprehensive view of the behavior and to track possible bugs / bad behaviors
* computes the average values for all the nodes
* separate the statistics with the metrics between 70% and 80% of the experiments (a time interval during which the experiment has probably converged, and to discard the bootstrap period)

Then it:
* prints the average statistics 
* pushes the list of lost packets + delays in a file to plot a distribution of the packet losses
* stores all the average metrics in *result.csv* in the correct directory
* plots the distributions (for **this** experiment) with the corresponding [templates](https://github.com/ftheoleyre/openwsn-sw/tree/track/software/scripts/stats) 



# Modifications


## To define a new scenario

You have to create a new scenario:
```bash
$ touch scripts/tools/scenarios/new.sh
```

And fill with a correct content. For instance, to measure the impact of different traffic load with different scheduling algorigthms:
```bash
#!/bin/bash



#options
RPLMETRIC="1"			# ETX
SCHEDALGO_LIST="1 2 3"		# Different algorithms
TRACK=1				# one common track with dedicated cells
DCELLS="1"

#topology
NODE_STEP=3			# I will reserve the nodes 2, 5, 8, 11, [..]
SITE=lille			# I reserve the Lille's platform
NODE_START=2			# first mote with id 2
nbnodes=20			# 20 nodes

#traffic
TRAFFIC_MSEC_LIST="1000	2000 3000 5000 10000 20000"		#ms between two packets (from ANY node) 


#experiment
DURATION=60					#in minutes
DIRNAME="traffic"


#a list of experiments
for exp in {0..8}
do
for TRAFFIC_MSEC in $TRAFFIC_MSEC_LIST
do
	for SCHEDALGO in SCHEDALGO_LIST
	do
		echo "iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME"
		iotlab_launch_exp.sh $DCELLS $TRACK $RPLMETRIC $SCHEDALGO $nbnodes $SITE $NODE_START $NODE_STEP $DURATION $TRAFFIC_MSEC $DIRNAME
	done
done 
done

```
And, that's all!



## To define and extract a new metric

You have to have a sufficient number of information in the log file (so, the firmware has to use a function like *openserial_statCelladd* in [openserial.c](https://github.com/ftheoleyre/openwsn-fw/blob/track/drivers/common/openserial.c).

To collect then the number of cells aded in the experiments:
* openVisualizer must print the event in the logfile (e.g. [ParserStat.py]( https://github.com/ftheoleyre/openwsn-sw/blob/track/software/openvisualizer/openvisualizer/moteConnector/ParserStat.py))
```bash
elif (statType == self.SERTYPE_CELL_ADD):
        log.info('STAT_CELL_ADD|addr={0}|comp={1}|asn={2}|statType={3}|trackinstance={4}|trackowner={5}|slotOffset={6}|type={7}|shared={8}|channelOffset={9}|neighbor={10}'.format(
                self.BytesToAddr(addr),
                mycomponent,
                self.BytesToString(asnbytes),
                statType,
                self.BytesToString(input[9:11]),
                self.BytesToAddr(input[11:19]),
                input[19],
                input[20],
                input[21],
                input[22],
                self.BytesToAddr(input[23:31])
)); 
```
* you have to modify [owsn_extract_stats_from_log.sh](https://github.com/ftheoleyre/openwsn-sw/blob/track/software/scripts/tools/owsn_extract_stats_from_log.sh)
* Initialization
```bash
get the list of seqnums for each source
for addr_l in `cat $NODESLIST` 
do
	array_addcells[$addr_s]=`cat $LOGFILE | grep STAT_CELL_ADD | grep "addr=$addr_l" | wc -l`
done
[...]
echo "--------AVG--------"
addCells_avg=0
for i in ${!array_addcells[*]} 
do
	addCells_avg=addCells_avg + array_addcells[i]
done
echo "addCells_avg=$addCells_avg"
```

:heavy_exclamation_mark: I did not test this modification. It contains (probably) some bugs



## To define and extract a new parameter


