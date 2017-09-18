import sys
import string

## usage messege
if len(sys.argv) != 2:
    print ('***************************************************')
    print ('* Usage : python3 ptt_process.py <save_file_name> *')
    print ('***************************************************')
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
            if char != ' ' and char != '\t':
                ret.append(char)
    if word != '':
        ret.append(word)
    return ret

with open('./Gossiping_processed','r') as f:
    for line in f:
        line = line.strip(' 　\n')
        if line== '':
            continue
        line = tokenize(line)
        print(' '.join(line),file=output_file)

output_file.close()
