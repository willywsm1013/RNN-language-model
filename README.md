# RNN-language-model
RNN based language model

This code is modified from pytorch example (https://github.com/pytorch/examples).

# Requirement
    * pytorch 0.2.0
# Usage
    1. Preprocess data
        (0) put pre_subtitle_no_TC directory downloaded from website into RNN-language-model/data/
        
        you can run bash preprocess.sh after step (0), then you can skip step (1)~(3)
        
        (1) cd RNN-language-model/data/ 
        (2) python3 process.py <file_name>
        (3) python3 split.py <data_file> <split_ratio>
        
    2. Start training
        * if you want to train under default argument :
            python3 main.py train 
        
        * if you have and you want to use GPU, add --cuda
            python3 main.py train --cuda

    3. Testing on AIFirst_test_problem.txt
        * put AIFirst_test_problem.txt into RNN-language-model/data/
        
        * test with default argument:
            python3 main.py test

        * you can specify the model you want to test by adding argument --save <model_name>
        * also, you can specify the path to save testing result by adding argument --test_output <output file name>
    
    4. Gernerating sentence
        * python3 generate.py --cuda --checkpoint <model_path>
            
