# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * User: nihuan
 * Date: 18-5-15
 * Time: 下午1:35
 * Desc: 
 """
__author__ = 'nihuan'

import csv
import os
file_dir = os.path.dirname(os.path.abspath(__file__))


def task_start():
    oss_list = label_reader()
    for img in oss_list:
        print(img)
        img_arr = img.split('/')
        if len(img_arr) == 5:
            bucket = 'oss://img-test/' + img_arr[-2] + '/' + img_arr[-1]
            print("bucket: %s" % (bucket,))
            suffix = bucket[-3:]
            header_update = oss_bucket_header(bucket, suffix)
            if header_update:
                print("meta update reslut: %s" % (header_update,))
                update_csv_line(img)
    return


def label_reader():
    tag_list = []
    csv_file = csv.reader(open(file_dir + '/source/bucket.csv'))
    for file in csv_file:
        is_oss_path = 0
        if file[0].find('http://127.0.0.1') or file[0].find('https://localhost'):
            is_oss_path = 1
        if len(file) == 2 and is_oss_path == 1:
            tag_list.append(file[0])
    return tag_list


def oss_bucket_header(bucket, suffix):
    content_type = 'image/jpeg'
    if suffix == 'jpg':
        content_type = 'image/jpeg'
    elif suffix == 'png':
        content_type = 'image/png'
    command = "./ossutil64 set-meta %s Content-Type:%s --update -r -f" % (bucket, content_type,)
    print(command)
    process_info = os.system(command)
    if process_info == 0:
        return 1
    else:
        return 0



def update_csv_line(img):
    csv_file = csv.reader(open(file_dir + '/source/1526622706.csv'))
    for line, file in enumerate(csv_file):
        if len(file) == 2 and file[0] == img:
            csv_new = file
            csv_new.append(1)
            write_result = write_csv(csv_new)
            print("write result: %s" % (write_result,))
    return


def write_csv(new_dict):
    new_csv = open(file_dir + '/source/malong_oss.csv', 'a', newline="")
    csv_write = csv.writer(new_csv)
    write_res = csv_write.writerow(new_dict)
    return write_res


 def delete_line(line):
     csv_delete_line = open(file_dir + '/source/bucket.csv').readlines()
     csv_delete_line[line] = ''
     with open(file_dir + '/source/bucket.csv', 'w') as f:
         f.writelines(csv_delete_line)


if __name__ == '__main__':
    task_start()
