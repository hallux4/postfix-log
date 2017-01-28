#!/bin/bash

index=1
file_path=$1

reader=""

if [ $(file $file_path | grep ASCII | wc -l) -eq 0 ]
then
    reader="zcat $file_path"
else
    reader="cat $file_path"
fi

array=($( $reader | head -n 1))

for elem in ${array[@]}
do
    echo "$index $elem"
    index=$(($index+1))
done

