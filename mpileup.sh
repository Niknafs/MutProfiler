#! /bin/bash

inputPos=$1
refSequence=$2
inputBam=$3
outputPrefix=$4

time while read line
do
samtools mpileup -f $refSequence -r "$line" \
    $inputBam  >> \
    $outputPrefix.mpileup \
    2> $outputPrefix.mpileup.log
done <  $inputPos



