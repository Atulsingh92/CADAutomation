#!/bin/bash
cad2pmdb="sld2pm.jou"

for i in */;
do
	cd ${i}
	cp ../${cad2pmdb} .
	sed -i "s/0/"${i%/}"/g" ${cad2pmdb}
	fluent 3ddp -meshing -t4 -gu -i ${cad2pmdb} > out.txt
	until [ -f ${i%/}.SLDPRT.pmdb ]
	do
    	 sleep 5
	done
	echo "${i%/}.SLDPRT.pmdb File created"
	cd ../
done
