import os
import torch
import string
class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
        #self.test = self.tokenize(os.path.join(path, 'test.txt'))
        
    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r') as f:
            tokens = 0
            for line in f:
                words = ['<bos>'] + line.split() + ['<eos>']
                tokens += len(words)
                for word in words:
                    self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r') as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                words = ['<bos>'] + line.split() + ['<eos>']
                for word in words:
                    ids[token] = self.dictionary.word2idx[word]
                    token += 1

        return ids
    def idx2word(self,idxs):
        ret = ''
        for idx in idxs:
            ret += self.dictionary.idx2word[idx[0]]
        return ret

def read_test(path,corpus,cuda):
    ## my tokenizer 
    def tokenize(text):
        ## pad begin-of-sentence
        ret = ['<bos>']
        word = ''
        for char in text :
            if char in string.ascii_letters: 
                word += char.lower()
            else:
                if word != '':
                    ret.append(word)
                    word = ''
                if char != ' ' and char != '　':
                    ret.append(char)
        if word != '':
            ret.append(word)
        ## pad end-of-sentence
        ret.append('<eos>')
        return ret
    with open(path,'r') as f:
        f.readline()
        test_data = []
        ## data format : id,dialogue,option
        for line in f:
            ## split each element using ','
            lines = line.strip('\n').split(',')

            ## dialogue is element 1
            dialogue = lines[1].split('\t')
            assert len(dialogue)<=3

            ## dialogue is element 2
            option = lines[2].split('\t')
            assert len(option) == 6 

            ## convert dialogue from word sequence to index sequence
            dialogue = [[corpus.dictionary.word2idx.get(w) for w in tokenize(d) if corpus.dictionary.word2idx.get(w) != None] for d in dialogue]
            dialogue = [w for sen in dialogue for w in sen]

            ## convert option from word sequence to index sequence
            option = [[corpus.dictionary.word2idx.get(w) for w in tokenize(o) if corpus.dictionary.word2idx.get(w) != None] for o in option]
     
            ## concat dialogue and option
            if cuda:
                combine = [torch.cuda.LongTensor(dialogue + o).view(-1,1) for o in option]
            else:
                combine = [torch.LongTensor(dialogue + o).view(-1,1) for o in option]

            test_data.append(combine)
    return test_data

