import xml.etree.ElementTree as ET
import os

path = './SQL_XML'
OA = os.path.join(path, 'Overall_toxicity.xml')

xml_data = ET.parse(OA).getroot()
Tag_list = []
C = 0
for TA in xml_data.findall('./RECORD/'):
    if C < 38:
        #        print(TA.tag)
        Tag_list.append(TA.tag)
    C = C + 1

# print(Tag_list)
print(len(Tag_list))
nTag = int(len(Tag_list))

Info = []
i = 0
while i <= nTag:
    for TA in xml_data.iter(Tag_list[i]):
        # if TA.tag == Tag_list[i]:
        #    Tag_name = Tag_list[i]
        # Info.append(TA.text)

        print(TA.text)
    i = i + 1

# print(Info)

## dictionary