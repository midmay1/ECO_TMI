#!/bin/csh -f

set L = `cat ./CIDlist.dat | wc -l`
@ L = $L + 1

@ C = 1
while ($C < $L)

set D = `sed -n ${C}p ./CIDlist.dat`
echo $D > INPUT
python3 read_pubchem.py >> log
python3 write_name.py

if (-e ./iupac_name) then
 mv iupac_name iupac_name.$D.dat
 mv smiles     smiles.$D.dat
 mv cas        cas.$D.dat

endif

@ C = $C + 1
end

echo 'finished'
