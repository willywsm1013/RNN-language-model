###############################################################################
# Language Modeling on Penn Tree Bank
#
# This file generates new sentences sampled from the language model
#
###############################################################################

import argparse

import torch
from torch.autograd import Variable

import readline
import data

parser = argparse.ArgumentParser(description='PyTorch PTB Language Model')

# Model parameters.
parser.add_argument('--data', type=str, default='./data/format_data',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='./model.pt',
                    help='model checkpoint to use')
parser.add_argument('--outf', type=str, default='generated.txt',
                    help='output file for generated text')
parser.add_argument('--words', type=int, default='1000',
                    help='number of words to generate')
parser.add_argument('--seed', type=int, default=1111,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
parser.add_argument('--log-interval', type=int, default=100,
                    help='reporting interval')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    else:
        torch.cuda.manual_seed(args.seed)

if args.temperature < 1e-3:
    parser.error("--temperature has to be greater or equal 1e-3")

with open(args.checkpoint, 'rb') as f:
    model = torch.load(f)
model.eval()

if args.cuda:
    model.cuda()
else:
    model.cpu()

corpus = data.Corpus(args.data)
ntokens = len(corpus.dictionary)

while True:
    # input = Variable(torch.rand(1, 1).mul(ntokens).long(), volatile=True)
    inp = input('>> ')
    inpS = ['<bos>'] + inp.split()
    inpLen = len(inpS)
    ids = torch.LongTensor(inpLen, 1)

    token = 0
    hidden = model.init_hidden(1)

    for word in inpS[:-1]:
        id_ = corpus.dictionary.word2idx[word]
        ids = torch.LongTensor([[id_]])
        _input = Variable(ids, volatile=True)   
        if args.cuda:
            _input.data = _input.data.cuda()
        output, hidden = model(_input, hidden)


    id_ = corpus.dictionary.word2idx[inpS[-1]]
    ids = torch.LongTensor([[id_]])
    _input = Variable(ids, volatile=True)   
    if args.cuda:
        _input.data = _input.data.cuda()

    word = None
    outS = []
    while word != '<eos>':
        output, hidden = model(_input, hidden)
        word_weights = output.squeeze().data.div(args.temperature).exp().cpu()
        word_idx = torch.multinomial(word_weights, 1)[0]
        # _input = Variable(torch.LongTensor(word_idx), volatile=True)
        _input.data.fill_(word_idx)
        word = corpus.dictionary.idx2word[word_idx]
        outS.append(word)
    print(outS)
