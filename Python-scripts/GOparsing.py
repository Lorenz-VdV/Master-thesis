import re
import numpy as np
import pandas as pd
import xlwt
import requests
import ete3
ncbi = ete3.NCBITaxa()



def MakeP2GO(species):
    print('start making GO dict')
    with open ('../../Data-handling/Datasets/GO_' + species + '_out.txt') as f:
        GO_entry =[]
        P2GO = {}
        for line in f:
            l = line.split('\t')
            if l[0] != 'UniProtKB':
                continue
            else:
                if l[1] not in GO_entry:
                    if GO_entry != []:
                        P2GO[GO_entry[0]]=GO_entry[1:]
                        GO_entry =[]
                    GO_entry.append(l[1])
                GO_entry.append(l[4])

    for key in P2GO.keys():
        P2GO[key]=list(pd.unique(P2GO[key]))
    print('finished making GO dict')
    return P2GO

def Find_GO_terms(species,ID_list):
    P2GO = MakeP2GO(species)
    GO_terms=[]
    for ID in ID_list:
        if ID in P2GO.keys():
            GO_terms.append(P2GO[ID])
        else:
            GO_terms.append(None)
    return GO_terms

def Find_proteins(species,GO):
    outp = []
    for key in MakeP2GO(species):
        if GO in MakeP2GO(species)[key]:
            outp.append(key)
    return outp

def MakeP2GO_hum():
    print('start making GO hum dict')
    with open ('../../Data-handling/Datasets/GO_human_out.txt') as f:
        GO_entry =[]
        P2GO_hum = {}
        for line in f:
            l = line.split('\t')
            if l[0] != 'UniProtKB':
                continue
            else:
                if l[1] not in GO_entry:
                    if GO_entry != []:
                        P2GO_hum[GO_entry[0]]=GO_entry[1:]
                        GO_entry =[]
                    GO_entry.append(l[1])
                GO_entry.append(l[4])

    for key in P2GO_hum.keys():
        P2GO_hum[key]=list(pd.unique(P2GO_hum[key]))
    print('finished making GO hum dict')
    return P2GO_hum

def Find_GO_terms_hum(ID_list):
    P2GO_hum = MakeP2GO_hum()
    GO_terms=[]
    for ID in ID_list:
        if ID in P2GO_hum.keys():
            GO_terms.append(P2GO_hum[ID])
        else:
            GO_terms.append(None)
    return GO_terms
def Find_proteins_hum(GO):
    outp = []
    for key in MakeP2GO_hum():
        if GO in MakeP2GO_hum()[key]:
            outp.append(key)
    return outp
if __name__ == "__main__":
    species = input ('Enter species ')
    Int_DB = pd.read_table('/Users/thesis/Desktop/Test run/' +species + '_IPR',
                            usecols=lambda x:x !="Unnamed: 0")
    Int_DB['go_a']=Int_DB.protein_a.apply(lambda x: Find_GO_terms(species,x))
    Int_DB['go_b']=Int_DB.protein_b.apply(lambda x: Find_GO_terms_hum(x))

    Int_DB.to_csv('/Users/thesis/Desktop/Test run/' + species + '_IPR_GO', sep ="\t")
    print('A new file has been created at /Users/thesis/Desktop/Test run/' + species + '_IPR_GO')
