import pandas as pd
import numpy as np
from GOparsing import Find_GO_terms,Find_GO_terms_hum
from IPRparsing import Find_IPR_terms, Find_IPR_terms_hum

parser = argparse.ArgumentParser(description = 'remapping proteinIDs for GO and IPR')

parser.add_argument('-o', '--origin', default = 'Users/thesis/Desktop', help = 'Enter path of interaction datasets that contain IDs that have to be remapped')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop', help = 'Enter path for target files')
parser.add_argument('-s', '--species', default ='None', help = 'Enter subject species')
results = parser.parse_args()

species = results.species

with open(results.origin + species + '_IPR_GO_Remap','r') as f:
    with open(origin.target + 'subgraph-mining-prep-int.txt','w') as w:
        for line in f:
            l = line.split()
            if l[0] != 'Taxid_A':
                w.write(l[3] + '\t'+l[4] + '\n')


with open(results.origin + species + '_IPR_GO_Remap','r') as f:
    with open(origin.target + 'subgraph-prep-GO-IPR.txt','w') as w:
        for line in f:
            l=line.split('\t')
            if Find_GO_terms(l[3]) != None:
                for i in range(len(Find_GO_terms(l[3]))):
                    w.write(l[3] + '\t' + Find_GO_terms(l[3])[i] + '\n')
            else:
                continue
            if Find_GO_terms_hum(l[4]) != None:
                for i in range(len(Find_GO_terms_hum(l[4]))):
                    w.write(l[4] + '\t' + Find_GO_terms_hum(l[4])[i] + '\n')
            else:
                continue

            if Find_IPR_terms(l[3]) != None:
                for i in range(len(Find_IPR_terms(l[3]))):
                    w.write(l[3] + '\t' + Find_IPR_terms(l[3])[i] + '\n')
            else:
                continue
            if Find_IPR_terms_hum(l[4]) != None:
                for i in range(len(Find_IPR_terms_hum(l[4]))):
                    w.write(l[4] + '\t' + Find_IPR_terms_hum(l[4])[i] + '\n')
            else:
                continue
