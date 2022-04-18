import pandas as pd
import re
import jieba
import os
from os import path
import io
import numpy as np


class Preprocess:
    def __init__(self, bv):
        self.bv = bv
        self.raw_dataset = pd.read_csv('./resources/raw_dataset/' + self.bv + '.csv', engine='python')

    # 预处理
    def preprocess(self):
        re_sub_vec = np.vectorize(self.re_sub)
        # 数据清洗
        self.raw_dataset['content'] = re_sub_vec(self.raw_dataset['content'])
        # 文本分词
        self.raw_dataset['content_list'] = self.raw_dataset['content'].map(self.sentence_split)
        seg_word = jieba4null()
        self.raw_dataset.loc[:, 'seg_words'] = self.raw_dataset['content_list'].map(seg_word.cut_sentence)
        self.raw_dataset = self.raw_dataset.drop(['content', 'content_list'], axis=1)
        # 存储处理后数据集
        self.raw_dataset.to_csv('./resources/dataset/' + self.bv + '.csv', encoding='utf_8', index=None)

    # 替换文本中的超链接和多余的空格
    def re_sub(self, text_l):
        if isinstance(text_l, str) and (text_l is not None):
            text_s = re.sub('\s+', ' ', text_l)
            text_s = re.sub(' ', ',', text_s)
            text_s = re.sub('#.+?#|\[.+?]|【.+?】', '', text_s)
            text_s = re.sub('https?:[a-zA-Z\\/\\.0-9_]+', '', text_s)
            text_s = re.sub('@.+?[,，：:\ )]|@.+?$', '', text_s)
            text_s = re.sub('我在(\\w){0,2}[:：](\\w*)', '', text_s)
            text_s = re.sub('\\[(\\w){1,4}\\]', '', text_s)
            text_s = re.sub('&[a-z]+;', '', text_s)
        else:
            text_s = str(text_l)
            text_s = self.re_sub(text_s)
        return text_s

    # 把每一条弹幕分割成单独的句子
    def sentence_split(self, content):
        sentence = str(content)
        sentence = re.sub('\u200b', '', sentence)
        result = re.split('。|？|！|\\.|\\?|\\!', sentence)
        return [ele for ele in result if len(ele) > 1]


class jieba4null:
    def __init__(self):
        self.rootdir = os.getcwd()
        self.STOP_WORDS_LIST = self.load_txt(path.join(self.rootdir, 'resources', 'stopwords_utf8.txt'))
        self.STOP_WORDS_LIST = set([re.sub('\n', '', item) for item in self.STOP_WORDS_LIST])
        jieba.load_userdict(path.join(self.rootdir, 'resources', 'emotion_user_dict.txt'))

    def filter_stop(self, input_text):
        for token in input_text:
            if token not in self.STOP_WORDS_LIST:
                yield token

    def cut_word(self, sent):
        words = self.filter_stop(jieba.cut(sent, cut_all=False))
        result = list(words)
        return list(filter(lambda x: x != '\u200b', result))

    def cut_sentence(self, sent_list):
        result = []
        for sent in sent_list:
            result.append(list(self.cut_word(sent)))
        return result

    def load_txt(self, file):
        with io.open(file, 'r', encoding='utf-8') as f_h:
            res = [line.encode('utf-8', 'ignore').decode('utf-8', 'ignore') for line in f_h]
            return res
