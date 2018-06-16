#coding:utf-8

import redis
import time
import json

class RedisCache:
    def __init__(self,redis_client):
        self._redis = redis_client

    def cache(self,timeout=0):
        def outter(func):
            def inner():
                #print('__inner__:%s'%timeout)
                r_data = self._redis.get('ptmp')
                if not r_data:
                    tmp = func()
                    self._redis .setex("ptmp",tmp,timeout)
                    r_data = tmp
                else:
                    r_data = json.loads(r_data.decode('utf-8'))
                    print('get data from redis')
                print(r_data)
            return inner
        return outter

redis_client = redis.Redis(host='127.0.0.1',port=6379,db=0)
cache = RedisCache(redis_client)

@cache.cache(timeout=10)
def execute():
    return json.dumps({'name':'jack'})

if __name__=='__main__':
    #redis_client.set('name','zhangsan')   # set
    #print(redis_client.get('name'))       # get
    execute()
    time.sleep(5)
    execute()

