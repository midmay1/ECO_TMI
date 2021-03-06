import os
import re
import html
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import datetime
import pickle

print("Start reading files...")
print(datetime.datetime.now())

db_folder = './database_sample/'

# 1 MS Database for version 1.0
MS_smiles = os.path.join(db_folder, 'Split_big', 'Name_MS.dat')

# 2 Pickle file name
db_pkl = "df.pkl"


def load_db():
    try:
        pickle_file = os.path.join(db_folder, db_pkl)
        with open(pickle_file, "rb") as file:
            df = pickle.load(file)
        print("READING PICKLE file!")

    except:
        cas_folder = os.path.join(db_folder, 'PUBCHEM', 'CAS')
        cid_list = sorted([int(d.split('.')[-2]) for d \
                           in os.listdir(cas_folder) if 'cas.' in d])

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

            # if cid == 525: print( cas, iupac_name, smiles )

        # Save data frame to pickle
        df.to_pickle(pickle_file)

    # msms_data_path = os.path.join(db_folder, json_file_name)
    # print(datetime.datetime.now())

    with open(MS_smiles, 'r') as file:
        msms_data = file.readlines()
        print("json Header loaded")
        # print(datetime.datetime.now())

    # print( df.index )
    # print( df.columns )
    # print( df.head() )

    return df, msms_data


################
def load_ms_info(smiles, msms):
    msms = [line.rstrip() for line in msms]

    db_folder = './database_sample/'

    for sm in range(0, len(msms)):
        try:
            if smiles == msms[sm]:
                try:
                    sm
                    data = os.path.join(db_folder, 'Split_big', 'MS.%d.json' % sm)
                    print(data)
                    with open(data, 'r') as f:
                        MS_data = json.load(f)
                except:
                    pass
        except:
            pass

    return MS_data


def load_poison_info(searched_cid, DBid):
    if DBid == 1:
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
        except:
            print("NO PUBCHEM DATA")
            toxic_list = ["NO DATA\n"]
            name = "NO DATA"
        return name, toxic_list

        ##### TEST ###### read more files
    if DBid == 2:
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

        except:
            print("NO HANDMADE DATA")
            toxic_app = ["NO DATA\n"]

        return toxic_app
        ##### read experiment files
    if DBid == 3:
        try:
            xml_file = os.path.join(db_folder, 'PUBCHEM', 'XML',
                                    'Experiment.{}.xml'.format(searched_cid))

            xml_data = ET.parse(xml_file).getroot()
            str_data = ET.tostring(xml_data, encoding='utf8').decode('utf8')

            start_str = '<Toxicity>'
            end_str = start_str.replace('T', '/T')
            regex = re.compile(r'{}.*{}'.format(start_str, end_str))

            toxic_app = regex.findall(str_data)
            toxic_app = [html.unescape(i.replace(start_str, '').replace(end_str, '')) for i in toxic_app]

        except:
            print("NO experiment DATA")
            toxic_app = ["NO DATA\n"]

        return toxic_app


def plot_mass(ax, mz_array, intensity_array):
    mz_array = np.array(mz_array)
    intensity_array = np.array(intensity_array)

    ax.grid(True)
    ax.vlines(mz_array, 0, intensity_array, color='#173F5F')

    threshold_intensity = 60.0
    top_idx = np.where(intensity_array >= threshold_intensity)[0]
    top_mz_array = mz_array[top_idx]
    top_intensity_array = intensity_array[top_idx]

    for m, i in list(zip(top_mz_array, top_intensity_array)):
        ax.text(m, i + .5, s=round(m, 2), horizontalalignment='center', verticalalignment='bottom', fontsize=15)

    ax.set_ylim([-1.0, 109.5])

    ax.set_xlabel('m/z', fontsize='xx-large')
    ax.set_ylabel('Intensity', fontsize='xx-large')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

    plt.tight_layout()
    return ax
