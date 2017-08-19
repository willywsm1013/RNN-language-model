import sys,os
import subprocess
import string
'''
    This program will read all .txt file under current directory.
    Each line in <save_file_name> is lines in a .txt file separated by one <tab>.
'''

## usage messege
if len(sys.argv) != 2:
    print ('**************************************************')
    print ('* Usage : python3 preprocess.py <save_file_name> *')
    print ('**************************************************')
    sys.exit()

## get save path
save_file = sys.argv[1]

output_file = open(save_file,'w')

def tokenize(sentence):
    ret = []
    word = ''
    for char in sentence :
        if char in string.ascii_letters: 
            word += char.lower()
        else:
            if word != '':
                ret.append(word)
                word = ''
            if char != ' ':
                ret.append(char)
    if word != '':
        ret.append(word)
    return ret


## walk through all file under current directory
for root, dirs, files in  os.walk('./pre_subtitle_no_TC/'):
    for name in files:
        path = os.path.join(root,name)
        if os.path.isfile(path) and name.split('.')[-1]=='txt':
            print ('find %s'%path)
            
            ## read file
            with open(path,'r') as f:
                for line in f:
                    line = line.strip(' 　\n')
                    if line== '':
                        continue
                    line = tokenize(line)
                    print(' '.join(line),file=output_file)

output_file.close()
            
            

