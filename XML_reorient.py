import xml.etree.ElementTree as ET
import os
import numpy as np


def indent(elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def converting(n):
    path = './SQL_XML'
    OA = os.path.join(path, "excel.%d.xml" % n)
    xml_data = ET.parse(OA).getroot()
    root = ET.Element("Excel_XML")
    node1 = ET.Element("RECORDS")
    node1.text = " "
    root.append(node1)

    list = ["index", "name", "CAS", "IUPAC", "SMILES"]
    get = []
    for i in xml_data[0].iter():
        if i.text != "NaN" and i.tag != "RECORD" and i.tag not in list:
            get.append(i.tag)
        elif i.tag in list:
            node2 = ET.SubElement(node1, i.tag)
            node2.text = i.text

    if len(get) == 0:
        pass
    else:
        nslice = 3
        data = []
        l = nslice
        for i in range(0, len(get), nslice):
            data.append(get[i:l])
            l = l + nslice

        slice = 0
        for slice in range(0, len(data)):
            B = []
            for i in xml_data[0].iter():
                if len(get) != 0 and i.tag in data[slice]:
                    if i.tag[-1] == str(1) or i.tag[-1] == str(2):
                        i.tag = i.tag[:-1]
                        A = i.tag + " : " + i.text
                        B.append(A)
                    else:
                        A = i.tag + " : " + i.text
                        B.append(A)

            node2 = ET.SubElement(node1, "Toxicty")
            node2.text = "  ".join(B)

        indent(root)
        # ET.dump(root)
        tree = ET.ElementTree(root)
        tree.write('./환경부로토스/' + 'excel_new.%d.xml' % n, xml_declaration=True, encoding='utf8')


for j in range(1, 167):
    converting(j)

