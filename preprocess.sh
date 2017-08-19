#!/bin/bash
cd data
echo 'merge data...'
python3 process.py data
echo 'spliting data...'
python3 split.py data 0.1 
rm data
cd ../
