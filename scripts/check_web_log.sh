#!/bin/bash

file_path=$1

reader=""

if [ $(file $file_path | grep ASCII | wc -l) -eq 0 ]
then 
    reader="zcat $file_path"
else
    reader="cat $file_path"
fi

echo "Please select the column you want to display. (SPACE BETWEEN NUMBER)"
read year
choice=($year)

i=0
length=${#choice[@]}

while [ $i -lt $length ]
do
    choice[$i]="\$${choice[$i]}"
    i=$(($i+1))
done

param=$(echo ${choice[@]} | tr -s ' ' ', ')

$reader | awk  '{ print '$param' }'

