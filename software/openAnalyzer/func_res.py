# -*-coding:Latin-1 -*

import re
import pandas as pd
from func_def_class import *
from func_parsing_logfile import *
import ast

#touve la nieme occurence d'une substring dans str
#def find_nth(haystack, needle, n):
    
# crée un df avec les reservations
#def create_df_res(data_file):

#fonction get simult df | entrée un df de réservation tmp et df des paquets transmis, en sortie une liste du nombre de paquets simultanés transmis pour chaque réservation de df tmp et leur asn
#def get_simult_df(df_tmp, df_tx):

#remplis le df de réservation | ajoute les données sur les transmissions de paquets et leurs collisions.
#def fill_simult(df_res, df_tx):

#Creer un df avec les données des réservations 
# fonction pour remplir un csv avec toutes les données res
#def create_df_step_res(data_file):

#Fill columns succes and id_res of res data frame
#def fill_succes_id(df_res):

#set state used for HMM learning
#def set_states(df_res):

#Add the column numAtt to df_res + add all paquet to the dataframe
#def add_paquet(df):

#touve la nieme occurence d'une substring dans str
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# LA SRC ET DEST SONT ./. A LA RES ET NON AU MSG
def create_df_res(data_file_tx):
    df = pd.DataFrame(columns=('time', 'asn', 'src_res', 'dest_res', 'src_pkt', 'dest_pkt', 'command', 'status', 'ch1', 
                               'slot1', 'ch2', 'slot2', 'ch3', 'slot3'))

    i=0
    with open(data_file_tx, "r") as f_tx:
        for line in f_tx:
            if len( line[line.find("choffset")+len("choffset[X]="):line.find("|", line.find("choffset"))] ) < 10 :
                ch1 = line[line.find("choffset")+len("choffset[X]="):line.find("|", line.find("choffset"))]
            else:
                ch1 = ""
            if len(line[find_nth(line, "choffset",2)+len("choffset[X]="):line.find("|", find_nth(line,"choffset",2) )]) <10:
                ch2 = line[find_nth(line, "choffset",2)+len("choffset[X]="):line.find("|", find_nth(line,"choffset",2) )]
            else:
                ch2=""
            if len(line[find_nth(line,"choffset",3)+len("choffset[X]="):line.find("|", find_nth(line,"choffset",3) )]) <10:
                ch3 = line[find_nth(line,"choffset",3)+len("choffset[X]="):line.find("|", find_nth(line,"choffset",3) )]
            else:
                ch3=""
                
            if len(line[line.find("slotoffset")+len("slotoffset[X]="):line.find("|", line.find("slotoffset"))]) <10:
                slot1 = line[line.find("slotoffset")+len("slotoffset[X]="):line.find("|", line.find("slotoffset"))]
            else:
                slot1=""
            if len(line[find_nth(line,"slotoffset",2) +len("slotoffset[X]=") : line.find("|", find_nth(line,"slotoffset",2) )])<10:
                slot2 = line[find_nth(line,"slotoffset",2) +len("slotoffset[X]=") : line.find("|", find_nth(line,"slotoffset",2) )]
            else:
                slot2=""
            if len(line[find_nth(line,"slotoffset",3) + len("slotoffset[X]="): line.find("|", find_nth(line,"slotoffset",3) )])<10:
                slot3 = line[find_nth(line,"slotoffset",3) + len("slotoffset[X]="): line.find("|", find_nth(line,"slotoffset",3) )]
            else:
                slot3=""
            
            if ( ( get_command(line)=="CELLADD_REQ" ) and ( (get_status(line)=="ENQUEUED" ) or (get_status(line)=="TXED") ) ) or ( ( get_command(line)=="CELLADD_REP" ) and  (get_status(line)=="RCVD" )  ):
                src = get_addr(line)[-4:]
                dest = get_neigh(line)[-4:]
                src_pkt=get_addr(line)[-4:]
                dest_pkt=get_neigh(line)[-4:]
            elif  ( ( get_command(line)=="CELLADD_REP" ) and ( (get_status(line)=="ENQUEUED" ) or (get_status(line)=="TXED") ) ) or ( ( get_command(line)=="CELLADD_REQ" ) and  (get_status(line)=="RCVD" )  ):
                dest = get_addr(line)[-4:]
                src = get_neigh(line)[-4:]
                src_pkt=get_addr(line)[-4:]
                dest_pkt=get_neigh(line)[-4:]
                
            df.loc[i]=[get_time(line), 
                    get_asn(line), 
                    str(src),
                    str(dest),
                    str(src_pkt),
                    str(dest_pkt),
                    #get_addr(line),
                    #get_neigh(line),
                    get_command(line), 
                    get_status(line), 
                    ch1,
                    slot1,
                    ch2,
                    slot2,
                    ch3,
                    slot3 ]
            i+=1
    
    return df
    #df.to_csv('data_csv/pkt_tx.csv',index=False)
    
def fill_succes_id(df_res):
    df = df_res.copy()
    df["id_res"]=0
    df["succes"]=0

    #marque les debut de chaque réservation par un id
    p = 0

    for i in range(len(df)):
        if (df.loc[i]["command"] == 'CELLADD_REQ') and (df.loc[i]["status"] == 'ENQUEUED'):
            p+=1
            df.set_value(i,"id_res",p)

    #set the id of each res

    for i in range (1,max(df["id_res"].unique())):
        src=df['src_res'][df.loc[df["id_res"]==i].index[0]]
        dest=df['dest_res'][df.loc[df["id_res"]==i].index[0]]
        asn=df['asn'][df.loc[df["id_res"]==i].index[0]]
        index_l=df.loc[ (df["src_res"]==src) & (df["dest_res"]==dest ) & (df["asn"]>asn)].index

        for j in index_l:
            if df.loc[j]["id_res"]<i:
                df.set_value(j,"id_res",i)

    #fill the label succes if a line with command=cell_rep and status=RCVD/TXED
    for i in range (1,max(df["id_res"].unique())):
        if (not df.loc[ (df["id_res"]==i) & (df["command"]=="CELLADD_REP" ) & (df["status"]=="RCVD")].empty) or (not df.loc[ (df["id_res"]==i) & (df["command"]=="CELLADD_REP" ) & (df["status"]=="TXED")].empty):
            for j in df.loc[ (df["id_res"]==i)].index:
                df.set_value(j,'succes',1)

    #for all res if failed (succes=0) and not failed msg -> get the failed from next res 
    for i in df.loc[ (df["succes"]==0) ]["id_res"].unique():
        #print i
        if df.loc[ (df["id_res"]==i) & (df["status"]=="FAILED") ].empty:
            #il n'y a pas de failed mais la res a échoué
            asn=df['asn'][df.loc[df["id_res"]==i].index[0]]
            src=df['src_res'][df.loc[df["id_res"]==i].index[0]]
            dest=df['dest_res'][df.loc[df["id_res"]==i].index[0]]
            if not df.loc[ (df["src_res"]==src) & (df["dest_res"]==dest ) & (df["status"]=='FAILED' )& (df["asn"]>asn )].head(1).empty:
                df.set_value(df.loc[ (df["src_res"]==src) & (df["dest_res"]==dest ) & (df["status"]=='FAILED' )& (df["asn"]>asn )].head(1).index[0], "succes", 0)
                df.set_value(df.loc[ (df["src_res"]==src) & (df["dest_res"]==dest ) & (df["status"]=='FAILED' )& (df["asn"]>asn )].head(1).index[0], "id_res", i)
            else:
                print "error:Reservation",i,"failed without failed message"

    return df


def set_state(df_res):
    df=df_res.copy()
    df["state"]=0
    # set a state value : req enqueued=1 / req tx/rx=2 / rep enqueued=3 /rep tx/rx=4 / failed=5
    for i in range(len(df)):
        if (df.loc[i]["command"]=='CELLADD_REQ') and (df.loc[i]["status"]=='ENQUEUED'):
            df.set_value(i,"state",1)
        if (df.loc[i]["command"]=='CELLADD_REQ') and (df.loc[i]["status"]=='TXED'):
            df.set_value(i,"state",2)
        if (df.loc[i]["command"]=='CELLADD_REQ') and (df.loc[i]["status"]=='RCVD'):
            df.set_value(i,"state",3)
        if (df.loc[i]["command"]=='CELLADD_REP') and (df.loc[i]["status"]=='ENQUEUED'):
            df.set_value(i,"state",4)
        if (df.loc[i]["command"]=='CELLADD_REP') and (df.loc[i]["status"]=='TXED'):
            df.set_value(i,"state",5)
        if (df.loc[i]["command"]=='CELLADD_REP') and (df.loc[i]["status"]=='RCVD'):
            df.set_value(i,"state",6)
        if (df.loc[i]["command"]=='CELLADD_REQ') and (df.loc[i]["status"]=='FAILED'):
            df.set_value(i,"state",7)
        if (df.loc[i]["command"]=='CELLADD_REP') and (df.loc[i]["status"]=='FAILED'):
            df.set_value(i,"state",8)

    return df


#Add the column numAtt to df_res + add all paquet to the dataframe
def add_paquet(df, df_tx):
    df_res = df.copy()
    df_res["numAtt"]=0

    for i in df_res.loc[df_res["status"]=="TXED"].index:
        asn = df_res.loc[i]["asn"]
        src = df_res.loc[i]["src_pkt"]
        dest = df_res.loc[i]["dest_pkt"]
        if not df_tx.loc[ (df_tx['asn']==asn) & (df_tx['addr']==src) & (df_tx['l2Dest'].str.endswith(dest))].empty: 
            numAtt = df_tx.loc[ (df_tx['asn']==asn) & (df_tx['addr']==src) & (df_tx['l2Dest'].str.endswith(dest))]["numTxAttempts"]
            df_res.set_value(i,"numAtt", int(numAtt))
            if int(numAtt)>1:
                df_tmp = df_tx.loc[ (df_tx['asn']<asn) & (df_tx['addr']==src) & (df_tx['l2Dest'].str.endswith(dest))].tail(int(numAtt) -1 )
                df_tmp = df_tmp.reset_index(drop=True)
                for j in range(int(numAtt)-1):
                    data = {'time' : df_tmp.loc[j]["time"] , 
                            'asn' : df_tmp.loc[j]["asn"], 
                            'src_res' : df_res.loc[i]["src_res"], 
                            'dest_res' : df_res.loc[i]["dest_res"], 
                            'src_pkt' : src, 'dest_pkt' : dest, 
                            'command' : df_res.loc[i]["command"], 
                            'status' : df_res.loc[i]["status"], 
                            "numAtt" : df_tmp.loc[j]["numTxAttempts"] }
                    df_res=df_res.append(data , ignore_index=True)
    return df_res
        

