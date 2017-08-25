# -*-coding:Latin-1 -*

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

from func_search import *
from func_taux_transm import *
from func_def_class import *
from func_res import *
from func_parsing_logfile import *
from func_parsing_csvfile import *

def parse(file_raw_data):
    
    LOG_FILE = "data/"+file_raw_data+".log"
    PK_TX_FILE = "data/parsed/"+file_raw_data+"/event/STAT_PK_TX.log"
    PK_RX_FILE = "data/parsed/"+file_raw_data+"/event/STAT_PK_RX.log"
    ACK_FILE = "data/parsed/"+file_raw_data+"/event/STAT_ACK.log"
    RES_FILE = "data/parsed/"+file_raw_data+"/event/STAT_6PCMD.log"
    CELL_FILE = "data/parsed/"+file_raw_data+"/event/STAT_CELL.log"
    
    TX_CSV='data_csv/'+file_raw_data+'_pkt_tx.csv'
    RX_CSV='data_csv/'+file_raw_data+'_pkt_rx.csv'
    RES_CSV='data_csv/'+file_raw_data+'_res.csv'
    PARENT_CSV='data_csv/'+file_raw_data+'_parent.csv'
    SONS_CSV='data_csv/'+file_raw_data+'_sons.csv'
    PKT_RES='data_csv/'+file_raw_data+'_pkt_res.csv'
    
    print "starting parsing file : ", LOG_FILE, "... "
    #### PARSING DES LOGS DANS DES SOUS FICHIER TXT
    sep_data_addr(file_raw_data)
    sep_data_event(file_raw_data)
    
    print "file parsed \nStarting to create dataframe ... "
    #### CREATION DES STRUCT PANDAS
    #fichier tx
    df_tx = create_df_tx(PK_TX_FILE)
    df_tx.to_csv(TX_CSV,index=False)

    # fichier rx
    df_rx = create_df_rx(PK_RX_FILE, ACK_FILE)
    df_rx.to_csv(RX_CSV,index=False)
    
    print "dataframes TX and RX done"
    #Change some columns type for the nexts operations
    df_tx["asn"] = df_tx["asn"].astype(int)
    df_tx["numTxAttempts"] = df_tx["numTxAttempts"].astype(int)
    df_tx = df_tx.fillna('')
    df_rx["asn"] = df_rx["asn"].astype(int)

    #fill the reception columns in the tx df to know what paquet was received and ACK
    df_tx = fill_succes_tx(df_tx,df_rx)
    df_tx.to_csv(TX_CSV,index=False)

    # fichiers res
    df_res=create_df_res(RES_FILE)
    df_res=fill_succes_id(df_res)
    #df_res=set_state(df_res)
    df_res.to_csv(RES_CSV,index=False)
    print "dataframe res done"

    #créer les fichiers parent et fils 
    df_parent = create_df_parent(CELL_FILE)
    df_parent = df_parent.drop_duplicates()
    df_parent = df_parent.reset_index(drop=True)
    df_parent.to_csv(PARENT_CSV,index=False)

    df_parent["asn"] = df_parent["asn"].astype(int)
    df_parent = df_parent.fillna('')

    df_fils = create_df_sons(df_parent)
    df_fils.to_csv(SONS_CSV,index=False)
    
    print "dataframe parent and sons done"
    
    df = add_paquet(df_res)
    df.sort_values(['asn'], ascending=[True], inplace=True)
    df = df.fillna('')
    df = df.reset_index(drop=True)
    df.to_csv(PKT_RES,index=False)
    
    return