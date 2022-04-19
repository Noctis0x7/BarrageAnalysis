from barrage.models import Barrage, Video

if __name__ == '__main__':
    v = Video.objects.filter(status=2).values_list()
    print(v)

