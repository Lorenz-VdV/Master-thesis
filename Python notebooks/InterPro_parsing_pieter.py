
# coding: utf-8

import re
import numpy as np
import pandas as pd


Int_DB = pd.read_table("Extracted datasets/Yersinia pestis", usecols=lambda x:x !="Unnamed: 0")


# Nieuwe implementatie
unique_ac = set(pd.unique(Int_DB[['Protein_A', 'Protein_B']].values.ravel()))

print(len(unique_ac))

# #zelfde code als hierboven maar dan voor de grote file
with open ('protein2ipr.dat','r') as f:
    with open ('ipr_out.txt','w') as w:
        outer_counter = 0
        for line in f:
            outer_counter += 1
            if outer_counter % 10000000 == 0:
                print('Processed',outer_counter,'lines')
            l = line.split('\t')[0]
            # print(l[0])
            # if l[0] in Int_DB.Protein_A or l[0] in Int_DB.Protein_B:
            if l in unique_ac:
                # print('Woohoo!')
                w.write(line)

# Versie Lorenz

# print(len(Int_DB.Protein_A))
# print(len(Int_DB.Protein_B))

# # #zelfde code als hierboven maar dan voor de grote file
# with open ('protein2ipr.dat','r') as f:
#     with open ('ipr_out.txt','w') as w:z
#         for line in f:
#             l = line.split('\t')
#             # print(l[0])
#             if l[0] in Int_DB.Protein_A or l[0] in Int_DB.Protein_B:
#                 w.write(line)
