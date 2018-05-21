# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * User: nihuan
 * Date: 18-5-9
 * Time: 下午3:36
 * Desc: 搜索关键词写入字典
 """
__author__ = 'nihuan'


import os
import json
import math
import time
import datetime
import re
from common.mysql import Db
from config.dbconfig import otherconfig
file_dir = os.path.dirname(os.path.abspath(__file__))

sbDb = Db()
page = otherconfig['page']
page_size = otherconfig['page_size']
last_id = 0
min_count = 3
last_day_count = 30
custom_dict = file_dir + '/custom.dic'
last_file = file_dir + '/logs/last_sync_time'
shop_match_regxp = '公司|纺织|布行|布业|市场'


def task_start():
    tag_list = []
    last_days = (datetime.datetime.now() - datetime.timedelta(days=+ last_day_count))
    last_time = int(time.mktime(last_days.timetuple()))
    try:
        local_time = time.localtime(int(last_time))
        print("最后同步时间: %s" % (time.strftime("%Y-%m-%d %H:%M:%S", local_time)))
        product_list = get_product_search(last_time)
        custom_dict_list = read_dict()
        if product_list:
            for file in product_list:
                key_count = len(file)
                first_count = 0
                if tag_list:
                    if tag_list[0][0] is not None:
                        first_count = len(tag_list[0][0])
                    if key_count >= first_count:
                        tag_list.insert(0, file)
                    else:
                        tag_list.append(file)
                else:
                    tag_list.append(file)
                tag_list = list(set(tag_list))
                tag_list.sort()
            if tag_list is not None:
                for key in tag_list:
                    key = key.strip()
                    if key in custom_dict_list:
                        print(r"字典 %s 已存在" % (key,))
                    elif len(key) > 6 or len(key) < 2:
                        print(r"关键词 %s 长度超限" % (key,))
                    elif key.isdigit():
                        print(r"关键词 %s 全数字" % (key,))
                    elif len(key.split(" ")) > 1:
                        print(r"关键词 %s 不合规" % (key,))
                    elif re.match("\b(?:%s)\b" % (shop_match_regxp,), key):
                        print(r"关键词 %s 包含店铺信息" % (key,))
                    else:
                        print(r"写入 %s 到字典" % (key,))
                        write_dict(key)
        sbDb.db_close()
    except ValueError:
        print("时间不存在 %s" % (json.dumps(last_time, )))


def get_product_search(day_time):
    tag_list = []
    print("搜索关键词检索开始:")
    table = 'sb_product_search_log'
    where = {'keyword': ['!=', "''"], 'search_time': ['>=', day_time], 'log_id': ['>', last_id]}
    fields = "log_id, keyword, count(distinct user_id) AS user_count"
    order = "log_id ASC"
    group = "keyword"
    keyword_count = sbDb.get_count(table, where, group, '')
    print(r"关键词个数: %s" % (keyword_count,))
    if keyword_count > 0:
        pages = int(math.ceil(keyword_count/page_size))
        for i in range(pages):
            result = sbDb.select_all(table, where, fields, page, page_size, order, group, '')
            if result is not None:
                for row in result:
                    where['log_id'] = ['>', row['log_id']]
                    keyword = r"%s" % (row['keyword'])
                    print(keyword)
                    user_count = row['user_count']
                    if user_count >= min_count:
                        tag_list.append(keyword)
    return tag_list


def get_last_time():
    last_times = []
    file_object = open(last_file, 'rU')
    try:
        for line in file_object:
            last_times.append(line.replace('\n', ''))
    finally:
        file_object.close()
    return last_times


def read_dict():
    dict_list = []
    custom_dict_reader = open(custom_dict, 'r')
    try:
        for line in custom_dict_reader:
            dict_list.append(line.replace('\n', ''))
    finally:
        custom_dict_reader.close()
    return dict_list


def write_dict(new_dict):
    try:
        dict_fo = open(custom_dict, 'a')
        dict_fo.write(new_dict + "\n")
    except IOError:
        print('写入字典数据失败:' + IOError.errno)


def write_last_time(last_time):
    try:
        time_object = open(last_file, 'w')
        last_time_string = '\n' . join(last_time)
        time_object.write(last_time_string)
    except IOError:
        print('写入更新时间失败:' + IOError.errno)


if __name__ == '__main__':
    task_start()
