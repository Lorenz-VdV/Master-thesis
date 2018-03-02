  #setup modules
import re
import numpy as np
import pandas as pd
import xlwt
import os
import ete3
ncbi = ete3.NCBITaxa()
import requests
import time
import argparse
from IPRparsing import Find_IPR_terms,Find_IPR_terms_hum
from GOparsing import Find_GO_terms,Find_GO_terms_hum
#ncbi.update_taxonomy_database()

#setup REST
BASE = 'http://www.uniprot.org'
KB_ENDPOINT = '/uniprot/'
TOOL_ENDPOINT = '/uploadlists/'

#setup argparse
parser = argparse.ArgumentParser(description = 'interaction data extraction initialisation')

parser.add_argument('-o', '--origin', default = 'Users/thesis/Desktop', help = 'Enter path of raw interaction datasets')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop', help = 'Enter path for target files')
parser.add_argument('-s', '--species', default ='None', help = 'Enter subject species')
results = parser.parse_args()

#Read in raw interaction data
species = results.species

HPIDB = pd.read_table(results.origin + species +'.txt',
                        names=["protein_a","protein_b","alias_a","alias_b","d_method","pubmedid","taxid_a","taxid_b","int_type","source_db","conf_score"],
                        usecols=[0,1,4,5,6,8,9,10,11,12,14],
                        header=0)

IntAct = pd.read_table(results.origin + species,
                        names=["protein_a","protein_b","alias_a","alias_b","d_method","pubmedid","taxid_a","taxid_b","int_type","source_db","conf_score"],
                        usecols=[0,1,4,5,6,8,9,10,11,12,14],
                        header=0)

PHISTO = pd.read_excel(results.origin + species +'.xls',
                        names= ["taxid_a", "protein_a", "protein_b", "d_method","pubmedid"],
                        usecols=[1,2,4,6,7])

print ('the length of HPIDB, IntAct and PHISTO is ' + str(len(HPIDB)), str(len(IntAct)) + ' and ' + str(len(PHISTO)) +' respectively')

#Clean up taxid column of IntAct
r = IntAct.taxid_a
r = r.str.lower()
r = r.str.extract(r'(?:taxid:)([0-9]*)',expand = False)
IntAct.taxid_a = r

r = IntAct.taxid_b
r = r.str.lower()
r = r.str.extract(r'(?:taxid:)([0-9]*)',expand = False)
IntAct.taxid_b = r

#Merge IntAct and HPIDB
df=pd.concat([HPIDB,IntAct])
df=df.reset_index(drop=True)
print('the length of the merged IntAct/HPIDB dataframe is ' + str(len(df)))

#Make list of all taxids in df
#select all taxids which have the taxid of the subject species in their lineage
#filter out all entries which don't have a taxid in the previously made selection
taxids= list(pd.unique(list(df.taxid_a.unique())+list(pd.unique(list(df.taxid_b.unique())))))
parent= ncbi.get_name_translator([species])
taxid_list=[]
for taxid in taxids:
    lineage = ncbi.get_lineage(taxid)

    if parent.get(species)[0] in lineage:
        taxid_list.append(taxid)
taxid_list.append('9606')

print('The selection of taxids is ' + str(ncbi.get_taxid_translator(taxid_list)))
sel1 = df.taxid_a.apply(lambda x: str(x) in taxid_list)
sel2 = df.taxid_b.apply(lambda x: str(x) in taxid_list)
df = df.loc[sel1 & sel2,:]
print('the length of df after taxid filtering is ' + str(len(df)))

#Clean up all the columns, keeping only interpretable information(i.e. get rid of all the IMEx encoding and such)
for name in ["d_method","int_type","source_db"]:
    r = df[name]
    r = r.str.extract((r'(?:psi-mi:"?MI:[0-9]*"?[(])([^)]*)(?:[)])') ,expand = False)
    df[name] = r


for name in ["protein_a","protein_b"]:
    r = df[name]
    r = r.str.extract(r'(?:uniprotkb:)([a-zA-Z0-9]*)', expand=False)
    df[name] = r


r = df.pubmedid
r = r.str.extract(r'(?:[^p]*)(?:pubmed:)([0-9]*)(?:.*)',expand=False)
df.pubmedid = r

r = df.conf_score
r = r.str.extract(r'(?:intact-miscore:)([0-9.]*)', expand=False)
df.conf_score = r

#define function to find uniprotIDs (based on RESTful queries of gene names) for entries which don't have a uniprotID in the dataframe
def Find_alt_ID(ID,organism):
    if type(ID) != str:
        return 'not a string'
    time.sleep(0.5)
    payload = {'query': 'gene:' + '\"'+ ID +'\"'+ 'AND organism:' + '\"' + organism + '\"' + 'AND reviewed:yes',
           'format': 'list'}

    result2 = requests.get(BASE + KB_ENDPOINT, params=payload)

    if result2.ok:
        return(result2.text).strip()
    else:
        print('Something went wrong ', result.status_code)

#Selection of entries w/o uniprotID (the clean-up step returned NaN when the protein ID column didn't have a uniprot ID)
#extraction of gene names, querying uniprot for protein IDs and replacing the non-uniprot IDs in the dataframe
sel1 = df.protein_a.isnull()
subset1 = df.loc[sel1,"alias_a"]
subset1 = subset1.str.extract(r'uniprotkb:([a-zA-Z0-9_-]*)\(gene name\)',expand=False)
subset1 = subset1.apply(lambda x : Find_alt_ID(x,'Human'))
subset1
df.loc[sel1,"protein_a"] = subset1

sel2 = df.protein_b.isnull()
subset2 = df.loc[sel2,"alias_b"]
subset2 = subset2.str.extract(r'uniprotkb:([a-zA-Z0-9_-]*)\(gene name\)',expand=False)
subset2 = subset2.apply(lambda x : Find_alt_ID(x,species))
df.loc[sel1,"protein_b"] = subset2

#filtering out the remaining null entries
sel1 = df.protein_a.isnull()
sel2 = df.protein_b.isnull()
df = df.loc[~sel1 & ~sel2,:]
df = df.drop(['alias_a','alias_b'],axis=1)
df = df.reset_index(drop=True)
print('the length of df after proteinID filtering is ' + str(len(df)))

#Reorganize df so that A_columns refer to the pathogen en B_columns to the human
df.taxid_a= df.taxid_a.apply(lambda x: str(x))
df.taxid_b = df.taxid_b.apply(lambda x: str(x))
for i in range(len(df)):
    if df.loc[i,"taxid_b"] != '9606':
        A = df.loc[i,"taxid_a"]
        B = df.loc[i,"taxid_b"]
        C = df.loc[i,"protein_a"]
        D = df.loc[i,"protein_b"]


        df.loc[i,"taxid_a"] = B
        df.loc[i,"taxid_b"] = A
        df.loc[i,"protein_a"]= D
        df.loc[i,"protein_b"]= C

#Filter out non-HPIs
sel = df.taxid_b == '9606'
df = df.loc[sel,:]
print('The length of df after filtering out non-HPIs is ' + str(len(df)))

#Make identifier for every interaction (based on ProteinIDs, detection method and pubmedID)
ID_all =[]
for i in range (0,len(df)):
    ID_list=[]
    ID_list.append (df.iloc[i,0])
    ID_list.append (df.iloc[i,1])
    ID_list.append (df.iloc[i,3])
    ID_list.append (df.iloc[i,2])
    ID_list.sort()
    ID_all.append(
        ID_list[0]
        +ID_list[1]
        + str(ID_list[2])
        +ID_list[3]
    )
df['id']=ID_all
print('There are ' +str(len(df.id.unique())) + ' unique interactions in df')

#Make identifier for entries of the PHISTO database (same way as previous identifier)
ID_all =[]
for i in range (0,len(PHISTO)):
    ID_list=[]
    ID_list.append (PHISTO.iloc[i,1])
    ID_list.append (PHISTO.iloc[i,2])
    ID_list.append (PHISTO.iloc[i,3])
    ID_list.append (str(PHISTO.iloc[i,4]))
    ID_list.sort()
    ID_all.append(
        ID_list[0]
        +ID_list[1]
        + ID_list[2]
        + ID_list[3]
    )
PHISTO['id'] = ID_all

PHISTO["taxid_b"]="9606"
PHISTO["source_db"]="PHISTO"

print('There are ' + str(len(PHISTO.id.unique())) + ' unique interactions in PHISTO')
#Merge PHISTO and df
#drop duplicates
df = pd.concat([df,PHISTO])
print('The merged dataframe has ' + str(len(df)) + ' interactions')
df = df.sort_values(by = "conf_score", ascending = False)
df = df.drop_duplicates("id")
print('The merged dataframe has ' + str(len(df)) + ' unique interactions')
df = df.reset_index()
df = df[["taxid_a","taxid_b","protein_a","protein_b","int_type","d_method","pubmedid","source_db","conf_score","id"]]
df.to_csv(results.target + species, sep ="\t")
print('The final interaction dataset can be found at' + results.target + species)

Int_DB = df
print('Start adding IPR')
Int_DB['ipr_a']=Find_IPR_terms(species,Int_DB.protein_a)
print('IPR terms added')
print('Start adding IPR hum')
Int_DB['ipr_b']=Find_IPR_terms_hum(Int_DB.protein_b)
print('IPR hum terms added')
Int_DB.to_csv(results.target+ species +"_IPR", sep ="\t")


print('start adding GO')
Int_DB['go_a']=Find_GO_terms(species,Int_DB.protein_a)
print('GO terms added')
print('start adding GO hum')
Int_DB['go_b']=Find_GO_terms_hum(Int_DB.protein_b)
print('GO hum terms added')
Int_DB.to_csv(results.target + species + '_IPR_GO', sep ="\t")
