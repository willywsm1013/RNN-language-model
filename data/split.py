import sys
'''
    This program is used to split one file into two files by split_ratio. 
'''

## Usage messege
if len(sys.argv) != 3:
    print ('*************************************************')
    print ('* Usage : python3 split.py <data> <split_ratio> *')
    print ('*************************************************')
    sys.exit()

data_path = sys.argv[1]
ratio = float(sys.argv[2])

assert ratio > 0 and ratio < 1,'split_ratio must between 0 and 1'

with open(data_path,'r') as f:
    lines = []
    for line in f :
        lines.append(line)

valid_num = int(len(lines)*ratio)

train = lines[valid_num:]
valid = lines[:valid_num]

with open('train.txt','w') as f:
    for line in train:
        print (line,file=f,end='')

with open('valid.txt','w') as f:
    for line in valid:
        print (line,file=f,end='')

