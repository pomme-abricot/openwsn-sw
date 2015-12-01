#!/bin/bash



if [ $# -ne 2 ]
then
	echo "usage $0 arecelldistrib trackactive"
	exit 3
fi




#VARIABLES
HOMEEXP="$HOME/exp-iotlab"
export OPTIONS="distribshared=$1 tracks=$2"
SITE="strasbourg"
DURATION_MIN="2"
DURATION_S=`echo "$DURATION_MIN * 60" | bc`
NBNODES=2
CURDIR=`pwd`



#build for dag root
echo "entering $HOMEEXP"
cd $HOMEEXP
make build-openwsn-sink-m3
if [ $? -ne 0 ]
then
	exit 4
fi
#build for nodes
make build-openwsn-m3





#destination for the logs / results
OPTIONS="${OPTIONS// /-}"
if [ ! -d "$HOME/stats" ]
then
	mkdir "$HOME/stats/"
fi
if [ ! -d "$HOME/stats/$OPTIONS" ]
then
	mkdir "$HOME/stats/$OPTIONS"

fi
LOGDIR=`mktemp -d "$HOME/stats/$OPTIONS/XXXXXX"`
LOGSUFFIX=`echo $LOGDIR | rev | cut -d "/" -f 1 | rev` 
echo "Push results in directory $LOGDIR"




#reserve the nodes and flash them
cd $HOMEEXP/tools
echo "entering $HOMEEXP/tools"
echo "python ExpOpenWSN.py --nb-nodes $NBNODES --name $LOGSUFFIX --site $SITE --duration $DURATION_MIN"
python ExpOpenWSN.py --nb-nodes $NBNODES --name $LOGSUFFIX --site $SITE --duration $DURATION_MIN
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
echo "$CURDIR/../stats/compute_stats.sh 0 500 openVisualizer.log"
$CURDIR/../stats/compute_stats.sh 0 500 $LOGDIR/openVisualizer.log




