from snownlp import SnowNLP

from barrage.models import Barrage, Video, Results


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
        result = Results(bv=self.bv)

        for ele in qs:
            br = Barrage.objects.get(id=ele.id)
            br.sentiments = get_sentiment(ele.content)

            if br.sentiments < 0.1:
                result.zero += 1
            elif br.sentiments < 0.2:
                result.point_one += 1
            elif br.sentiments < 0.3:
                result.point_two += 1
            elif br.sentiments < 0.4:
                result.point_three += 1
            elif br.sentiments < 0.5:
                result.point_four += 1
            elif br.sentiments < 0.6:
                result.point_five += 1
            elif br.sentiments < 0.7:
                result.point_six += 1
            elif br.sentiments < 0.8:
                result.point_seven += 1
            elif br.sentiments < 0.9:
                result.point_eight += 1
            elif br.sentiments < 1:
                result.point_nine += 1
            else:
                result.one += 1

            score += br.sentiments
            br.save()

        result.positive = result.point_four + result.point_five + result.point_six + result.point_seven + result.point_eight
        + result.point_nine + result.one
        result.negative = result.zero + result.point_one + result.point_two + result.point_three
        result.total = count
        result.save()
        if count == 0:
            total = 0
        else:
            total = score / count
        video = Video.objects.get(bv=self.bv)
        video.sentiments = round(total, 2)
        video.status = 2
        video.save()
