import re
from GOremapping import Find_GO_name
import argparse


parser = argparse.ArgumentParser(description = 'translating GO IDs to GO terms')

parser.add_argument('-o', '--origin', default = '/Users/thesis/Desktop/', help = 'Enter path of file that you want to translate')
parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop/', help = 'Enter path for translated file')
results = parser.parse_args()

with open (results.origin,'r') as f:
    with open(results.target,'w') as w:
        pattern_GO = re.compile(r'(GO:[0-9]*)')
        pattern_4 = re.compile('-4')
        pattern_3 = re.compile('-3')
        pattern_2 = re.compile('-2')
        line = f.readline()
        for line in f:
            match_4 = re.search(pattern_4, line)
            match_3 = re.search(pattern_3,line)
            match_2 = re.search(pattern_2,line)
            if match_4:
                match_GO = set(re.findall(pattern_GO,line))
                if len(match_GO) == 4:
                    for term in match_GO:
                        line = re.sub(term,Find_GO_name(term),line)
                    w.write(line + '\n')
            elif match_3:
                match_GO = set(re.findall(pattern_GO,line))
                if len(match_GO) == 3:
                    for term in match_GO:
                        line = re.sub(term,Find_GO_name(term),line)
                    w.write(line + '\n')
            elif match_2:
                match_GO = set(re.findall(pattern_GO,line))
                if len(match_GO) == 2:
                    for term in match_GO:
                        line = re.sub(term,Find_GO_name(term),line)
                    w.write(line + '\n')
            else:
                continue
