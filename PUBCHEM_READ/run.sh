#!/bin/csh -f

date

@ C = $1
while ($C < $2)

echo $C > INPUT
python3 read_pubchem.py >> log

if (-e output.$C.xml) echo $C >> ecolist.dat

@ C = $C + 1
end

date
