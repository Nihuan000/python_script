# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * User: nihuan
 * Date: 18-4-18
 * Time: 上午10:24
 """
__author__ = 'nihuan'

import csv
import os
file_dir = os.path.dirname(os.path.abspath(__file__))


def un_match_reader():
    tag_list = []
    csv_file = csv.reader(open(file_dir + '/match/un_match.csv'))
    for file in csv_file:
        if file[0] != '':
            sub_tag = file[0].split('>>')[0]
            tag_list.append(sub_tag)
    return tag_list


def shop_tag_reader():
    shop_list = []
    shop_tag_file = csv.reader(open(file_dir + '/match/main_product.csv'))
    for tag in shop_tag_file:
        shop_list.append(tag)
    return shop_list


def csv_match():
    tag = un_match_reader()
    shop_tag = shop_tag_reader()
    for sub_tag in tag:
        tag_match_list = [sub_tag]
        for shop in shop_tag:
            shop_main_tag = shop[0]
            if sub_tag == shop_main_tag:
                tag_match_list.append(shop[1])

        if len(tag_match_list) == 1:
            write_csv(tag_match_list, 1)
        else:
            write_csv(tag_match_list, 2)


def write_csv(new_dict, match_type):
    if match_type == 1:
        file_name = '/result/标签未匹配结果.csv'
    else:
        file_name = '/result/标签已匹配结果.csv'
    new_csv = open(file_dir + file_name, 'a', newline="")
    csv_write = csv.writer(new_csv)
    csv_write.writerow(new_dict)


if __name__ == '__main__':
    csv_match()
