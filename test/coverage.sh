#!/bin/sh

coverage run test/pysumo_tests.py

for f in `ls test/gui/ | grep py`
do
		cat test/gui/$f
		coverage run --append test/gui/$f
		echo "hit enter to continue"
		read i
done
coverage report --include='src/*' > $1
