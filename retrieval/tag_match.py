# -*- coding: utf-8 -*-
"""
 * Created by PyCharm Community Edition.
 * User: nihuan
 * Date: 18-4-3
 * Time: 下午12:47
 * Desc: 标签匹配脚本
 """
__author__ = 'nihuan'

import csv
import os


def task_start():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    tag_list = label_reader(file_dir)
    if tag_list is not None:
        dict_list = tag_dict_match(file_dir)
        for tag in tag_list:
            print("旧标签名: %s %s" % (tag[0], tag[1],))
            old_tag = tag[0] + '>>' + tag[1]
            tag_match_list = [old_tag]
            match_top_name = top_dict(tag[1])
            is_match = 0
            if match_top_name != '':
                dict_file = file_dir + '/dict/tag_dict/' + match_top_name + '.csv'
                match_dict = get_tag_match(tag[0], dict_file)
                if match_dict != '':
                    print("匹配类目: %s >> %s" % (match_top_name, match_dict))
                    tag_match_list.append(match_top_name + '>>' + match_dict)
                    is_match = 1

            if is_match == 0:
                for dictFile in dict_list:
                    dict_file_name = dictFile.split('/')[-1]
                    dict_name = dict_file_name.split('.')[0]
                    match_dict = get_tag_match(tag[0], dictFile)
                    if match_dict != '':
                        print("匹配类目: %s >> %s" % (dict_name, match_dict))
                        tag_match_list.append(dict_name + '>>' + match_dict)
            if len(tag_match_list) > 2:
                write_csv(tag_match_list, file_dir)


def label_reader(file_dir):
    tag_list = []
    csv_file = csv.reader(open(file_dir + '/match/sb_label.csv'))
    for file in csv_file:
        tag_list.append(file)
    return tag_list


def tag_dict_match(file_dir):
    dict_dir = file_dir + '/dict/tag_dict/'
    name = []
    for root, dirs, files in os.walk(dict_dir):
        for file in files:
            name.append(dict_dir + file)
    return name


def get_tag_match(tag, dict_file):
    muilt_tag = ''
    tag_csv_dict = csv.reader(open(dict_file))
    line_num = 0
    tag_index = []
    for tag_name in tag_csv_dict:
        if line_num == 0:
            tag_index = tag_name
        if tag in tag_name:
            muilt_index = tag_name.index(tag)
            tag_index_name = tag_index[muilt_index]
            muilt_tag = tag_index_name
        line_num += 1
    return muilt_tag


def top_dict(old_top):
    dict_list = {'针织类': '针织面料', '梭织类': '', '蕾丝/绣品': '蕾丝绣品', '皮革皮草': '皮革皮草', '其他面料': '其他面料', '辅料': '辅料', '加工服务': '加工服务'}
    return dict_list[old_top]


def write_csv(new_dict, file_dir):
    new_csv = open(file_dir + '/result/标签关联重复匹配结果.csv', 'a', newline="")
    csv_write = csv.writer(new_csv)
    csv_write.writerow(new_dict)


if __name__ == '__main__':
    task_start()
