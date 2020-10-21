import os
import re
import html
import xml.etree.ElementTree as ET

db_folder = './V1_DATABASE/'
xml_folder = os.path.join(db_folder, 'PUBCHEM_xml')
cid_list = sorted([int(d.split('.')[-2]) for d \
                   in os.listdir(xml_folder) if '.xml' in d])
NZ = 0
NZ_C = 0
NM = 0
NM_C = 0
NF = 0
NF_C = 0
ND = 0
ND_C = 0
NO = 0
NO_C = 0

list_all=['toxic list:\n']
for cid in cid_list :
 switchZ = 0
 switchM = 0
 switchF = 0
 switchD = 0
 switchO = 0

 xml_file = os.path.join(db_folder, 'PUBCHEM_xml', 'output.{}.xml'.format(cid))

 xml_data = ET.parse(xml_file).getroot()
 str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

 start_str = '<ns0:String>'
 end_str = start_str.replace('ns0', '/ns0')
 regex = re.compile(r'{}.*{}'.format(start_str, end_str))

 toxic_list = regex.findall(str_data)
 toxic_list = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_list]

 for tox in toxic_list:
  if 'zebra fish' in tox or 'zebrafish' in tox or 'danio rerio' in tox or 'daniorerio' in tox :
   NZ = NZ + 1
   switchZ= 1
  elif 'fathead minnow' in tox or 'pimephales promelas' in tox :
   NF = NF + 1
   switchF = 1
  elif 'medaka' in tox or 'oryzias latipes' in tox:
   NM = NM + 1
   switchM = 1
  elif 'daphnia' in tox:
   ND = ND + 1
   switchD = 1
  else:
   NO = NO + 1


 if switchZ == 1 :
  NZ_C = NZ_C + 1
 if switchF == 1 :
  NF_C = NF_C + 1
 if switchM == 1 :
  NM_C = NM_C + 1
 if switchD == 1 :
  ND_C = ND_C + 1
 if switchF == 0 and switchZ == 0 and switchM == 0 and switchD == 0 :
  NO_C = NO_C + 1



print("number of zebrafish data:",NZ)
print("number of fathead data:",NF)
print("number of medaka data:",NM)
print("number of daphnia data:",ND)
print("number of others:",NO)

print("number of compounds have zebrafish:",NZ_C)
print("number of compounds have fathead:",NF_C)
print("number of compounds have medaka:",NM_C)
print("number of compounds have daphnia:",ND_C)
print("number of compounds have no species above:",NO_C)

