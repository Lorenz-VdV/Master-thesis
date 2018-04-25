import pandas as pd
import numpy as np
from GOparsing import MakeP2GO, MakeP2GO_hum
from IPRparsing import MakeP2IPR, MakeP2IPR_hum
import argparse
import re
import GOremapping as gor

parser = argparse.ArgumentParser(description = 'making files for subgraph mining')

parser.add_argument('-o', '--origin', default = '/Users/thesis/Desktop/', help = 'Enter path of interaction datasets that you want to analyse')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop/', help = 'Enter path for target files')
parser.add_argument('-s', '--species', default = None, help = 'Enter subject species')
parser.add_argument('-d', '--depth', default = '', help = 'Enter desired depth of GO terms')
parser.add_argument('-r', '--remap', action= 'store_true', help ='add flag if remapping is desired')
parser.add_argument('-l', '--label', action= 'store_true', help= 'add flag if distinction between host and pathogen should be made')
results = parser.parse_args()

label = results.label
print('label is' + str(label))
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
if label == True:
    setup= setup + '-label'

print('setup is' + setup)

with open(results.origin + species + 'IPR_GO_Remap','r') as f:
    with open(results.target + species + '-subgraph-mining-prep-int.txt','w') as w:
        for line in f:
            l = line.split()
            if l[0] != 'Taxid_A':
                w.write(l[3] + '\t' + l[4] + '\n')

with open(results.origin + species + 'IPR_GO_Remap','r') as f:
    with open(results.target + species + '-subgraph-mining-prep-go-ipr' + setup + '.txt','w') as x:
        GO_P = MakeP2GO(species)
        GO_H = MakeP2GO_hum()
        IPR_P = MakeP2IPR(species)[1]
        IPR_H = MakeP2IPR_hum()[1]
        proteins = []
        for line in f:
            l = line.split()
            proteins.extend([l[3],l[4]])
        proteins = set(proteins)
        for i in proteins:
            if i in GO_P.keys():
                terms_to_write =[]
                go_terms = GO_P[i]
                if remap == False:
                    for term in go_terms:
                        terms_to_write.append(term)
                    if terms_to_write != []:
                        terms_to_write = set(terms_to_write)
                        for term in terms_to_write:
                            if label == True:
                                x.write(i + '\t' + term + '_P' + '\n')
                            else:
                                x.write(i + '\t' + term+ '\n')
                else:
                    for term in go_terms:
                        remapped_terms = gor.Remap(term,depth)
                        for item in remapped_terms:
                            terms_to_write.append(item)
                    if terms_to_write != []:
                        terms_to_write = set(terms_to_write)
                        for term in terms_to_write:
                            if label == True:
                                x.write(i + '\t' + term + '_P' + '\n')
                            else:
                                x.write(i + '\t' + term+ '\n')
            if i in IPR_P.keys():
                terms_to_write =[]
                ipr_terms = IPR_P[i]
                for term in ipr_terms:
                    terms_to_write.append(term)
                if terms_to_write != []:
                    terms_to_write = set(terms_to_write)
                    for term in terms_to_write:
                        if label == True:
                            x.write(i + '\t' + term + '_P' + '\n')
                        else:
                            x.write(i + '\t' + term+ '\n')

            if i in GO_H.keys():
                terms_to_write =[]
                go_terms = GO_H[i]
                if remap == False:
                    for term in go_terms:
                        terms_to_write.append(term)
                    if terms_to_write != []:
                        terms_to_write = set(terms_to_write)
                        for term in terms_to_write:
                            if label == True:
                                x.write(i + '\t' + term + '_H' + '\n')
                            else:
                                x.write(i + '\t' + term + '\n')

                else:
                    for term in go_terms:
                        remapped_terms = gor.Remap(term,depth)
                        for item in remapped_terms:
                            terms_to_write.append(item)
                    if terms_to_write != []:
                        terms_to_write = set(terms_to_write)
                        for term in terms_to_write:
                            if label == True:
                                x.write(i + '\t' + term + '_H' + '\n')
                            else:
                                x.write(i + '\t' + term + '\n')
            if i in IPR_H.keys():
                terms_to_write =[]
                ipr_terms = IPR_H[i]
                for term in ipr_terms:
                    terms_to_write.append(term)
                if terms_to_write != []:
                    terms_to_write = set(terms_to_write)
                    for term in terms_to_write:
                        if label == True:
                            x.write(i + '\t' + term + '_H' + '\n')
                        else:
                            x.write(i + '\t' + term + '\n')
