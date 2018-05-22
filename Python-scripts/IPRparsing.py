import re
import numpy as np
import pandas as pd
import requests
import ete3
ncbi = ete3.NCBITaxa()

## FUNCTIONS ##

def MakeP2IPR(species):
    print('start making IPR dict')
    IPR_entry=[]
    P2IPR_full={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_' + species+ '_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_full[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append((l[1],l[2]))

    for key in P2IPR_full.keys():
        P2IPR_full[key]=list(pd.unique(P2IPR_full[key]))

    IPR_entry=[]
    P2IPR_ID={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_' + species+ '_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_ID[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append(l[1])
    for key in P2IPR_ID.keys():
        P2IPR_ID[key]=list(pd.unique(P2IPR_ID[key]))

    IPR_entry=[]
    P2IPR_name={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_' + species+ '_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_name[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append(l[2])

    for key in P2IPR_name.keys():
        P2IPR_name[key]=list(pd.unique(P2IPR_name[key]))
    print('finished IPR dict')
    return (P2IPR_full,P2IPR_ID,P2IPR_name)

def Find_IPR_terms(species,ID_list):
    P2IPR=MakeP2IPR(species)[1]
    IPR_terms=[]
    for ID in ID_list:
        if ID in P2IPR.keys():
            IPR_terms.append(P2IPR[ID])
        else:
            IPR_terms.append(None)
    return IPR_terms
def Find_proteins(species,IPR):
    P2IPR=MakeP2IPR(species)[1]
    outp = []
    for key in P2IPR:
        if IPR in P2IPR[key]:
            outp.append(key)

    return outp


def MakeP2IPR_hum():
    print('start making IPR hum dict')
    IPR_entry=[]
    P2IPR_full_hum={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_human_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_full_hum[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append((l[1],l[2]))

    for key in P2IPR_full_hum.keys():
        P2IPR_full_hum[key]=list(pd.unique(P2IPR_full_hum[key]))

    IPR_entry=[]
    P2IPR_ID_hum={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_human_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_ID_hum[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append(l[1])
    for key in P2IPR_ID_hum.keys():
        P2IPR_ID_hum[key]=list(pd.unique(P2IPR_ID_hum[key]))

    IPR_entry=[]
    P2IPR_name_hum={}
    with open ('/Users/thesis/Desktop/Google Drive/thesis-lorenz/Data-handling/Datasets/ipr_human_out.txt','r') as f:
        for line in f:
            l = line.split('\t')
            if l[0] not in IPR_entry:
                if IPR_entry != []:
                    P2IPR_name_hum[IPR_entry[0]]=IPR_entry[1:]
                    IPR_entry =[]
                IPR_entry.append(l[0])
            IPR_entry.append(l[2])

    for key in P2IPR_name_hum.keys():
        P2IPR_name_hum[key]=list(pd.unique(P2IPR_name_hum[key]))
    print('finished IPR hum dict')
    return (P2IPR_full_hum,P2IPR_ID_hum,P2IPR_name_hum)

def Find_IPR_terms_hum(ID_list):
    P2IPR_hum=Make_P2IPR_hum()[1]
    IPR_terms=[]
    for ID in ID_list:
        if ID in P2IPR_hum.keys():
            IPR_terms.append(P2IPR_hum[ID])
        else:
            IPR_terms.append(None)
    return IPR_terms

def Find_proteins_hum(IPR):
    outp = []
    P2IPR_hum = MakeP2IPR_hum()[1]
    for key in P2IPR_hum:
        if IPR in P2IPR_hum[key]:
            outp.append(key)
    return outp

if __name__ == "__main__":
    species=input('Enter species ')
    Int_DB = pd.read_table("/Users/thesis/Desktop/Test run/"+species,
    usecols=lambda x:x !="Unnamed: 0")
    Int_DB['ipr_a']=Int_DB.protein_a.apply(lambda x: Find_IPR_terms(species,x))
    Int_DB['ipr_b']=Int_DB.protein_b.apply(lambda x: Find_IPR_terms_hum(x))

    Int_DB.to_csv("/Users/thesis/Desktop/Test run/" + species +"_IPR", sep ="\t")
    print('A new file has been created at /Users/thesis/Desktop/Test run/'+ species +'_IPR')
