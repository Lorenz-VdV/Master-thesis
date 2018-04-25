import pandas as pd
import numpy as np
import os
import xlwt
import re

GO = open("../../Data-handling/Datasets/go-basic.obo", 'r')

Gene_entry =[]
all_entries =[]
relations=[]
GO_pattern=re.compile(r'GO:[0-9]*')

for line in GO:
    newentry = False
    x = line.split()
    if x !=[]:
            if x[0] == r'[Term]':
                Gene_entry.append(x[0])
            if x[0] == 'id:':
                Gene_entry.append(x[1])
            elif x[0] == 'name:':
                string=''
                for i in range(1,len(x)):
                    string = string + x[i] + ' '
                Gene_entry.append(string)
            elif x[0] == 'namespace:':
                Gene_entry.append(x[1])
            elif x[0] == 'is_a:':
                for i in range(1,len(x)):
                    if GO_pattern.match(x[i]):
                        relations.append(x[i])
            elif x[0] == 'is_obsolete:':
                Gene_entry.append(['obsolete'])
            else:
                continue
    else:
        if Gene_entry != []:
            if relations != []:
                Gene_entry.append(relations)
            if Gene_entry[0] == r'[Term]':
                all_entries.append((Gene_entry[1],Gene_entry[2:]))
                Gene_entry =[]
                relations=[]

GO_entries = dict(all_entries)

def Find_GO_name (GO_ID):
    return GO_entries[GO_ID][0]

def Find_GO_ID (GO_name):
    for key in GO_entries.keys():
        if GO_name == GO_entries[key][0]:
            return key


root=[Find_GO_ID('molecular_function '), Find_GO_ID('cellular_component '), Find_GO_ID('biological_process ')]


Map_list = []

for key in GO_entries.keys():
    if key not in root:
        Map_list.append((key,GO_entries[key][2]))



GO_Parents = dict(Map_list)
for key in root:
    GO_Parents[key]=[key]

def Find_Parent(GO_ID, levels):
    if GO_Parents[GO_ID] == ['obsolete']:
        return 'This GO ID is obsolete'
    Child_list = []
    Parent_list = [GO_ID]
    for x in range(0,levels):
        Child_list = Parent_list
        Parent_list =[]
        for y in range(0,len(Child_list)):
            Child = Child_list[y]
            Parents = GO_Parents[Child]
            for z in range(0,len(Parents)):
                Parent_list.append(Parents[z])
            #print(Child_list)
            #print (Parent_list)
    return Parent_list

def Find_Child(GO_ID,levels):
    if GO_Parents[GO_ID] == ['obsolete']:
        return 'This GO ID is obsolete'
    Child_list = [GO_ID]
    Parent_list = []
    specific_child_list=[]
    for x in range(0,levels):
        Parent_list = Child_list
        Child_list =[]
        for Parent in Parent_list:
            for key in GO_Parents.keys():
                if Parent in GO_Parents[key]:
                    specific_child_list.append(key)
            if specific_child_list != []:
                for term in specific_child_list:
                    Child_list.append(term)
            else:
                Child_list.append(Parent)

    return Child_list

def Assign_depth():
    for GO_ID in GO_entries.keys():
        if GO_Parents[GO_ID] == ['obsolete']:
            continue
        root_term = False
        depth =0
        inp=[GO_ID]
        outp=[]

        while not root_term:
            depth = depth +1
            for term in inp:
                for parent in Find_Parent(term,1):
                    outp.append(parent)

                for word in root:
                    if word in outp:
                        root_term = True
            inp = list(pd.unique(outp[:]))
            outp=[]

        GO_entries[GO_ID].append(depth)


for key in root:
    GO_entries[key]=GO_entries[key][:2]
    GO_entries[key].append(0)

def Remap (GO_ID, goal_depth):

#Tackling special situations
    if GO_ID not in GO_entries.keys():
        return 'None'
    if goal_depth == 0:
        return Find_GO_ID(GO_entries[GO_ID][2])

    if GO_Parents[GO_ID] == ['obsolete']:
        print (str(GO_ID) + 'This term is obsolete')
        return 'None'

    if goal_depth < 0:
        return("goal_depth can't be a negative integer")

#Determining max depth
    depth_list=[]
    for key in GO_entries.keys():
        if key in root:
            depth_list.append(0)
        else:
            if GO_Parents[key] != ['obsolete']:
                depth_list.append(GO_entries[key][3])
    max_depth = max(pd.unique(depth_list))
    if goal_depth > max_depth:
        return ('max depth in the GO DAG is '+ str(max_depth))

#Determining depth of given term
    if GO_ID in root:
        init_depth=0
    else:
        init_depth = GO_entries[GO_ID][3]
#trivial anwser
    if goal_depth == init_depth:
        return [GO_ID]
#diff < 0 means goal depth is more specific thus we need to find all child terms at goal depth
#diff>0 means goal depth is more general thus we need to find parents at goal depth
    else:
        diff = init_depth - goal_depth
        if diff < 0: #MAG NIET!!!! Voer check in met waarschuwing
            #print("You cannot map to terms with a higher depth. The depth of " + str(GO_ID)+ " is " + str(init_depth))
            return [GO_ID]
        elif diff>0:
            out_list=[]
            for i in range(0,init_depth):
                to_test = Find_Parent(GO_ID,i)
                for term in to_test:
                    if GO_entries[term][3] == goal_depth:
                        out_list.append(term)
            return list(pd.unique(out_list))
