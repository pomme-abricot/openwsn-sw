# -*-coding:Latin-1 -*

import re
import pandas as pd



#def create_df_tx(data_file_tx):

#def create_df_rx(data_file_tx, data_file_ack_rx):

#def fill_succes_tx(df_tx, df_rx):

    
def create_df_tx(data_file_tx):
    df = pd.DataFrame(columns=('time', 'addr', 'comp','asn', 'statType', 'trackinstance', 'trackowner', 'length', 'frameType', 'slotOffset', 'frequency', 'l2Dest', 'txpower', 'numTxAttempts', 'queuePos','succes_rx', 'succes_ack', 'list_rx'))

    i=0
    with open(data_file_tx, "r") as f_tx:
        for line in f_tx:
            df.loc[i]=[get_time(line), 
                    get_addr(line), 
                    get_comp(line), 
                    get_asn(line), 
                    get_statType(line), 
                    get_trackinstance(line), 
                    get_trackowner(line), 
                    get_length(line), 
                    get_frameType(line), 
                    get_slotOffset(line), 
                    get_frequency(line), 
                    get_l2Dest(line), 
                    get_txpower(line), 
                    get_numTxAttempts(line),
                    get_queuePos(line),
                    0,
                    0,
                    ""]
            i+=1
            
    df.to_csv('data_csv/pkt_tx.csv',index=False)

    
    
def create_df_rx(data_file_tx, data_file_ack_rx):
    i=0
    df = pd.DataFrame(columns=('time', 'addr', 'comp','asn', 'statType', 'trackinstance', 'trackowner',
                                 'length', 'frameType', 'slotOffset', 'frequency', 'l2Src', 'rssi', 
                                  'lqi', 'crc', 'queuePos', 'ACK_RX'))
    with open(data_file_tx, "r") as f_rx:
        for line in f_rx:
            df.loc[i]=[get_time(line), 
                    get_addr(line), 
                    get_comp(line), 
                    get_asn(line), 
                    get_statType(line), 
                    get_trackinstance(line), 
                    get_trackowner(line), 
                    get_length(line), 
                    get_frameType(line), 
                    get_slotOffset(line), 
                    get_frequency(line), 
                    get_l2Src(line), 
                    get_rssi(line), 
                    get_lqi(line),
                    get_crc(line),
                    get_queuePos(line),
                    0]
            i+=1
    
    with open(data_file_ack_rx, "r") as f_rx:
        for line in f_rx:
            #pour chaque ligne on met la variable ack de la rx associée a 1
            #si il existe une rx associée a l'ack
            df.loc[(df['asn']==get_asn(line)) & (df['l2Src'].str.endswith(get_addr(line))), "ACK_RX" ] = 1
            
    
    df.to_csv('data_csv/pkt_rx.csv',index=False)
    
    
def fill_succes_tx(df_tx, df_rx):
    i=0
    j=0
    asn_tx = 0
    src_tx = ""
    dest_tx = ""
    list_addr_rx = []
    list_index = []

    # pour tous les tx
    for i in range(len(df_tx)):
        #on regarde si la tx est recu | cad si des rx ont eu lieu au meme asn
        asn_tx = df_tx.iloc[i]["asn"]
        src_tx = df_tx.iloc[i]["addr"]
        dest_tx = df_tx.iloc[i]["l2Dest"]

        list_addr_rx = df_rx.loc[ (df_rx['asn']==asn_tx) & (df_rx['l2Src'].str.endswith(src_tx)) ]["addr"].values.tolist()
        df_tx.set_value(i,"list_rx",list_addr_rx)
        if len(list_addr_rx)>0:
            df_tx.set_value(i,"succes_rx",1)

            list_index = df_rx.loc[ (df_rx['asn']==asn_tx) & (df_rx['l2Src'].str.endswith(src_tx)) ].index.tolist()
            j=0
            for j in list_index:
                if df_rx.iloc[j]["ACK_RX"] == '1':
                    df_tx.set_value(i,"succes_ack",1)
            
    df_tx.to_csv('data_csv/pkt_tx.csv',index=False)

    