#!/bin/bash

rsync -av --delete-after --exclude '.sconsign.dblite' --exclude 'build' --exclude 'projects/common'  $HOME/exp-iotlab/openwsn/openwsn-fw/ $HOME/exp-iotlab/openwsn/openwsn-fw-sink/
