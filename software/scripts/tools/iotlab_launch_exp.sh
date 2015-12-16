#!/bin/bash

#DEBUG=1
#FORBIDDEN_NODES="243 256 239"		#DEAD nodes in iotlab
FORBIDDEN_NODES="243 256 239 319 335 351 356"

if [ $# -ne 11 ]
then
	echo "usage $0 celldistrib trackactive rplmetric schedalgo nbnodes site nodestart nodestep duration traffic_sec dirresult"
	exit 3
fi


#flush everything
sudo killall /usr/bin/python > /dev/null 2> /dev/null
sudo killall socat > /dev/null 2> /dev/null
sudo killall ssh > /dev/null 2> /dev/null
sudo killall sleep > /dev/null 2> /dev/null
 

#VARIABLES
CURDIR=`pwd`
ASN_AGG=2000
ASN_START=4000


#PARAMS
DCELL=$1
TRACK=$2
RPLMETRIC=$3
SCHEDALGO=$4


#topology
#line grenoble : 96-178
NBNODES=$5
SITE=$6
NODE_START=$7
NODE_STEP=$8
DURATION_MIN=$9


#Traffic
CEXAMPLE_PERIOD=`echo "${10} * $NBNODES" | bc`		#one packet every nb_nodes seconds 


#DIRS
DIRRES=${11}



#arguments to compile the firmware
HOMEEXP="$HOME/exp-iotlab"
export OPTIONS="distribshared=$DCELL tracks=$TRACK rplmetric=$RPLMETRIC schedalgo=$SCHEDALGO cex_period=$CEXAMPLE_PERIOD"


#removes the previous logfile
echo "removes the previous logfile $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log"
sudo rm -f $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log





#stop any other running experiment (silent since we have probably no running experiment here)
#if [ -z "$DEBUG" ]
#then 
#echo "experiment-cli stop"
#	experiment-cli stop 2> /dev/null
#fi


#resync the sink and node firmwares
echo "entering directory $HOMEEXP"
cd $HOMEEXP
./git_mirroring.sh



#build for dag root
echo "entering $HOMEEXP"
echo "Buiding OpenWSN"
cd $HOMEEXP
if [ -z "$DEBUG" ]
then 
	make build-openwsn-sink-m3 > /dev/null 2> /dev/null
else
	make build-openwsn-sink-m3
fi
if [ $? -ne 0 ]
then
	exit 4
fi
#build for nodes
make build-openwsn-m3 > /dev/null 2> /dev/null




#destination for the logs / results
OPTIONS="${OPTIONS// /,}"
if [ ! -d "$HOME/stats" ]
then
	mkdir "$HOME/stats/"
fi
if [ ! -d "$HOME/stats/$DIRRES" ]
then
	mkdir "$HOME/stats/$DIRRES"
fi
if [ ! -d "$HOME/stats/$DIRRES/$OPTIONS,nbnodes=$NBNODES" ]
then
	mkdir "$HOME/stats/$DIRRES/$OPTIONS,nbnodes=$NBNODES"

fi
echo "mktemp -d \"$HOME/stats/$DIRRES/$OPTIONS,nbnodes=$NBNODES/XXXXXX\""
LOGDIR=`mktemp -d "$HOME/stats/$DIRRES/$OPTIONS,nbnodes=$NBNODES/XXXXXX"`
LOGSUFFIX=`echo $LOGDIR | rev | cut -d "/" -f 1 | rev` 
echo "Push results in directory $LOGDIR"







#reserve the nodes and : compute the exact list of nodes to reserve
#avoids the blacklisted nodes
NODELIST="$NODE_START"
offset=0
for (( i=1; i<=$NBNODES; i+=1 ))
do
	NODE=`echo "$offset + $i * $NODE_STEP + $NODE_START" | bc`
	while [[ $FORBIDDEN_NODES == *"$NODE"* ]] 
	do
		offset=`echo "$offset + 1" | bc`
		NODE=`echo "$offset + $i * $NODE_STEP + $NODE_START" | bc`
	done	
	NODELIST="$NODELIST+$NODE"
done




#START an experiment
if [ -z "$DEBUG" ]
then 
	TMPFILE=`mktemp`
	echo "experiment-cli submit -n $LOGSUFFIX -d $DURATION_MIN -l $SITE,m3,$NODELIST"
	experiment-cli submit -n $LOGSUFFIX -d $DURATION_MIN -l $SITE,m3,$NODELIST > $TMPFILE
	cat $TMPFILE
	expid=`cat $TMPFILE | grep id | cut -d ":" -f 2`
	echo "Experiment id $expid"


	#bug in the reservation
	if [ -z "$expid" ]
	then
		echo "the reservation failed, removes $LOGDIR"
		rm -Rf $LOGDIR
		exit
	fi
	
	#wait the experiments has been launched
	res=""
	while [ -z "$res" ]
	do
		res=`experiment-cli get -s -i $expid`
		echo $res
		sleep 1
		res=`echo "$res" | grep "Running"`
	done
fi
	



#flash them (if DEBUG activated, get a currently existing experiment)
cd $HOMEEXP/tools
echo "entering $HOMEEXP/tools"
CMD="python ExpOpenWSN.py"
echo "$CMD"
$CMD

if [ $? -ne 0 ]
then
	echo "Error: cannot upload the firmware to iotlab, removes $LOGDIR"
	rm -Rf $LOGDIR
	exit 3
fi



#retrieves the experiment-id (from pyhton ExpOpenWSN - debug mode)
if [ ! -z "$DEBUG" ]
then
	tmp=`ls -l Experiment-Last` 	
	expid=`echo $tmp | rev | cut -d ">" -f 1 | rev | cut -d "-" -f 2`	
	echo "expid $exp_id"
fi




#launch port forwarding (by default, uses the last experiment-id)
cd $HOMEEXP/tools
echo "entering $HOMEEXP/tools"
./expctl ssh-forward
sleep 1
./expctl pseudo-tty --all
echo "PID $! $$"


#waits the port forwarding actually works
sleep 1






#openvizualizer
cd $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer
echo "$HOMEEXP/openwsn/openwsn-sw/software/openvisualizer"
sudo scons runweb &
CHILD_OPENVIZ=$!
echo "openvizualizer running with pid $CHILD_OPENVIZ"





#reset (sometimes, the network doesnt boot)
if [ -z "$DEBUG" ]
then
	sleep 3
	echo "Reseting the nodes: node-cli -i $expid -r"
    node-cli -i $expid -r
fi






#wait the experiments has been terminated
res=""
while [ -z "$res" ]
do
	res=`experiment-cli get -s -i $expid`
	echo $res
	sleep 60
	res=`echo "$res" | grep "Terminated\|Error"`
done





#end of the experiment
echo "I am now killing openvizualizer"
sudo kill $CHILD_OPENVIZ





#flush everything
sudo killall /usr/bin/python
sudo killall socat
sudo killall ssh
sudo killall sleep
	
	
	
#echo "xperiment-cli stop"
#experiment-cli stop





#move the stats (log file)
echo "pushing results to $LOGDIR"
if [ ! -e "$HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log" ]
then
	echo "unexisting logfile - experiment error - $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log - statdir $LOGDIR"
	rm -Rf $LOGDIR
	exit 2
fi
sudo mv $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log $LOGDIR
sudo chown -R $USER $LOGDIR



#compute the graphs
cd $LOGDIR
echo "entering $LOGDIR"
echo "owsn_extract_stats_from_log.sh $ASN_START $ASN_AGG openVisualizer.log"
owsn_extract_stats_from_log.sh $ASN_START $ASN_AGG openVisualizer.log

#garbage
rm -f TMPFILE


