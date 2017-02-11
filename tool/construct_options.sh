#!/bin/bash

DIR=boost_1_63_0

(
	cd $DIR
	echo '    options = {'
	echo '        "shared": [True, False],'
	echo '        "header_only": [False, True],'
	echo '        "cxxdefines": "ANY",'
	echo '        "cxxflags": "ANY",'
	./b2 --show-libraries | grep '-' | sed 's/^.*- \(.*\)$/        "without_\1": [False, True],/g'
	echo '    }'
)
