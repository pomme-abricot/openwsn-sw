#!/bin/bash



if [ $# -ne 8 ]
then
	echo "usage $0 celldistrib trackactive rplmetric schedalgo scenario nbnodes nodesep dirresult"
	exit 3
fi




#VARIABLES
HOMEEXP="$HOME/exp-iotlab"
export OPTIONS="distribshared=$1 tracks=$2 rplmetric=$3 schedalgo=$4"
SITE="grenoble"
DURATION_MIN="30"
DURATION_S=`echo "$DURATION_MIN * 60" | bc`
NBNODES=$6
CURDIR=`pwd`
ASN_AGG=2000
ASN_START=4000

#scenarios
if [ "$5" = "line" ]
then
#left line 96-??
#middle line 207-287
	FIRSTNODE=207		#m3-96 is the first node of the list
	NODESINCR=$7		#select ids with a difference of X		
else 
	echo "unknown scenario ($5)"
	exit 3
fi

FORBIDDEN_NODES="243"


#resync the sink and node firmwares
echo "entering directory $HOMEEXP"
cd $HOMEEXP
./git_mirroring.sh



#build for dag root
echo "entering $HOMEEXP"
cd $HOMEEXP
#make build-openwsn-sink-m3
if [ $? -ne 0 ]
then
	exit 4
fi
#build for nodes
#make build-openwsn-m3





#destination for the logs / results
OPTIONS="${OPTIONS// /,}"
if [ ! -d "$HOME/stats" ]
then
	mkdir "$HOME/stats/"
fi
if [ ! -d "$HOME/stats/$8" ]
then
	mkdir "$HOME/stats/$8"
fi
if [ ! -d "$HOME/stats/$8/$OPTIONS,nbnodes=$NBNODES" ]
then
	mkdir "$HOME/stats/$8/$OPTIONS,nbnodes=$NBNODES"

fi
echo "mktemp -d \"$HOME/stats/$8/$OPTIONS,nbnodes=$NBNODES/XXXXXX\""
LOGDIR=`mktemp -d "$HOME/stats/$8/$OPTIONS,nbnodes=$NBNODES/XXXXXX"`
LOGSUFFIX=`echo $LOGDIR | rev | cut -d "/" -f 1 | rev` 
echo "Push results in directory $LOGDIR"



#stop any other running experiment (silent since we have probably no running experiment here)
echo "experiment-cli -u theoleyr -p x9HBHvm8 stop"
experiment-cli -u theoleyr -p x9HBHvm8 stop 2> /dev/null




#reserve the nodes and : compute the exact list of nodes to reserve
#avoids the blacklisted nodes
#line grenoble : 96-178
NODELIST="$FIRSTNODE"
offset=0
for (( i=1; i<=$NBNODES; i+=1 ))
do
	NODE=`echo "$offset + $i * $NODESINCR + $FIRSTNODE" | bc`
	while [[ $FORBIDDEN_NODES == *"$NODE"* ]] 
	do
		offset=`echo "$offset + 1" | bc`
		NODE=`echo "$offset + $i * $NODESINCR + $FIRSTNODE" | bc`
	done	
	NODELIST="$NODELIST+$NODE"
done


TMPFILE=`mktemp`
echo "experiment-cli -u theoleyr -p x9HBHvm8 submit -n $LOGSUFFIX  -d $DURATION_MIN -l $SITE,m3,$NODELIST"
experiment-cli -u theoleyr -p x9HBHvm8 submit -n $LOGSUFFIX  -d $DURATION_MIN -l $SITE,m3,$NODELIST > $TMPFILE
expid=`cat $TMPFILE | grep id | cut -d ":" -f 2`
echo "Experiment id $expid"


#bug in the reservation
if [ -z "$expid" ]
then
	echo "the reservation failed"
	exit
fi


#wait the experiments has been laucnhed
res=""
while [ -z "$res" ]
do
	res=`experiment-cli -u theoleyr -p x9HBHvm8 get -s -i $expid`
	echo $res
	sleep 1
	res=`echo "$res" | grep "Running"`
done



#flash them
cd $HOMEEXP/tools
echo "entering $HOMEEXP/tools"
echo "python ExpOpenWSN.py" #  --nbnodes $NBNODES --name $LOGSUFFIX --site $SITE --duration $DURATION_MIN"
python ExpOpenWSN.py #--nb-nodes $NBNODES --name $LOGSUFFIX --site $SITE --duration $DURATION_MIN
if [ $? -ne 0 ]
then
	echo "Error: cannot upload the firmware to iotlab"
	exit 3
fi


#launch port forwarding
cd $HOMEEXP/tools
echo "entering $HOMEEXP/tools"
./expctl ssh-forward
sleep 1
./expctl pseudo-tty --all
echo "PID $! $$"


#openvizualizer
cd $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer
echo "$HOMEEXP/openwsn/openwsn-sw/software/openvisualizer"
sudo scons runweb &
CHILD_OPENVIZ=$!
echo "openvizualizer running with pid $CHILD_OPENVIZ"
sleep $DURATION_S
echo "I am now killing openvizualizer, that's the end of the experiment ($DURATION_S seconds)"
sudo kill $CHILD_OPENVIZ



#flush everything
sudo killall python
sudo killall socat
sudo killall ssh
sudo killall sleep
	
echo "experiment-cli -u theoleyr -p x9HBHvm8 stop"
experiment-cli -u theoleyr -p x9HBHvm8 stop



#move the stats (log file)
echo "pushing results to $LOGDIR"
if [ ! -e "$HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log" ]
then
	echo "unexisting logfile - experiment error - $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log"
	exit 2
fi
sudo mv $HOMEEXP/openwsn/openwsn-sw/software/openvisualizer/build/runui/openVisualizer.log $LOGDIR
sudo chown -R $USER $LOGDIR



#compute the graphs
cd $LOGDIR
echo "entering $LOGDIR"
echo "$CURDIR/compute_stats.sh $ASN_START $ASN_AGG openVisualizer.log"
$CURDIR/compute_stats.sh $ASN_START $ASN_AGG openVisualizer.log

#garbage
rm TMPFILE


