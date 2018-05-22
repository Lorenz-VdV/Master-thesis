#Study set: file met alle uniprotIDs die we willen bestuderen onder elkaar in 1 kolom (is een subset van de population set)
#Population set: file met alle uniprotIDs die we willen gebruiken als achtergrond onder elkaar in 1 kolom (bevat ook de study set)
#Association file: basically de population set met een tweede kolom in waarin alle GO termen in staan (; tussen termen en tab tussen de kolommen)

import pandas as pd
import numpy as np
from GOparsing import MakeP2GO, MakeP2GO_hum
from IPRparsing import MakeP2IPR, MakeP2IPR_hum
import argparse
import re
import GOremapping as gor

parser = argparse.ArgumentParser(description = 'making files for gene enrichment analysis')

parser.add_argument('-o', '--origin', default = '/Users/thesis/Desktop/', help = 'Enter path of interaction datasets that you want to analyse')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop/', help = 'Enter path for target files')
parser.add_argument('-s', '--species', default = None, help = 'Enter subject species')
parser.add_argument('-d', '--depth', default = '', help = 'Enter desired depth of GO terms')
parser.add_argument('-r', '--remap', action= 'store_true', help ='add flag if remapping is desired')
#parser.add_argument('-l', '--label', action= 'store_true', help= 'add flag if distinction between host and pathogen should be made')

results = parser.parse_args()

#label = results.label
#print('label is' + str(label))
species = results.species
remap = results.remap
print('remap is' + str(remap))

if remap == True:
    depth=int(results.depth)
    print ('assigning depths')
    gor.Assign_depth()

setup =''
if remap == True:
    setup= setup + '-depth-' + str(depth)
#if label == True:
    #setup= setup + '-label'

print('setup is' + setup)

with open(results.origin + species + 'IPR_GO_Remap','r') as f:
    with open(results.target + species + '-goa-study.txt','w') as w:
        proteins=[]
        for line in f:
            l = line.split()
            if l[0] != 'Taxid_A':
                proteins.extend([l[3],l[4]])
        proteins = set(proteins)
        for id in proteins:
            w.write(id + '\n')

with open(results.target + species + '-goa-association' + setup + '.txt','w') as x:
    with open(results.target + species + '-goa-population.txt','w') as y:
        GO_P = MakeP2GO(species)
        GO_H = MakeP2GO_hum()
        proteins = []
        proteins.extend(GO_P.keys())
        proteins.extend(GO_H.keys())
        for term in proteins:
            y.write(term + '\n')
            if term in GO_P.keys():
                x.write(term + '\t')
                for i in range(0,len(GO_P[term])):
                    x.write(GO_P[term][i])
                    if i != len(GO_P[term]):
                        x.write(',')
                x.write('\n')
            if term in GO_H.keys():
                x.write(term + '\t')
                for i in range(0,len(GO_H[term])):
                    x.write(GO_H[term][i])
                    if i != len(GO_H[term]):
                        x.write(',')
                x.write('\n')
