import jieba
import pandas as pd

from barrage.models import Barrage, Video


# 机械压缩去重方法
def compress(st: str):
    sa = []  # 定义一个空列表
    de_str = ''  # 定义一个空字符
    for i in st:
        if len(sa) == 0:
            sa.append(i)
        else:
            if i == de_str:  # 判断是否与上一个删除元素相同
                continue  # 相同则不做任何处理
            elif i == sa[-1]:  # 继续判断是否与倒数第二个元素相同
                de_str = sa.pop(-1)  # 相同赋值给删除字符，不放入列表
            else:
                sa.append(i)  # 如果都不是，则放入列表
    print("".join(sa))
    return "".join(sa)


# jieba分词方法
def jieba_cut(st: str):
    seg_list = jieba.cut(st)
    return " ".join(seg_list).split()


# 去停用词
def filter_stop(words):
    stopwords = [line.strip() for line in open('./resources/stopwords.txt', encoding='UTF-8').readlines()]
    words = words.replace("[", '')
    words = words.replace("]", '')
    words = words.replace("'", '')
    words = words.split(', ')
    return [w for w in words if w not in stopwords]


class Process:
    def __init__(self, bv):
        self.bv = bv
        self.raw_dataset = pd.read_csv('./resources/raw_dataset/' + self.bv + '.csv', engine='python',
                                       on_bad_lines='skip')
        self.flag = False
        self.msg = None
        self.s_flag = 0

    # 数据清洗
    def data_clean(self):
        # 缺失值等处理
        df = self.raw_dataset
        df = df.drop_duplicates()
        df = df.dropna()
        # 机械压缩去重
        df['clean_data'] = df['content'].apply(compress)
        # 特殊字符过滤
        df['clean_data'] = df['clean_data'].str.replace("[^\u4e00-\u9fa5，]+", '')
        df = df.dropna()
        # 去除过短弹幕
        df = df[df['clean_data'].apply(len) >= 2]
        df = df.dropna()
        df = df.drop_duplicates()

        df.to_csv('./resources/dataset/' + self.bv + '.csv', encoding='utf_8', index=None)
        clean_list = pd.read_csv('./resources/dataset/' + self.bv + '.csv', nrows=10)
        return clean_list.clean_data.tolist()

    # 文本分词
    def word_cut(self):
        df = pd.read_csv('./resources/dataset/' + self.bv + '.csv')
        df['cut_word'] = df['clean_data'].apply(jieba_cut)
        df.to_csv('./resources/dataset/' + self.bv + '.csv', encoding='utf_8', index=None)
        cut_word_list = pd.read_csv('./resources/dataset/' + self.bv + '.csv', nrows=10)
        return cut_word_list.cut_word.tolist()

    # 去停用词
    def stop_words(self):
        df = pd.read_csv('./resources/dataset/' + self.bv + '.csv')
        df['stop_word'] = df['cut_word'].apply(filter_stop)
        df.to_csv('./resources/dataset/' + self.bv + '.csv', encoding='utf_8', index=None)
        cut_word_list = pd.read_csv('./resources/dataset/' + self.bv + '.csv', nrows=10)
        return cut_word_list.stop_word.tolist()

    # 存储
    def store(self):
        try:
            dataset = pd.read_csv('./resources/dataset/' + self.bv + '.csv')
            content_list = dataset.content.tolist()
            for content in content_list:
                Barrage.objects.create(content=content, bv=self.bv)
            self.msg = '存储到数据库成功！请选择下一步'
            self.s_flag = 1
            video = Video.objects.get(bv=self.bv)
            video.status = 1
            video.save()
            # path = './resources/dataset/' + bv + '.csv'
            # if os.path.exists(path):
            #     os.remove(path)
            # else:
            #     print('文件不存在：' + path)
        except Exception as e:
            print(e)
            self.msg = '存储失败！'
            self.s_flag = 0
