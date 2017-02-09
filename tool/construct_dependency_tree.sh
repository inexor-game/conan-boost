#!/bin/bash

DIR=boost_1_63_0
DISABLE_ALL=$(
	cd $DIR
	./b2 --show-libraries | grep '-' | sed 's/^.*- \(.*\)$/-o without_\1=True/g'
)

OUT=dependencies.txt
echo '{' > $OUT

for LIB in $(
	cd $DIR
	./b2 --show-libraries | grep '-' | sed 's/^.*- \(.*\)$/\1/g'
); do
	echo $LIB
	conan install -g env -o shared=False $(echo $DISABLE_ALL | sed "s/without_$LIB=True/without_$LIB=False/g") || exit 1
	rm -rf $DIR/bin.v2
	rm -f $DIR/stage/lib/*
	conan build > "build_${LIB}.log" 2>&1 || exit 2
	echo -n "    \"$LIB\": [" >> $OUT
	(
		cd $DIR/stage/lib
		echo -n '"'
		(ls *.a | sed 's/^libboost_\(.*\).a/\1/g' | xargs echo -n) | sed 's/ /", "/g' | tr -d '\n'
		echo -n '"'
	) >> $OUT
	echo "]," >> $OUT
done

echo '}' >> $OUT
