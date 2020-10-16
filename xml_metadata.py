import os
import re
import html
import xml.etree.ElementTree as ET

db_folder = './V1_DATABASE/'
xml_folder = os.path.join(db_folder, 'PUBCHEM_xml')
cid_list = sorted([int(d.split('.')[-2]) for d \
                   in os.listdir(xml_folder) if '.xml' in d])

N_LC50 = 0
N_EC50 = 0

N_LC50_C = 0
N_EC50_C = 0
N_data= 0


list_all=['toxic list:\n']
for cid in cid_list :
 switchL = 0
 switchE = 0

 xml_file = os.path.join(db_folder, 'PUBCHEM_xml', 'output.{}.xml'.format(cid))

 xml_data = ET.parse(xml_file).getroot()
 str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

 start_str = '<ns0:String>'
 end_str = start_str.replace('ns0', '/ns0')
 regex = re.compile(r'{}.*{}'.format(start_str, end_str))

 toxic_list = regex.findall(str_data)
 toxic_list = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_list]

 for tox in toxic_list:
  N_data = N_data + 1
  if 'LC50' in tox:
   N_LC50 = N_LC50 + 1
   switchL = 1
  elif 'EC50' in tox:
   N_EC50 = N_EC50 + 1
   switchE = 1

 if switchL == 1 :
  N_LC50_C = N_LC50_C + 1
 if switchE == 1 :
  N_EC50_C = N_EC50_C + 1

print(N_data)
print(len(cid_list))

print(N_LC50)
print(N_EC50)

print(N_LC50_C)
print(N_EC50_C)


