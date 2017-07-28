# -*-coding:Latin-1 -*

import re
import pandas as pd
from func_def_class import *
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

#touve la nieme occurence d'une substring dans str
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# LA SRC ET DEST SONT ./. A LA RES ET NON AU MSG
def create_df_res(data_file_tx):
    df = pd.DataFrame(columns=('time', 'asn', 'src', 'dest', 'command', 'status', 'ch1', 
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
            elif  ( ( get_command(line)=="CELLADD_REP" ) and ( (get_status(line)=="ENQUEUED" ) or (get_status(line)=="TXED") ) ) or ( ( get_command(line)=="CELLADD_REQ" ) and  (get_status(line)=="RCVD" )  ):
                dest = get_addr(line)[-4:]
                src = get_neigh(line)[-4:]
                
            df.loc[i]=[get_time(line), 
                    get_asn(line), 
                    src,
                    dest,
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