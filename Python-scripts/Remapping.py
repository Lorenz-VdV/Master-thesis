import pandas as pd
import numpy as np
import requests
from IPRparsing import Find_IPR_terms,Find_IPR_terms_hum
from GOparsing import Find_GO_terms,Find_GO_terms_hum
import argparse
BASE = 'http://www.uniprot.org'
KB_ENDPOINT = '/uniprot/'
TOOL_ENDPOINT = '/uploadlists/'

def map_retrieve(ids2map, source_fmt='ACC+ID',
                 target_fmt='ACC', output_fmt='list'):
    if hasattr(ids2map, 'pop'):
        ids2map = ' '.join(ids2map)
    payload = {'from': source_fmt,
               'to': target_fmt,
               'format': output_fmt,
               'query': ids2map,
               }
    response = requests.get(BASE + TOOL_ENDPOINT, params=payload)
    if response.ok:
        return response.text
    else:
        response.raise_for_status()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'remapping proteinIDs for GO and IPR')

    parser.add_argument('-o', '--origin', default = 'Users/thesis/Desktop', help = 'Enter path of map with interaction datasets that contain IDs that have to be remapped')
    parser.add_argument('-t', '--target', default = '/Users/thesis/Desktop', help = 'Enter path of map for target files')
    parser.add_argument('-s', '--species', default ='None', help = 'Enter subject species')
    results = parser.parse_args()

    species = results.species

    Int_DB = pd.read_table(results.origin + species + '_IPR_GO',
                            usecols=lambda x:x !="Unnamed: 0")

    sel1 = Int_DB.ipr_a.isnull()
    sel2 = Int_DB.ipr_b.isnull()
    sel3 = Int_DB.go_a.isnull()
    sel4 = Int_DB.go_b.isnull()

    listA = Int_DB.loc[sel1|sel3,'protein_a'].unique()
    listB = Int_DB.loc[sel2|sel4,'protein_b'].unique()

    Int_DB['a_remapped_from'] = np.nan
    Int_DB['b_remapped_from'] = np.nan

    with open(results.target +species +' alt-ids-a.txt','w') as w:
        for name in listA:
            sel = Int_DB.protein_a == name
            Int_DB.loc[sel,'a_remapped_from'] = name
            alt_id = map_retrieve(name)
            if len(alt_id) > 6:
                alt_id = alt_id.split()[0]
            Int_DB.loc[sel,'protein_a'] = alt_id.strip()
            w.write(name+ '\t' + alt_id.strip() + '\n')


    with open(results.target + species +' alt-ids-b.txt','w') as w:
        for name in listB:
            sel = Int_DB.protein_b == name
            Int_DB.loc[sel,'b_remapped_from'] = name
            alt_id = map_retrieve(name)
            if len(alt_id) > 6:
                alt_id = alt_id.split()[0]
            Int_DB.loc[sel,'protein_b'] = alt_id.strip()
            w.write(name + '\t' + alt_id.strip() + '\n')

    Int_DB.loc[sel1,'ipr_a'] = Find_IPR_terms(species,Int_DB.loc[sel1,'protein_a'])
    Int_DB.loc[sel2,'ipr_b'] = Find_IPR_terms_hum(Int_DB.loc[sel2,'protein_b'])
    Int_DB.loc[sel3,'go_a'] = Find_GO_terms(species,Int_DB.loc[sel3,'protein_a'])
    Int_DB.loc[sel4,'go_b'] =Find_GO_terms_hum( Int_DB.loc[sel4,'protein_b'])

    Int_DB.to_csv(results.target+ species + "IPR_GO_Remap", sep ="\t")
