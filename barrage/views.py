from django.shortcuts import render, HttpResponse
from barrage.crawl import BarrageCrawl
from barrage.preprocess import Preprocess
import pandas as pd
from barrage.models import RawDataSet, Barrage
import os


# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')


# 爬取模块
def barrage_crawl(request):
    bv = request.GET.get('bvnumber')
    spider = BarrageCrawl(bv)
    spider.run()
    if spider.flag == 1:
        RawDataSet(bv).save()
    return render(request, 'uploadResult.html', {
        'msg': spider.msg,
        'currentMsg': '爬取结果',
        'bv': bv
    })


# 上传页面
def upload(request):
    return render(request, 'upload.html')


# 上传数据集
def upload_file(request):
    if request.method == 'POST':
        up_file = request.FILES.get('upload_file', None)
        print(up_file.name.split('.')[0])
        if up_file is None:
            return HttpResponse('没有上传文件')
        else:
            bv = up_file.name.split('.')[0]
            # 打开特定的文件进行二进制的写操作
            with open('./resources/raw_dataset/%s' % up_file.name, 'wb+') as f:
                # 分块写入文件
                for chunk in up_file.chunks():
                    f.write(chunk)
            RawDataSet(bv).save()
            return render(request, 'uploadResult.html', {
                'msg': '上传成功',
                'currentMsg': '上传结果',
                'flag': True,
                'bv': bv
            })
    else:
        return render(request, 'uploadResult.html', {
            'msg': '上传失败，请检查文件格式是否正确',
            'currentMsg': '上传结果',
            'flag': False
        })


# 预处理和存储
def preprocess_store(request):
    bv = request.GET.get('bv')
    if None is bv:
        rawlist = list(RawDataSet.objects.all().values_list(flat=True))
        return render(request, 'preprocess.html', {
            'flag': -1,
            'rawlist': rawlist
        })
    else:
        raw_dataset = pd.read_csv('./resources/raw_dataset/' + bv + '.csv', nrows=10)
        short_list = raw_dataset.content.tolist()
        return render(request, 'preprocess.html', {
            'flag': 0,
            'bv': bv,
            'list': short_list
        })


# 预处理
def preprocess(request):
    bv = request.GET.get('bv')
    Preprocess(bv).preprocess()
    dataset = pd.read_csv('./resources/dataset/' + bv + '.csv', nrows=10)
    short_list = dataset.seg_words.tolist()
    RawDataSet.objects.get(bv=bv).delete()
    # path = './resources/raw_dataset/' + bv + '.csv'
    # if os.path.exists(path):
    #     os.remove(path)
    # else:
    #     print('文件不存在：' + path)

    return render(request, 'preprocess.html', {
        'flag': 1,
        'bv': bv,
        'list': short_list
    })


# 存储到数据库
def store(request):
    try:
        bv = request.GET.get('bv')
        dataset = pd.read_csv('./resources/dataset/' + bv + '.csv')
        content_list = dataset.seg_words.tolist()
        for content in content_list:
            Barrage.objects.create(content=content, bv=bv)
        store_msg = '存储到数据库成功！请选择下一步'
        s_flag = 1
        # path = './resources/dataset/' + bv + '.csv'
        # if os.path.exists(path):
        #     os.remove(path)
        # else:
        #     print('文件不存在：' + path)

    except Exception as e:
        print(e)
        store_msg = '存储失败！'
        s_flag = 0

    return render(request, 'preprocess.html', {
        'bv': bv,
        'store_msg': store_msg,
        's_flag': s_flag
    })


# 情感分析
def analysis(request):
    return


# 分析结果
def result(request):
    return


# 历史记录
def history(request):
    return
