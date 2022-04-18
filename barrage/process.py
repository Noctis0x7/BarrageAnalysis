import pandas as pd


# 机械压缩去重方法
from barrage.models import Barrage


def compress(st: str):
    for i in range(1, int(len(st) / 2) + 1):
        for j in range(len(st)):
            if st[j:j+i] == st[j+i:j+2*i]:
                k = j + i
                while st[k:k+i] == st[k+i:k+2*i] and k < len(st):
                    k = k + i
                st = st[:j] + st[k:]
    return st


class Process:
    def __init__(self, bv):
        self.bv = bv
        self.raw_dataset = pd.read_csv('./resources/raw_dataset/' + self.bv + '.csv', engine='python',
                                       on_bad_lines='skip')
        self.flag = False
        self.msg = None
        self.s_flag = 0

    # 预处理
    def preprocess(self):
        # 缺失值等处理
        df = self.raw_dataset
        df = df.iloc[:, [1]]
        df = df.drop_duplicates()
        df = df.dropna()
        # 机械压缩去重
        df['content'] = df['content'].apply(compress)
        # 特殊字符过滤
        df['content'] = df['content'].str.extract(r"([a-zA-Z0-9\u4e00-\u9fa5，]+)")
        df = df.dropna()
        # 去除过短弹幕
        df = df[df['content'].apply(len) >= 2]
        df = df.dropna()
        df = df.drop_duplicates()
        # 存储
        df.to_csv('./resources/dataset/' + self.bv + '.csv', encoding='utf_8', index=None)

    # 存储
    def stroe(self):
        try:
            dataset = pd.read_csv('./resources/dataset/' + self.bv + '.csv')
            content_list = dataset.content.tolist()
            for content in content_list:
                Barrage.objects.create(content=content, bv=self.bv)
            self.msg = '存储到数据库成功！请选择下一步'
            self.s_flag = 1
            # path = './resources/dataset/' + bv + '.csv'
            # if os.path.exists(path):
            #     os.remove(path)
            # else:
            #     print('文件不存在：' + path)
        except Exception as e:
            print(e)
            self.msg = '存储失败！'
            self.s_flag = 0
