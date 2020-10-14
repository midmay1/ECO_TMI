import os
import re
import html
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

db_folder = './database_sample/'
#json_file_name = 'natural-unpd-81372-new-79553_with_MS.json'
json_file_name = 'SMILES_MS_v2.json'

def load_db():
    xml_folder = os.path.join(db_folder, 'PUBCHEM', 'XML')
    cid_list = sorted([int(d.split('.')[-2]) for d \
                       in os.listdir(xml_folder) if '.xml' in d])

    df = pd.DataFrame(columns=['cid', 'CAS', 'IUPAC', 'SMILES'])
    for i, cid in enumerate(cid_list):
        cas_file = os.path.join(db_folder, 'PUBCHEM', 'CAS', 'cas.{}.dat'.format(cid))
        iupac_file = os.path.join(db_folder, 'PUBCHEM', 'IUPAC', 'iupac_name.{}.dat'.format(cid))
        smiles_file = os.path.join(db_folder, 'PUBCHEM', 'SMILES', 'smiles.{}.dat'.format(cid))

        with open(cas_file) as f, open(iupac_file) as g, open(smiles_file) as h:
            cas = f.readlines()
            iupac_name = g.readlines()
            smiles = h.readlines()

        cas = [d.split('  ')[1] for d in cas]
        iupac_name = [d.split('  ')[1] for d in iupac_name][0]
        smiles = [d.split('  ')[1] for d in smiles][0]

        df.loc[i] = [cid, cas, iupac_name, smiles]
    
    msms_data_path = os.path.join(db_folder, json_file_name)
    with open(msms_data_path, 'r') as f:
        msms_data = json.load(f)
        
    return df, msms_data

def load_poison_info(searched_cid):
    toxic_list_all = ["PUBCHEM DATA\n"]
    try:
        xml_file = os.path.join(db_folder, 'PUBCHEM', 'XML',
                            'output.{}.xml'.format(searched_cid))

        xml_data = ET.parse(xml_file).getroot()
        str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')
    
        name_start_str = '<ns0:RecordTitle>'
        name_end_str = name_start_str.replace('ns0', '/ns0')
        regex = re.compile(r'{}.*{}'.format(name_start_str, name_end_str))
        name = regex.findall(str_data)[0]
        name = name.replace(name_start_str, '').replace(name_end_str, '')
    
        start_str = '<ns0:String>'
        end_str = start_str.replace('ns0', '/ns0')
        regex = re.compile(r'{}.*{}'.format(start_str, end_str))

        toxic_list = regex.findall(str_data)
        toxic_list = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_list]
        toxic_list_all = toxic_list_all + toxic_list
    except:
        print("NO PUBCHEM DATA")
        toxic_list_all = toxic_list_all + ["NO DATA\n"]
        name = "NO DATA"


    ##### TEST ###### read more files
    toxic_list_all = toxic_list_all + ["HANDMADE DATA\n"]
    try:
        xml_file = os.path.join(db_folder, 'PUBCHEM', 'XML',
                            'handmade.{}.xml'.format(searched_cid))

        xml_data = ET.parse(xml_file).getroot()
        str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

        start_str = '<Toxicty>'
        end_str = start_str.replace('T', '/T')
        regex = re.compile(r'{}.*{}'.format(start_str, end_str))

        toxic_app = regex.findall(str_data)
        toxic_app = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_app]

        toxic_list_all = toxic_list_all + toxic_app
    except:
        print("NO HANDMADE DATA")
        toxic_list_all = toxic_list_all + ["NO DATA\n"]


    ###############################################################

    return name, toxic_list_all

def plot_mass(ax, mz_array, intensity_array):
    mz_array = np.array(mz_array)
    intensity_array = np.array(intensity_array)
    
    ax.grid(True)
    ax.vlines(mz_array, 0, intensity_array, color='#173F5F')
    
    threshold_intensity = 60.0
    top_idx = np.where(intensity_array>=threshold_intensity)[0]
    top_mz_array = mz_array[top_idx]
    top_intensity_array = intensity_array[top_idx]
        
    for m, i in list(zip(top_mz_array, top_intensity_array)):
        ax.text(m, i+.5, s=round(m, 2), horizontalalignment='center', verticalalignment='bottom', fontsize=8)
    
    ax.set_ylim([-1.0, 109.5])

    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')
    
    plt.tight_layout()
    
    return ax