import xml.etree.ElementTree as ET
import os
import sys

path = './SQL_XML'
OA = os.path.join(path, 'Overall_toxicity.xml')

#xml_data = ET.parse(OA).getroot()


n = 0
JHead = "<RECORDS>"
JTail = "</RECORDS>"
with open(OA) as f:
    while n < 166:
        Head = f.readline()
        #print(Head)
        if Head.strip() == "<RECORD>":
            n = n+1
            sys.stdout = open("excel.%d.xml" %n,"w")
            print(JHead)
            print(Head)
            for i in range(1,40):
                Test = f.readline()
                print(Test)
            print(JTail)
