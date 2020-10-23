import xml.etree.ElementTree as ET
import os
import html
import pubchempy as pcp
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
    OA = os.path.join(path, "Experiment.%d.xml" % n)
    xml_data = ET.parse(OA).getroot()
    root = ET.Element("Experiment_XML")
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
            if i.tag == "SMILES":
                print(i.text, "Smiles")
                CID = str(pcp.get_compounds(i.text, 'smiles'))
                CID = CID.replace('[Compound(', '').replace(')]', '')
                print(i.text, CID, "smiles and CID")

    if len(get) == 0:
        pass
    else:
        data = []
        data.append(get[0:3])
        data.append(get[4:8])

        for slice in range(0, len(data)):
            B = []
            for i in xml_data[0].iter():
                if len(get) != 0 and i.tag in data[slice]:
                    i.tag = html.unescape(str(i.tag))
                    i.text = html.unescape(str(i.text))
                    A = i.tag + " : " + i.text
                    B.append(A)

            node2 = ET.SubElement(node1, "Toxicity")
            node2.text = "  ".join(B)

        indent(root)
        # ET.dump(root)
        tree = ET.ElementTree(root)
        if CID == "NO DATA":
            pass
        else:
            tree.write('./환경부로토스/' + 'Experiment.%d.xml' % int(CID), xml_declaration=True, encoding='utf8')

for i in range(0, 13):
    try:
        print(i, "th converting")
        converting(i)
    except:
        pass

# converting(11)