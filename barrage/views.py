from django.shortcuts import render, HttpResponse

from barrage.analysis import Analysis
from barrage.crawl import BarrageCrawl
from barrage.process import Process
import pandas as pd
from barrage.models import Video, Barrage, Results


# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')


# 爬取模块
def barrage_crawl(request):
    bv = request.GET.get('bv')
    spider = BarrageCrawl(bv)
    spider.run()
    flag = False

    if spider.flag == 1:
        try:
            Video.objects.get(bv=bv).delete()
        except Exception as e:
            print(e)
        finally:
            Video.objects.create(bv=bv, status=0, title=spider.title, up=spider.up, views=spider.views)
            flag = True

    return render(request, 'uploadResult.html', {
        'msg': spider.msg,
        'currentMsg': '爬取结果',
        'bv': bv,
        'flag': flag
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
            try:
                Video.objects.get(bv=bv).delete()
            except Exception as e:
                print(e)
            finally:
                Video.objects.create(bv=bv, status=0)
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


# 预处理和存储请求
def preprocess_store(request):
    bv = request.GET.get('bv')
    if None is bv:
        rawlist = list(Video.objects.exclude(status=2).values_list(flat=True))
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


# 数据清洗
def data_clean(request):
    bv = request.GET.get('bv')
    clean_list = Process(bv=bv).data_clean()
    return render(request, 'preprocess.html', {
        'flag': 1,
        'bv': bv,
        'list': clean_list
    })


# 文本分词
def word_cut(request):
    bv = request.GET.get('bv')
    cut_list = Process(bv=bv).word_cut()
    return render(request, 'preprocess.html', {
        'flag': 2,
        'bv': bv,
        'list': cut_list
    })


# 去停用词
def stop_words(request):
    bv = request.GET.get('bv')
    stop_list = Process(bv=bv).stop_words()
    return render(request, 'preprocess.html', {
        'flag': 3,
        'bv': bv,
        'list': stop_list
    })


# 存储到数据库
def store(request):
    bv = request.GET.get('bv')
    ps = Process(bv)
    ps.store()
    return render(request, 'preprocess.html', {
        'bv': bv,
        'store_msg': ps.msg,
        's_flag': ps.s_flag
    })


# 情感分析
def analysis(request):
    bv = request.GET.get('bv')
    if bv is not None:
        Analysis(bv).run()
        flag = 1
        analysis_list = []
    else:
        flag = 0
        analysis_list = list(Video.objects.exclude(status=2).values_list(flat=True))
    return render(request, 'analysis.html', {
        'bv': bv,
        'flag': flag,
        'list': analysis_list
    })


# 分析结果
def result(request):
    bv = request.GET.get('bv')
    if bv is not None:
        video = Video.objects.get(bv=bv)
        result = Results.objects.get(bv=bv)
        return render(request, 'result.html', {
            'bv': bv,
            'result': result,
            'data': [result.zero, result.point_one, result.point_two, result.point_three, result.point_four,
                     result.point_five, result.point_six, result.point_seven, result.point_eight,
                     result.point_nine, result.one],
            'video': video
        })
    else:
        results = Video.objects.filter(status=2)
        return render(request, 'resultlist.html', {
            'results': results
        })


# 删除数据
def delete(request):
    bv = request.GET.get('bv')
    video = Video.objects.get(bv=bv)
    video.delete()
    Barrage.objects.filter(bv=bv).delete()
    return result()
