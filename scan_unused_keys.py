#coding:utf-8

# 扫描代码统计文件的key值是否在代码中使用了。

import os
import time
import glob
from sys import argv
import re
import operator

from public_pythons import all_stat_keys_from_code
from public_pythons import hh_print

def ag_shell(key, goal_path, ignore_path):
    ag_shell = ""
    if len(ignore_path) == 0:
        ag_shell = "ag -lc %s %s" % (key, goal_path)
    else:
        ag_shell = "ag -lc %s %s --ignore %s" % (key, goal_path, ignore_path)
    count = os.popen(ag_shell).readlines()
    return count

def find_unused_keys(keys, goal_path, ignore_path):
    if len(ignore_path) > 0 and ignore_path.startswith(goal_path) == False:
        hh_print.print_error(0, "搜索ignore地址有问题, 必须在目标地址级下")
        exit(0)
    relative_ignore_path = ""
    unused_keys = []
    if len(ignore_path) != 0:
        relative_ignore_path = ignore_path.replace(goal_path, "")
    # print "relative_ignore_path: %s" % (relative_ignore_path)
    index = 0
    for key_string in keys:
        index = index + 1
        if len(key_string) == 0:
            continue
        hh_print.print_color_string("搜索进度：%s" % (index * 100.0 / len(keys)), "green")
        count = ag_shell(key_string, goal_path, relative_ignore_path)
        if len(count) == 0:
            unused_keys.append(key_string)
    return unused_keys

def print_unused_keys(array):
    hh_print.print_color_string("代码中未使用的 KEYS: ", "brown")
    key_string = ""
    for key in array:
        key_string = key_string + key + '\n'
    hh_print.print_color_string(key_string, "red")

if __name__ == '__main__':
    if len(argv) < 1:
        print "Usage: python scan_unused_keys.py\n"
        exit(0)

    scan_code_folder = '/Users/doubleHH/waimai/WaimaiProject/c_waimai-app_ios/src/WaiMai/'
    ignore_path = scan_code_folder + 'General/WMStatistic/'
    stat_code_path_ios = ignore_path + 'WMStatisticsDefines.m'

    all_variables = all_stat_keys_from_code.generate_ios_variables(stat_code_path_ios)
    hh_print.print_color_string("all key count: %d" % (len(all_variables)), "lred")
    # hh_print.print_array(all_variables, "variables")
    # exit(0)
    unused_keys = find_unused_keys(all_variables, scan_code_folder, ignore_path)
    print_unused_keys(unused_keys)
