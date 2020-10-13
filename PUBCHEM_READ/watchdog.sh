#!/bin/csh
if (! -e log) exit


set A = (`tail -n 1 $PWD/log_old`)
set B = (`tail -n 1 $PWD/log`)
set C = (`head -n 1 $PWD/log`)
@ C = $C + 300000

if ($C == $A) exit

if ($A == $B) then

 cp -r $PWD $PWD/../something_wrong_$B

 $PWD/run.sh $A $C

else 

 tail -n 1 log > log_old

endif


