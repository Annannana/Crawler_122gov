from threading import Thread
import requests
import json
import pymongo

'''
class gov(Thread):
    def __init__(self, limit):
        self.limit = limit
        self.pool = Queue()

    def run(self):
        for url in self.q:

    def get(self):
        if self.limit > 0:
            if self.queue
            self.limit -= 1
            return self.pool
'''
from multiprocessing import Pool


def getData(url):
    response = requests.get(url=url)
    datas = json.loads(response.text).get('data')
    for data in datas.get('content'):
        officehour = data['gzsjfw']
        phone = [data['lxdh']]
        address = data['lxdz']
        city = data['fzjg']
        gps = data['gps']
        lng = lat = ''
        if gps:
            gps = gps.split(',')
            lng = gps[0]
            lat = gps[1]
        name = data['wdmc']
        tag = data['ywfwms']
        item = {
            'officehour': officehour,
            'phone': phone,
            'address': address,
            'city': city,
            'lng': lng,
            'lat': lat,
            'name': name,
            'tag': tag,
        }
        client = pymongo.MongoClient(host='172.18.19.121')  # =MongoClient('mongodb://localhost:27017/')
        db = client["data-china"]  # =client.jingyu
        collection = db['china-122gov-life-190822']
        collection.insert_one(item)


if __name__ == '__main__':
    pool = Pool()
    l = []
    with open('yanjie.txt', 'r') as file:
        for line in file.readlines():
            l.append(line.strip())
    pool.map(getData, l)
