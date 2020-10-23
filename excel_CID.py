import xml.etree.ElementTree as ET
import os
#import sys
import pubchempy as pcp

path = './SQL_XML'
OA = os.path.join(path, 'Overall_toxicity.xml')

# xml_data = ET.parse(OA).getroot()
tree = ET.parse(OA)
root=tree.getroot()
element = root[0] #get first child of root element

for chem in range(0,166):
    smiles = root[chem][4].text
    CID = str(pcp.get_compounds(smiles, 'smiles'))
    CID = CID.replace('[Compound(','').replace(')]','')
    print(CID)

    #for i in range(5,38):
    #    if str(root[chem][i].text) != "NaN":
    #        tag  = root[0][i].tag
    #        text = root[0][i].text
    #        merged = tag + " : " + text
    #        print(merged)
    #    else:
    #        tag  = root[0][i].tag
    #        text = root[0][i].text
    #        merged ="NO DATA " + tag + " : " + text
    #        print(merged)

#smiles = root[0][3].text
