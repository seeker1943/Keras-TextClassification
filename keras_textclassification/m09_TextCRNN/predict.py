# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/3 10:51
# @author   :Mo
# @function :train of CRNN with baidu-qa-2019 in question title


import numpy as np

from keras_textclassification.conf.path_config import path_embedding_random_char, path_hyper_parameters_fast_text
from keras_textclassification.conf.path_config import path_model_fast_text_baiduqa_2019
from keras_textclassification.etl.text_preprocess import PreprocessText
from keras_textclassification.m09_TextCRNN.graph import CRNNGraph as Graph
from keras_textclassification.base_utils.file_util import load_json

if __name__=="__main__":
    hyper_parameters = {'model': {'label': 17,
                                  'batch_size': 16,
                                  'embed_size': 30,
                                  'filters': [2, 3, 4],  # 论文中 filters=3
                                  'filters_num': 300,  # 论文中 filters_num=150,300
                                  'channel_size': 1,
                                  'dropout': 0.5,
                                  'decay_step': 100,
                                  'decay_rate': 0.9,
                                  'epochs': 20,
                                  'len_max': 50,
                                  'vocab_size': 20000,  # 这里随便填的，会根据代码里修改
                                  'lr': 1e-3,
                                  'l2': 0.001,
                                  'activate_classify': 'softmax',
                                  'embedding_type': 'random',  # 还可以填'random'、 'bert' or 'word2vec"
                                  'is_training': False,
                                  'model_path': path_model_fast_text_baiduqa_2019,
                                  'path_hyper_parameters': path_hyper_parameters_fast_text,
                                  'num_rnn_layers': 1,  # 论文是2，但训练实在是太慢了
                                  'rnn_type': 'LSTM',
                                  # type of rnn, select 'LSTM', 'GRU', 'CuDNNGRU', 'CuDNNLSTM', 'Bidirectional-LSTM', 'Bidirectional-GRU'
                                  'rnn_units': 256,  # large 650, small is 300
                                  },
                        'embedding': {'embedding_type': 'random',
                                      'corpus_path': path_embedding_random_char,
                                      'level_type': 'char',
                                      'embed_size': 30,
                                      'len_max': 50,
                                      },
                        # We also initialize the word vector for the unknown words from the uniform distribution [-0.25, 0.25].
                        }
    hyper_parameters = load_json(path_hyper_parameters_fast_text)

    pt = PreprocessText
    graph = Graph(hyper_parameters)
    graph.load_model()
    ra_ed = graph.word_embedding
    ques = '你好呀'
    ques_embed = ra_ed.sentence2idx(ques)
    pred = graph.predict(np.array([ques_embed]))
    pre = pt.prereocess_idx(pred[0])
    print(pre)
    while True:
        print("请输入: ")
        ques = input()
        ques_embed = ra_ed.sentence2idx(ques)
        pred = graph.predict(np.array([ques_embed]))
        pre = pt.prereocess_idx(pred[0])
        print(pre)