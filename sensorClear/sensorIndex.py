# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * User: nihuan
 * Date: 18-4-24
 * Time: 下午2:46
 * Desc: 神策埋点清理
 """
__author__ = 'nihuan'


import os
import calendar
import shlex
import subprocess
file_dir = os.path.dirname(os.path.abspath(__file__))


def task_start():
    event_list = get_event_list()
    if event_list:
        for event in event_list:
            print("当前事件: " + event)
            get_month_list(event)
    return


def get_event_list():
    """所有事件信息"""
    all_sensor = file_dir + '/sensorDict/allSensor.txt'
    record = open(all_sensor, 'r')
    sensor_string = record.read()

    """埋点事件信息"""
    with_sensor = file_dir + '/sensorDict/withSensor.txt'
    with_record = open(with_sensor, 'r')
    with_string = with_record.read()
    with_list = with_string.split('\n')

    """检索出不在埋点列表里的事件"""
    all_list = []
    if sensor_string != "":
        line_str = sensor_string.split('\n')
        for line in line_str:
            sensor_event = line.split('\t')[0]
            if sensor_event not in with_list:
                all_list.append(sensor_event)
    return all_list


def get_month_list(event):
    year = 2017
    current_year = str(year)
    for month in range(1, 13):
        current_month = '%02d' % month
        print("当前月份: " + current_month)
        month_end = str(calendar.monthrange(year, month)[1])
        command = "sa_clean clean_event_by_date --begin " + current_year + "-" + current_month + "-01 --end " + current_year \
                  + "-" + current_month + "-" + month_end + \
                  " --event " + event + " --project default"
        process_info = os.system(command)
        print(process_info)


if __name__ == '__main__':
    task_start()
