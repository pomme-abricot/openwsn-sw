# Purpose and organization

* graphes: scripts to handle a collection of experiments (i.e. results.csv for each experiment), aggregate the measures, compute the confidence intervals, and generate a single .txt file (matrix of values) which can be directly used by gnuplot
* stats: models of gnuplot files to plot the distributions of delays and packet losses
* tools: to automatize the experiments (reserve the nodes, open ssh tunnels, start openvizualizer, store the results in log files, plot the distribution of delays and packet losses, etc.)


# Installation

You must modify your PATH variable to include both the experiment-cli tools, and the scripts:

```bash
PATH=$PATH:/$HOME/exp-iotlab/openwsn/openwsn-sw/software/scripts/tools:$HOME/exp-iotlab/iot-lab/parts/cli-tools
```

You may find convenient to create a symbolic link in your home directory:

```bash
ln -s /$HOME/exp-iotlab/openwsn/openwsn-sw/software/scripts/ $HOME/
```

Finally, let's create a directory to store the statistics and logs when an experiment is executed on IOTLab:

```bash
mkdir $HOME/stats
```



# Workflow

Let's start a collection of experiments. For instance, we can study the impact of the track management method with a variable number of nodes:

```bash
cd $HOME/scripts/tools/scenarios
./tracks.sh
```

Nothing else to do. Just watch the stdout to verify no error occurs.

After a few hours / days / weeks, let's now take a look at the results. Everying was stored in $HOME/stats. First, let's ask the scripts to parse the log files and compute the statistics (PDR, delay, etc.):


```bash
theoleyre@briconet:~$  cd $HOME/stats/tracks
theoleyre@briconet:~$  owsn_update_stats.sh 
```

You are now able to plot your graphs:


```bash
mkdir $HOME/scripts/graphes/tracks/data/raw/
cp -Rf $HOME/stats/tracks/* $HOME/scripts/graphes/tracks/data/raw/
cd  $HOME/scripts/graphes/
./create_all_graphs.sh
```

If your configuration files are correct, you should now have some new graphs placed in $HOME/scripts/graphes/tracks/



# Detailed description

You may perhaps have to modify the scripts or the configuration files. You can find detailed explanations here:
* measure new metrics, define a new set of experiments: https://github.com/ftheoleyre/openwsn-sw/tree/track/software/scripts/tools
* define new graphs to plot: https://github.com/ftheoleyre/openwsn-sw/tree/track/software/scripts/graphes
