# -*-coding:Latin-1 -*

import re
import pandas as pd
from func_parsing_logfile import * 
import ast


#créer le dataframe des paquets transmis
#def create_df_tx(data_file_tx):

#créer le dataframe des paquets recus
#def create_df_rx(data_file_tx, data_file_ack_rx):

#rempli les colonnes des réussites de transmission dans le df de paquet transmis 
#def fill_succes_tx(df_tx, df_rx):

#créer le df des liaisons fils/pere pour chaque réactualisation
#def create_df_parent(data_file):

#créer le df qui pour chaque parent donne la liste des fils
#def create_df_sons(df_parent):

#fonction qui donne le pere pour un noeud et un asn donné
#def get_parent(node_data, asn_data):

#rempli le df des réservation | nombre de frères du noeud source de la réservation
#def fill_nb_siblings(df_res, df_fils, df_parent):
    
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

    
    
#creer la df avec les infos sur les changements de parents
def create_df_parent(data_file):

    list_parent=[]
    del list_parent[:]
    
    with open(data_file) as origin_file:
        for line in origin_file:
            if "control cell with the parent" in line:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                addr = line[line.find("from ")+len("from "):line.find(":", line.find("from"))]
                parent = line[line.find("parent ")+len("parent "):line.find(")", line.find("parent "))]
                list_parent.append([asn, addr, parent,'', "res triggered"])
            if "parent update" in line:
                asn = line[line.find("asn")+len("asn="):line.find(")", line.find("asn"))]
                addr = line[line.find("from ")+len("from "):line.find(":", line.find("from"))]
                parent = line[line.find("by ")+len("by "):line.find("\n", line.find("from"))]
                old = line[line.find("nexthops ")+len("nexthops "):line.find(" by", line.find("nexthops"))]
                list_parent.append([asn, addr, parent, old, "parent update"])
            if "oldParent" in line:
                pass
                
    
    i=0
    df_parent = pd.DataFrame(columns=('asn', 'addr', 'parent', 'old_parent', "info"))
    for elem in list_parent:
        df_parent.loc[i]=[elem[0], 
                   elem[1],
                   elem[2],
                   elem[3],
                   elem[4]
                  ]
                   
        i+=1
    df_parent.to_csv('data_csv/parent.csv',index=False)
    

def create_df_sons(df_parent):
    df_fils = pd.DataFrame(columns=('asn', 'parent', 'fils'))

    list_parent=df_parent.parent.unique().tolist()
    list_fils = []
    for el in range (len(list_parent)):
        list_fils.append([])

    p=0
    for i in range(len(df_parent)):
        asn = df_parent.loc[i]["asn"]
        addr= df_parent.loc[i]["addr"]
        parent= df_parent.loc[i]["parent"]
        info = df_parent.loc[i]["info"]
        old = df_parent.loc[i]["old_parent"]
        if info == "res triggered":
            #on verifie si le noeud est dans la liste
            if not addr in list_fils[ list_parent.index(parent) ] :
                list_fils[ list_parent.index(parent) ].append(addr)

            list_tmp = list(list_fils[ list_parent.index(parent) ])
            df_fils.loc[p]=[asn, 
                        parent,
                        list_tmp
                        ]
            p+=1

        if info == "parent update":
            # on l'ajoute a son nouveau pere
            if not addr in list_fils[ list_parent.index(parent) ] :
                list_fils[ list_parent.index(parent) ].append(addr)
            #on supprime le noeud de la liste précedente
            if  addr in list_fils[ list_parent.index(old) ] :
                list_fils[ list_parent.index(old) ].remove(addr)

            list_tmp = list(list_fils[ list_parent.index(parent) ])
            df_fils.loc[p]=[asn, 
                        parent,
                        list_tmp
                        ] 
            p+=1
            list_tmp = list(list_fils[ list_parent.index(old) ])
            df_fils.loc[p]=[asn, 
                        old,
                        list_tmp
                        ]
            p+=1
    
    df_fils.to_csv('data_csv/sons.csv',index=False)

            
            
def get_nb_siblings(node_son, df_fils,asn_data, df_parent):
    asn_data = int(asn_data)
    if get_parent(node_son, asn_data, df_parent) == "no parent":
        return "error : no parent"
    else:
        return len(ast.literal_eval(df_fils.loc[ (df_fils["asn"] <= asn_data) & (df_fils["parent"] ==get_parent(node_son, asn_data, df_parent))].iloc[-1]["fils"])) -1
    
            
#fonction qui donne le pere d'un noeud pour un asn donné
def get_parent(node_data, asn_data, df_parent):
    asn_data = int(asn_data)
    if not df_parent.loc[ (df_parent["asn"] <= asn_data) & (df_parent["addr"] ==node_data)].empty:
        return df_parent.loc[ (df_parent["asn"] <= asn_data) & (df_parent["addr"] ==node_data)].iloc[-1]["parent"]
    else:
        return "no parent"
    
def fill_nb_siblings(df_res, df_fils, df_parent):
    for i in range(len(df_res)):
        if get_nb_siblings(df_res.iloc[i]["src"],df_fils,df_res.iloc[i]["asn creation"], df_parent) == "error : no parent":
            #pass
            #on met la valeur de siblings a 0 quand le noeud n'a pas de parent (A modifier avec une valeur plus cohérente) 
            df_res.set_value(i,"nb_sibl", 0 )
        else:
            df_res.set_value(i,"nb_sibl",get_nb_siblings(df_res.iloc[i]["src"], df_fils, df_res.iloc[i]["asn creation"] , df_parent) )
            
    df_res.to_csv('data_csv/res.csv',index=False)