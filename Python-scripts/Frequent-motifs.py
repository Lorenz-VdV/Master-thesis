import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = 'extracing most frequent motifs')

parser.add_argument('-o', '--origin', default = '/Users/thesis/Desktop/', help = 'Enter path of file that you want to analyse')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop/', help = 'Enter path for output directory')
parser.add_argument('-n', '--number', default = 10, help = 'Enter how many frequent motifs you want')

results = parser.parse_args()
number = int(results.number)
db = pd.read_table(results.origin, header =None, names=["Motif", "FreqS", "FreqT","P-value"])
db_sorted = db.sort_values("FreqS",ascending = False)
db_to_write = db_sorted.iloc[:number,:]

db_to_write.to_csv(results.target + "/Frequent-motifs-" + str(results.number))
