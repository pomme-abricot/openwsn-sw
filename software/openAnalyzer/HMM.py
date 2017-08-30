# -*-coding:Latin-1 -*

import re
import pandas as pd
from func_def_class import *
from func_parsing_logfile import *

import random
from random import shuffle
import numpy as np

from sklearn.model_selection import train_test_split
from ghmm import *
import ghmm

#Creer les sets de données 
# chaque reservation entre 2 noeuds est transformé en une séquence de 2 à ~8 characteres
def HMM_create_data_set(df):
    df_res = df.copy()
    df_res.sort_values(['src_res', 'dest_res', 'asn', 'command', 'status'], ascending=[True, False, True, False, False], inplace=True)
    #un set de reservation
    train_set = []
    #ensemble des sets
    train_sets=[]
    #concaténation de tous les set
    train_set_conc=[]
    set_tmp=[]
    p=0
    del train_sets[:]
    df_tmp = pd.DataFrame
    l_dest = []
    alph = IntegerRange(1,9)

    for src in df_res["src_res"].unique():
        del train_set[:]
        df_tmp = df_res.loc[df_res["src_res"]==src]
        l_dest = df_tmp["dest_res"].unique().tolist()

        for dest in l_dest:
            train_set = df_res.loc[ (df_res["src_res"]==src) & (df_res["dest_res"]==dest) ]["state"].tolist()
            train_set_emmission = EmissionSequence(alph, train_set)
            set_tmp=train_set[:]
            train_sets.append(set_tmp)
   
    return train_sets

def HMM_parsing_data(file_data_good, file_data_bad, alph):
    #BONNE CONNECTION
    df_res_g = pd.read_csv(file_data_good, dtype=str)
    df_res_g["asn"] = df_res_g["asn"].astype(int)
    #df_res["id_res"] = df_res["id_res"].astype(int)
    #df_res["succes"] = df_res["succes"].astype(int)
    df_res_g["state"] = df_res_g["state"].astype(int)
    df_res_g = df_res_g.fillna('')
    #df_res.sort_values(['asn', 'command', 'status'], ascending=[True, False, False], inplace=True)
    df_res_g = df_res_g.reset_index(drop=True)
    
    #MAUVAISE CONNECTION
    df_res_b = pd.read_csv(file_data_bad, dtype=str)
    df_res_b["asn"] = df_res_b["asn"].astype(int)
    #df_res["id_res"] = df_res["id_res"].astype(int)
    #df_res["succes"] = df_res["succes"].astype(int)
    df_res_b["state"] = df_res_b["state"].astype(int)
    df_res_b = df_res_b.fillna('')
    #df_res.sort_values(['asn', 'command', 'status'], ascending=[True, False, False], inplace=True)
    df_res_b = df_res_b.reset_index(drop=True)
    
    train_sets_s = HMM_create_data_set(df_res_g)
    train_sets_f = HMM_create_data_set(df_res_b)
    
    #create train set and test set
    X_s = np.asarray(train_sets_s)
    y_s = y=np.array([1]*len(train_sets_s))
    X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_s, y_s, test_size=0.33, random_state=42, shuffle=False)
    X_train_s, X_test_s, y_train_s, y_test_s=X_train_s.tolist(), X_test_s.tolist(), y_train_s.tolist(), y_test_s.tolist()
    X_f = np.asarray(train_sets_f)
    y_f = y=np.array([0]*len(train_sets_f))
    X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_f, y_f, test_size=0.33, random_state=42, shuffle=False)
    X_train_f, X_test_f, y_train_f, y_test_f=X_train_f.tolist(), X_test_f.tolist(), y_train_f.tolist(), y_test_f.tolist()

    #transforme la liste en sequence d'emission
    seq_train_s = SequenceSet(alph, X_train_s)
    seq_train_f = SequenceSet(alph, X_train_f)

    seq_test_s = SequenceSet(alph, X_test_s)
    seq_test_f = SequenceSet(alph, X_test_f)
    
    return seq_train_s, seq_train_f, seq_test_s, seq_test_f

#test_sets[0] -> X_test, [1] -> y_test
# on teste chaque seq sur les 2 modeles et on prend celui avec le plus petit likelihood
def HMM_calcul_score(seq_test_s, seq_test_f, m_succes, m_fail):
    vp=0.0
    vn=0.0
    fp=0.0
    fn=0.0
    for el in seq_test_s:
        v_s = m_succes.viterbi(el)
        v_f = m_fail.viterbi(el)
        if v_s[1] < v_f[1]:
            vp+=1
        else:
            fp+=1
        
    for el in seq_test_f:
        v_s = m_succes.viterbi(el)
        v_f = m_fail.viterbi(el)
        if v_s[1] > v_f[1]:
            vn+=1
        else:
            fn+=1
    if (fp+vp)!= 0:
        precision = vp/(fp+vp)
    else:
        precision = 0
    if (fn+vp)!= 0:
        recall = vp/(fn+vp)
    else:
        recall = 0
    if (precision+recall) != 0:
        fmeasure = 2*(precision*recall)/(precision+recall)
    else:
        fmeasure = 0
    
    return precision, recall, fmeasure, vp, vn, fp, fn


def HMM_find_best(seq_train_s, seq_train_f, seq_test_s, seq_test_f, sigma, nb_states=5, nb_loops=10):

    #indicator
    precision_tmp, recall_tmp, fmeasure_tmp = 0,0,0
    m_best_ini = ghmm.DiscreteEmissionHMM
    l_fmeasure = []
    l_precision = []
    l_recall = []

    A = []
    B = []
    l_tmp = []

    for n in range(2,nb_states+1):
        del l_fmeasure[:]
        del l_precision[:]
        del l_recall[:]

        for loop in range(nb_loops):
            #A matrice proba transition etats | ici on a n etats
            #on ne teste que pour un A avce des valeurs aléatoire
            del A[:]
            for i in range(n):
                l_tmp = [random.randint(1,100) for i in xrange(n)]
                l_tmp[:]= [float(x)/sum(l_tmp) for x in l_tmp]
                A.append( l_tmp )

            #matrice de proba des evenements
            del B[:]
            for i in range(n):
                l_tmp = [random.randint(1,100) for i in xrange(len(sigma))]
                l_tmp[:]= [float(x)/sum(l_tmp) for x in l_tmp]
                B.append( l_tmp )

            #proba de l'etat initial
            pi = [random.randint(1,100) for i in xrange(n)]
            pi[:]= [float(x)/sum(pi) for x in pi]


            m_ini = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
            m_succes = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
            m_fail = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)

            m_succes.baumWelch(seq_train_s)
            m_fail.baumWelch(seq_train_f)

            precision, recall, fmeasure, vp, vn, fp, fn = HMM_calcul_score(seq_test_s, seq_test_f, m_succes, m_fail)
            l_fmeasure.append(fmeasure)
            l_recall.append(recall)
            l_precision.append(precision)
            if fmeasure > fmeasure_tmp:
                m_best_ini = m_ini
                fmeasure_tmp = fmeasure
                recall_tmp = recall
                precision_tmp = precision
        
        plt.figure()
        plt.title("nb_state : %d" % n)
        plt.plot()
        
    return m_best_ini, fmeasure_tmp, recall_tmp, precision_tmp


def HMM_get_indicators(seq_train_s, seq_train_f, seq_test_s, seq_test_f, sigma, nb_states=5, nb_loops=10):

    #indicator
    precision_tmp, recall_tmp, fmeasure_tmp = 0,0,0
    m_best_ini = ghmm.DiscreteEmissionHMM
    l_fmeasure = []
    del l_fmeasure[:]
    l_precision = []
    del l_precision[:]
    l_recall = []
    del l_recall[:]

    A = []
    B = []
    l_tmp = []
    n=nb_states

    for loop in range(nb_loops):
        #A matrice proba transition etats | ici on a n etats
        #on ne teste que pour un A avce des valeurs aléatoire
        del A[:]
        for i in range(n):
            l_tmp = [random.randint(1,100) for i in xrange(n)]
            l_tmp[:]= [float(x)/sum(l_tmp) for x in l_tmp]
            A.append( l_tmp )

        #matrice de proba des evenements
        del B[:]
        for i in range(n):
            l_tmp = [random.randint(1,100) for i in xrange(len(sigma))]
            l_tmp[:]= [float(x)/sum(l_tmp) for x in l_tmp]
            B.append( l_tmp )

        #proba de l'etat initial
        pi = [random.randint(1,100) for i in xrange(n)]
        pi[:]= [float(x)/sum(pi) for x in pi]


        m_ini = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
        m_succes = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
        m_fail = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)

        m_succes.baumWelch(seq_train_s)
        m_fail.baumWelch(seq_train_f)

        precision, recall, fmeasure, vp, vn, fp, fn = HMM_calcul_score(seq_test_s, seq_test_f, m_succes, m_fail)
        l_fmeasure.append(fmeasure)
        l_recall.append(recall)
        l_precision.append(precision)
        if fmeasure > fmeasure_tmp:
            m_best_ini = m_ini
            fmeasure_tmp = fmeasure
            recall_tmp = recall
            precision_tmp = precision
    return m_best_ini, fmeasure_tmp, recall_tmp, precision_tmp, l_fmeasure, l_recall, l_precision