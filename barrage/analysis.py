from snownlp import SnowNLP

from barrage.models import Barrage, Video


def get_sentiment(text):
    s = SnowNLP(text)
    return s.sentiments

class Analysis:
    def __init__(self, bv):
        self.bv = bv

    def run(self):
        qs = Barrage.objects.filter(bv=self.bv)
        score = 0.0
        count = len(qs)
        for ele in qs:
            br = Barrage.objects.get(id=ele.id)
            br.sentiments = get_sentiment(ele.content)
            score += br.sentiments
            br.save()
        total = score / count
        print(total)
        print(round(total, 2))
        video = Video.objects.get(bv=self.bv)
        video.sentiments = round(total, 2)
        video.status = 2
        video.save()
