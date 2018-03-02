import pandas as pd
import numpy as np
from GOparsing import Find_GO_terms,Find_GO_terms_hum
from IPRparsing import Find_IPR_terms, Find_IPR_terms_hum
import argparse
import re

parser = argparse.ArgumentParser(description = 'remapping proteinIDs for GO and IPR')

parser.add_argument('-o', '--origin', default = 'Users/thesis/Desktop', help = 'Enter path of interaction datasets that contain IDs that have to be remapped')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop', help = 'Enter path for target files')
parser.add_argument('-s', '--species', default ='None', help = 'Enter subject species')
results = parser.parse_args()

species = results.species

with open(results.origin + species + 'IPR_GO_Remap','r') as f:
    P_prot=[]
    H_prot=[]
    with open(results.target + 'subgraph-mining-prep-int.txt','w') as w:
        for line in f:
            l = line.split()
            if l[0] != 'Taxid_A':
                w.write(l[3] + '\t'+l[4] + '\n')
                P_prot.append(l[3])
                H_prot.append(l[4])


with open(results.origin + species + 'IPR_GO_Remap','r') as f:
    with open(results.target + 'subgraph-mining-prep-go-ipr.txt','w') as x:
        GO_P = Find_GO_terms(species,P_prot)
        GO_H = Find_GO_terms_hum(H_prot)
        IPR_P = Find_IPR_terms(species,P_prot)
        IPR_H = Find_IPR_terms_hum(H_prot)
        for line in f:
            counter= counter +1
            l=line.split()
            pattern = re.compile(r'[0-9]')
            if pattern.match(l[1]) != None:
                i = P_prot.index(l[3])
                if GO_P[i] != None:
                    for term in GO_P[i]:
                        x.write(l[3] + '\t' + term + '\n')
                if IPR_P[i] != None:
                    for term in IPR_P[i]:
                        x.write(l[3] + '\t' + term + '\n')

                j = H_prot.index(l[4])
                if GO_H[i] != None:
                    for term in GO_H[i]:
                        x.write(l[4] + '\t' + term + '\n')
                if IPR_H[i] != None:
                    for term in IPR_H[i]:
                        x.write(l[4] + '\t' + term + '\n')
