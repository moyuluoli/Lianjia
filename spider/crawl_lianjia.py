import os
import logging
from config.configs import *

import time
import pymongo
import elasticsearch

# 更新数据前先删除当天已经存在的数据库
def drop_database():
    client = pymongo.MongoClient()
    # es = elasticsearch.Elasticsearch()
    if client[newhousedb()]:
        client.drop_database(newhousedb())
    if client[ershoufangdb()]:
        client.drop_database(ershoufangdb())
    if client[rentdb()]:
        client.drop_database(rentdb())

    # if es.indices.exists(ershoufangdb()):
    #     es.indices.delete(ershoufangdb())
    # if es.indices.exists(newhousedb()):
    #     es.indices.delete(newhousedb())
    # if es.indices.exists(rentdb()):
    #     es.indices.delete(rentdb())


def crawl_ershoufang():
    os.chdir('lianjia_ershoufang')
    print(os.getcwd())
    logging.info('成功进入{}'.format(os.getcwd()))
    ershoufang_crawl = os.system('scrapy crawl ershoufang')
    os.chdir(os.pardir)
    print(os.getcwd())


def crawl_newhouse():
    newhouse_dir = os.chdir('lianjia_newhouse')
    print(os.getcwd())
    logging.info('成功进入{}'.format(os.getcwd()))
    newhouse_crawl = os.system('scrapy crawl newhouse')
    os.chdir(os.pardir)
    print(os.getcwd())


def crawl_rent():
    rent_dir = os.chdir('lianjia_rent')
    print(os.getcwd())
    logging.info('成功进入{}'.format(os.getcwd()))
    rent_crawl = os.system('scrapy crawl rent')
    os.chdir(os.pardir)
    print(os.getcwd())


def crawl_lianjia():
    print(os.getcwd())
    os.chdir('spider')
    drop_database()
    spider_status = '正在爬取二手房数据'
    crawl_ershoufang()
    spider_status = '正在爬取新房数据'
    print(os.getcwd())
    crawl_newhouse()
    spider_status = '正在爬取租房数据'
    print(os.getcwd())
    crawl_rent()
    data_update_time = int(time.time())
    os.chdir(os.pardir)


if __name__ == '__main__':
    crawl_lianjia()
