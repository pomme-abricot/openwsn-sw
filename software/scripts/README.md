# PREPARATION

theoleyre@briconet:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/theoleyre/scripts/tools:/home/theoleyre/exp-iotlab/iot-lab/parts/cli-tools

theoleyre@briconet:~$ ls -l $HOME
scripts -> exp-iotlab/openwsn/openwsn-sw/software/scripts/

theoleyre@briconet:~$ mkdir $HOME/stats


# EXECUTION

cd $HOME/scripts/tools/scenarios
./tracks.sh



# STATS
theoleyre@briconet:~$  cd $HOME/stats/tracks
theoleyre@briconet:~$  owsn_update_stats.sh 

#GRAPHS
theoleyre@briconet:~$  cp $HOME/stats/tracks/*
theoleyre@briconet:~$  
