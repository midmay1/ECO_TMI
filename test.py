import xml.etree.ElementTree as ET


# import Utils_xml

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

        # info = (TE.split('.')[-2],TE.split('.')[-1])


def load(filename):
    XML = ET.parse('./' + filename)
    xml_data = XML.getroot()
    info = (filename.split('.')[-3], filename.split('.')[-2])
    idx = []
    con = []
    dur = []
    fur = []
    # print(ZE)
    for REC in xml_data.iter("RECORD"):
        for index in REC.iter("index"):
            idx.append(index.text)
        for conc in REC.iter("Concentration"):
            con.append(conc.text)
        for du in REC.iter("Duration"):
            dur.append(du.text)
        for fi in REC.iter("FI"):
            fur.append(fi.text)
    return info, idx, con, dur, fur


# TE = 'Zebra.EC50.xml'
# XML = ET.parse('./'+ TE )
# X_root = XML.getroot()
# print(X_root)

a = load('Zebra.EC50.xml')
# print(len(a[3]))
# print(a[0][166])

# r = TE.split('.')[1]
# info = (TE.split('.')[-2],TE.split('.')[-1])
# print(r)
# print(info)
root = ET.Element("Excel_XML")
node1 = ET.Element("RECORDS")
node1.text = " "
root.append(node1)

print(a[1][0])
for i in (a[1]):
    i = int(i) - 1
    # print(i)
    ind = a[1][i]
    # print(ind)
    if1 = str(a[0][0])
    if2 = str(a[0][1])
    if str(a[2][i]) == "None":
        C = ' '
    else:
        C = " ".join(["Concentration :", str(a[2][i])])

    if str(a[3][i]) == "None":
        D = ' '
    else:
        D = " ".join(["Duration :", str(a[3][i])])

    if str(a[4][i]) == "None":
        # if a[4][i] == "None" :
        F = ' '
    else:
        F = " ".join(["Further info:", str(a[4][i])])

    node2 = ET.SubElement(node1, "index")
    node2.text = ind
    node3 = ET.SubElement(node1, "Toxicity")
    node3.text = " "
    if D != ' ' and C != ' ' and F != ' ':
        node4 = ET.SubElement(node3, "Stings")
        # node4.text = a[0][0]+':'+a[0][1]+','+'Concentration :'+a[1]+'Duration :'+a[2]+'Further Info :'+a[3]
        # node4.text = join([a[0][0],':',a[0][1],'Concentration :',a[1],'Duration :',a[2],'Further Info :',a[3]])
        # node4.text = " ".join([if2,";",if1,";","Concentration : ",C,",","Duration :",D,",","Further info :",F])
        node4.text = " ".join([if2, ";", if1, ";", C, D, F])

# node2 = ET.SubElement(node1,"index")
# node2.text = "1"


indent(root)
ET.dump(root)