from datetime import datetime

from barrage.models import Barrage, Video

if __name__ == '__main__':
    year = datetime.today().year
    print(year)
    pub_time = '04-15'
    print(pub_time)
    pub_time = str(year) + '-' + pub_time
    print(pub_time)

