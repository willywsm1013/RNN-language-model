#!/bin/bash
cd data
echo 'process ptt data...'
python3 ptt_process.py data
echo 'spliting data...'
python3 split.py data 0.1 
rm data
cd ../
