#!/bin/bash
sc2pm="scdoc2pmdb.jou"

for i in */
do
	cd ${i}
	cp ../${sc2pm} .
	sed -i "s/0/"${i%/}"/g" ${sc2pm}
	fluent 3ddp -meshing -t4 -gu -i ${sc2pm} > outpmdb.txt
	until [ -f ${i%/}.scdoc.pmdb ]
	do
    	 sleep 5
	done
	mv ${i%/}.scdoc.pmdb ${i%/}.pmdb
	echo "${i%/}.pmdb created"
	cd ../
done
