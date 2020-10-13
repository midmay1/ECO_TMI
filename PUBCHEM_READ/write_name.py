import xml.etree.ElementTree as ET
import pubchempy as pcp
import cirpy as cp
from urllib.request import urlopen
import sys

f = open("INPUT",'r')
stringn = f.readline()
sid = int(stringn)

switch = 0
n = 0
m = 0

string0 = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"
string = string0 + "%d/XML/?response_type=display" % sid

url = string
response = urlopen(url)
web_source = response.read().decode("utf-8")
xtree = ET.fromstring(web_source)

for head in xtree.iter("{http://pubchem.ncbi.nlm.nih.gov/pug_view}TOCHeading"):
 if(head.text == "Ecotoxicity Values"):
  com = pcp.Compound.from_cid(stringn)
  sys.stdout = open("iupac_name","w")
  print('%d  %s  ' % (sid,com.iupac_name))
  sys.stdout.close()

  sys.stdout = open("smiles","w")
  print('%d  %s  ' % (sid,com.canonical_smiles))
  sys.stdout.close()


  cas = cp.resolve(com.canonical_smiles,'cas')
  sys.stdout = open("cas","w")
  if(str(type(cas)) == "<class 'list'>"):
   n = len(cas) 
   for i in range(0,n):
    print('%d  %s  ' % (sid,cas[i]))
  else: 
    print('%d  %s  ' % (sid,cas))
  sys.stdout.close()
