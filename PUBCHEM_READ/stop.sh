#!/bin/csh
if (! -e log) exit


set A = (`tail -n 1 log_old`)
set B = (`tail -n 1 log`)
set C = (`head -n 1 log`)
@ C = $C + 300000

echo $A
echo $B
echo $C
echo $PWD

