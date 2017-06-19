from func_search import *
from func_taux_transm import *
from func_def_class import *
from func_res import *
from func_parsing_logfile import *
from func_parsing_csvfile import *

import os
#import matplotlib.pyplot as plt
import re
import numpy as np
from path import Path
import csv
from pandas import *
import pandas as pd
import sys
import ast


#### PARSING DES LOGS DANS DES SOUS FICHIER TXT
sep_data_addr("data/exp_10.log")
sep_data_event("data/exp_10.log")

#### CREATION DES STRUCT PANDAS
#fichier tx
create_df_tx("data/parsed/event/data_STAT_PK_TX.log")
# fichier rx
create_df_tx("data/parsed/event/data_STAT_PK_RX.log", "data/parsed/event/data_STAT_ACK_RX.log")

df_tx = pd.read_csv(r'data_csv/pkt_tx.csv', dtype=str)
df_tx["numTxAttempts"] = df_tx["numTxAttempts"].astype(int)
df_tx["asn"] = df_tx["asn"].astype(int)

df_rx = pd.read_csv(r'data_csv/pkt_rx.csv', dtype=str)
df_rx["asn"] = df_rx["asn"].astype(int)

#complete le df tx
fill_succes_tx(df_tx,df_rx)

# fichier res
create_df_res("data/parsed/event/data_OTHER_ParserPrintf.log")

df_res = pd.read_csv(r'data_csv/res.csv', dtype=str)

#complete les champs simult des reservations
fill_simult(df_res, df_tx)

