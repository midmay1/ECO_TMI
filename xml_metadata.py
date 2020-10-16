import os
import re
import html
import xml.etree.ElementTree as ET

xml_folder = os.path.join(db_folder, 'PUBCHEM', 'XML')
cid_list = sorted([int(d.split('.')[-2]) for d \
                   in os.listdir(xml_folder) if '.xml' in d])

for cid in cid_list :
 xml_file = os.path.join(db_folder, 'PUBCHEM', 'XML', 'output.{}.xml'.format(cid))

 xml_data = ET.parse(xml_file).getroot()
 str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

 start_str = '<ns0:String>'
 end_str = start_str.replace('ns0', '/ns0')
 regex = re.compile(r'{}.*{}'.format(start_str, end_str))

 toxic_list = regex.findall(str_data)
 toxic_list = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_list]
print(toxic_list)
