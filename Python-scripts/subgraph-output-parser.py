import re
from GOremapping import Find_GO_name
import argparse


parser = argparse.ArgumentParser(description = 'translating GO IDs to GO terms')

parser.add_argument('-o', '--origin', default = '/Users/thesis/Desktop/', help = 'Enter path of file that you want to translate')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop/', help = 'Enter path for translated file')
results = parser.parse_args()

with open (results.origin,'r') as f:
    with open(results.target,'w') as w:
        pattern = re.compile(r'(GO:[0-9]*)')
        line = f.readline()
        for line in f:
            match = set(re.findall(pattern,line))
            for term in match:
                line = re.sub(term,Find_GO_name(term),line)
            w.write(line + '\n')
