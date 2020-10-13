import xml.etree.ElementTree as ET
from urllib.request import urlopen
#from urllib import urlopen

#sid = 887 #702

f = open("INPUT",'r')
string = f.readline()
sid = float(string)

switch = 0
n = 0
m = 0

string0 = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"
string = string0 + "%d/XML/?response_type=display" % sid

url = string
response = urlopen(url)
web_source = response.read().decode("utf-8")
xtree = ET.fromstring(web_source)

print(int(sid))

for head in xtree.iter("{http://pubchem.ncbi.nlm.nih.gov/pug_view}TOCHeading"):
 if(head.text == "Ecotoxicity Values"):
  switch = 1

if(switch == 1):

 iid = 3
 for i in range(3,len(xtree)):
  if(xtree[iid][0].text == "Toxicity"): 
   iid = iid + 1
  else:
   xtree.remove(xtree[iid])

 child = xtree[3] #Toxicity 

 iid = 1
 for i in range(1,len(child)):
  if(child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}Section"):
   child.remove(child[iid])
  else:
   iid = iid + 1

 iid = 1 
 for i in range(1,len(child)):
  if(child[iid][0].text != "Toxicological Information"):
   child.remove(child[iid])
  else:
   iid = iid + 1
 
 g1child = child[1] #Toxicity - Section

 iid = 1
 for i in range(1,len(g1child)):
  if(g1child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}Section"):
   g1child.remove(g1child[iid])
  else:
   iid = iid + 1

 iid = 1
 for i in range(1,len(g1child)):
  if(g1child[iid][0].text != "Ecotoxicity Values"):
   g1child.remove(g1child[iid])
  else:
   iid = iid + 1

 g2child = g1child[1] #Toxicity - Section - Ecotoxicity Values

 iid = 1
 for i in range(1,len(g2child)):
  if(g2child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}Information"):
   g2child.remove(g2child[iid])
  else:
   iid = iid + 1
   
 for i in range(1,len(g2child)):
  g3child = g2child[i] #Toxicity - Section - Ecotoxicity Values - Information
  iid = 0
  for j in range(0,len(g3child)):
   if(g3child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}Value"):
    g3child.remove(g3child[iid])
   else:
    iid = iid + 1

 for i in range(1,len(g2child)):
  g3child = g2child[i] #Toxicity - Section - Ecotoxicity Values - Information
  for j in range(0,len(g3child)):
   g4child = g3child[j]
   iid = 0
   for k in range(0,len(g4child)):
    if(g4child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}StringWithMarkup"):
     g4child.remove(g4child[iid])
    else:
     iid = iid + 1

 for i in range(1,len(g2child)):
  g3child = g2child[i] #Toxicity - Section - Ecotoxicity Values - Information
  for j in range(0,len(g3child)):
   g4child = g3child[j] #Toxicity - Section - Ecotoxicity Values - Information - StringWithMarkup
   for k in range(0,len(g4child)):
    g5child = g4child[k] #Toxicity - Section - Ecotoxicity Values - Information - StringWithMarkup - String
    iid = 0
    for l in range(0,len(g5child)): 
     if(g5child[iid].tag != "{http://pubchem.ncbi.nlm.nih.gov/pug_view}String"):
      g5child.remove(g5child[iid])
     else:
      iid = iid + 1


 fstring = "output.%d.xml" % sid

 tree = ET.ElementTree(xtree)
 tree.write(fstring, encoding="utf-8",xml_declaration=True)

