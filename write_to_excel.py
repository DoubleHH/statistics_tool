#coding:utf-8

# 分析iOS和Android工程中的统计，并生成一份对比的Excel表

import os
import time
import glob
from sys import argv
import operator

from public import all_stat_keys_from_code
from public import hh_excel_tool

def find_item(items, key):
    for item in items:
        if cmp(item[0], key) == 0:
            return item
    return None

def write_same_and_different_excel(all_ios_stat_items, all_android_stat_items):
    keys_same = []
    keys_ios_only = []
    keys_android_only = []
    keys_same_action_diff = []

    keys_ios = all_ios_stat_items.keys()
    for key in keys_ios:
        if all_android_stat_items.has_key(key):
            keys_same.append(key)
        else:
            keys_ios_only.append(key)

    keys_android = all_android_stat_items.keys()
    for key in keys_android:
        if keys_same.count(key) == 0:
            keys_android_only.append(key)

    all_android_stat_items_values = all_android_stat_items.values()
    for key in keys_ios_only:
        ios_item = all_ios_stat_items[key]
        key_deal = ios_item[0][:]
        key_deal = key_deal.replace("%@", "%s")
        if find_item(all_android_stat_items_values, key_deal) == None:
            continue
        keys_same_action_diff.append(key)

    print "All keys, iOS:%d, Android:%d, Same:%d, iOS only: %d, Android only:%d, SameKeyDiffAction:%d" % (len(keys_ios), len(keys_android), len(keys_same), len(keys_ios_only), len(keys_android_only), len(keys_same_action_diff))

    same_titles = ["key值", "action动作", "note注释(iOS)", "note注释(Android)"]
    same_sheet_items = [same_titles]
    for key in keys_same:
        ios_item = all_ios_stat_items[key][:]
        android_item = all_android_stat_items[key]
        ios_item.append(android_item[-1])
        same_sheet_items.append(ios_item)

    single_titles = ["key值", "action动作", "note注释"]
    ios_only_items = [single_titles]
    for key in keys_ios_only:
        ios_only_items.append(all_ios_stat_items[key])

    android_only_items = [single_titles]
    for key in keys_android_only:
        android_only_items.append(all_android_stat_items[key])

    same_key_diff_action_titles = ["key值", "action动作(iOS)", "action动作(Android)", "note注释(iOS)", "note注释(Android)"]
    same_key_diff_action_sheet = [same_key_diff_action_titles]
    for key in keys_same_action_diff:
        ios_item = all_ios_stat_items[key][:]
        key_dealed = (ios_item[0][:]).replace("%@", "%s")
        android_item = find_item(all_android_stat_items_values, key_dealed)
        # if android_item != None:
        ios_item.insert(2, android_item[1])
        ios_item.append(android_item[-1])
        same_key_diff_action_sheet.append(ios_item)

    sheet_array = []
    sheet_array.append(["Same", same_sheet_items])
    sheet_array.append(["iOS Only", ios_only_items])
    sheet_array.append(["Android Only", android_only_items])
    sheet_array.append(["SameKeyDiffAction", same_key_diff_action_sheet])
    hh_excel_tool.generate_excel(sheet_array, excel_name())

def excel_name():
    time_string = time.strftime('%Y%m%d_%H%M_%S', time.localtime(time.time()))
    return ("stat_" + time_string)

if __name__ == '__main__':
    if len(argv) < 1:
        print "Usage: python write_to_excel.py\n"
        exit(0)

    stat_code_path_ios = '/Users/doubleHH/waimai/WaimaiProject/c_waimai-app_ios/src/WaiMai/General/WMStatistic/WMStatisticsDefines.m'
    stat_code_path_android = '/Users/doubleHH/waimai/WaimaiProject/c_wmapp_android/library/waimaihostutils/src/com/baidu/lbs/waimai/waimaihostutils/stat/StatConstants.java'

    all_ios_stat_items = all_stat_keys_from_code.generate_ios_keys(stat_code_path_ios)
    all_android_stat_items = all_stat_keys_from_code.generate_java_keys(stat_code_path_android)

    write_same_and_different_excel(all_ios_stat_items, all_android_stat_items)
