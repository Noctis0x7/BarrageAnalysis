from snownlp import sentiment

if __name__ == '__main__':
    sentiment.train('../resources/pos.txt', '../resources/neg.txt')
    sentiment.save('barrage_sentiment.marshal')

