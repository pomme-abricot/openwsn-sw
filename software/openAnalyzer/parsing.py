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
create_df_rx("data/parsed/event/data_STAT_PK_RX.log", "data/parsed/event/data_STAT_ACK_RX.log")

df_tx = pd.read_csv(r'data_csv/pkt_tx.csv', dtype=str)
df_tx["asn"] = df_tx["asn"].astype(int)
df_tx["numTxAttempts"] = df_tx["numTxAttempts"].astype(int)
df_tx["trackinstance"] = df_tx["trackinstance"].astype(int)
df_tx = df_tx.fillna('')

df_rx = pd.read_csv(r'data_csv/pkt_rx.csv', dtype=str)
df_rx["asn"] = df_rx["asn"].astype(int)


#creer la df qui contient les infos sur les res
create_df_step_res("data/parsed/event/data_OTHER_ParserPrintf.log")

# fichiers res
create_df_res("data/parsed/event/data_OTHER_ParserPrintf.log")

df_res = pd.read_csv(r'data_csv/res.csv', dtype=str)
df_res["numAttempts"] = df_res["numAttempts"].astype(int)
#df_res["nb_sibl"] = df_res["nb_sibl"].astype(int)
df_res["succes"] = df_res["succes"].astype(int)
df_res["state"] = df_res["state"].astype(int)
df_res["asn creation"] = df_res["asn creation"].astype(int)
df_res = df_res.fillna('')
df_res.sort_values(['asn creation', 'asn_req'], ascending=[True, True], inplace=True)

#complete le df tx
fill_succes_tx(df_tx,df_rx)

#créer les fichiers parent et fils 
create_df_parent("data/parsed/event/data_OTHER_ParserPrintf.log")

df_parent = pd.read_csv(r'data_csv/parent.csv', dtype=str)
df_parent["asn"] = df_parent["asn"].astype(int)
df_parent = df_parent.fillna('')

create_df_sons(df_parent)

df_fils = pd.read_csv(r'data_csv/sons.csv', dtype=str)
df_fils["asn"] = df_fils["asn"].astype(int)

# a lancer après les siblings et qu'UNE fois 
fill_simult(df_res, df_tx)