#!/usr/bin/python3
#Read file $1 and convert to $2
from tabulate import tabulate
from sys import argv

data = []
f1 = open(argv[1], "r")
for line in f1:
	nw = line.split()
	if len(nw) != 4:
		continue
	data.append(nw)
f1.close()

rst = tabulate(data[1:], headers=data[0],tablefmt='rst')

f2 = open(argv[2], "w")
f2.write("Statement Coverage of pysumo and pySUMOQt\n======================================================\n")
f2.write(rst)
f2.write("\n")
f2.close()
