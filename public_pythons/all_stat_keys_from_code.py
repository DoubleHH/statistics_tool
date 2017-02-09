#coding:utf-8

# 描述：把iOS代码定义统计文件里的统计生成一个key的字典集合

import os
import time
import glob
from sys import argv
import re
import operator
import hh_print

# iOS统计Key的正则
RE_KEY_IOS = re.compile(r"@\".*\"")
# Android统计Key的正则
RE_KEY_ANDROID = re.compile(r"\".*\"")
# 变量名的正则
PATTERN_FOR_VARIABLE = re.compile(r"WM_STAT_.*=")

# 统计中四种action
ACTIONS = ['click', 'show', 'collect', 'ready']

# 检查action是否是统计中的四种之一
def check_action(action):
    global ACTIONS
    for value in ACTIONS:
        if cmp(value, action) == 0:
            return True
    return False

# 在一行字符串中找到key，action等信息
def find_ios_key_with_line(line):
    global RE_KEY_IOS
    match = RE_KEY_IOS.search(line)
    result = []
    error = ""
    if match:
        key_action_str = match.group()
        key_action_str = key_action_str[2:(len(key_action_str) - 1)]
        key_action_arr = key_action_str.split()
        if len(key_action_arr) < 2:
            error = "ios (%s), key或者Action值有问题" % (line)
        else:
            result = key_action_arr
    if len(result) == 0:
        error = "ios (%s), 未能解析出值" % (line)
    return [result, error]

# 在一行字符串中找到统计值的iOS定义变量名
def find_ios_variable(line):
    global PATTERN_FOR_VARIABLE
    match = PATTERN_FOR_VARIABLE.search(line)
    variable = ""
    error = ""
    if match:
        string = match.group()
        string = string[0:(len(string) - 1)]
        string = string.strip()
        variable = string
    else:
        error = "(%s) 未找到变量名" % (line)
    return [variable, error]

# 在一个iOS代码统计文件中找到所有统计相关的值，包括key，action等
def generate_ios_keys(path):
    global RE_KEY_IOS
    all_items = {}

    f = file(path)
    note = ""
    pattern = re.compile(RE_KEY_IOS)
    index = 0
    for line in f:
        index = index + 1
        # if index > 20:
        #     return
        line = line.strip().strip('\n')
        len_line = len(line)
        if len_line == 0:
            continue
        note_prefix = "///"
        if line.startswith(note_prefix):
            note = line[len(note_prefix) : len_line]
            # print "note: %s" % (note)
            continue
        if line.startswith('NSString') == False:
            continue
        find_ios_key_result = find_ios_key_with_line(line)
        result = find_ios_key_result[0]
        error = find_ios_key_result[1]
        if len(result) == 0:
            hh_print.print_error(index, error)
            continue
        key_action_str = ' '.join(result[:2])
        # 处理%@类型的统计
        key_action_str = key_action_str.replace("%@", "%")
        all_items[key_action_str] = [result[0].strip(), result[1].strip(), note.strip()]
        note = ""
    return all_items

# 在一个iOS代码统计文件中找到所有统计的变量值
def generate_ios_variables(path):
    f = file(path)
    index = 0
    all_keys = []
    all_variables = []

    for line in f:
        index = index + 1
        # if index > 20:
        #     return
        line = line.strip().strip('\n')
        len_line = len(line)
        # print "line: %s" % (line)
        if len_line == 0:
            continue
        code_prefix = "NSString"
        if line.startswith(code_prefix) == False:
            # print "note: %s" % (note)
            continue
        key_result = find_ios_key_with_line(line)
        if len(key_result[0]) == 0:
            hh_print.print_error(index, key_result[1])
            continue
        if all_keys.count(key_result[0]) != 0:
            hh_print.print_error(index, ("%s, key值重复了" % line))
            continue
        variable_result = find_ios_variable(line)
        if len(variable_result[0]) == 0:
            hh_print.print_error(index, variable_result[1])
            continue
        # print "success: key:%s, variable:%s" % (key_result[0], variable_result[0])
        all_keys.append(key_result[0])
        all_variables.append(variable_result[0])
    return all_variables

# 从一行字符串中找到统计的key，action等
def find_java_key_with_line(line):
    global RE_KEY_ANDROID
    match = RE_KEY_ANDROID.search(line)
    result = []
    error = ""
    if match:
        key_str = match.group()
        key_str = key_str[1:(len(key_str) - 1)]

        if len(key_str) > 0:
            # find action
            property_name = line.split()[1]
            property_name_arr = property_name.split("_")
            action = property_name_arr[-1].lower()
            if check_action(action) == False:
                error = "android (%s) 统计action有问题，必须是click等" % (line)
            else:
                result = key_str.split(' ')
                result.insert(1, action)
    if len(result) == 0:
        error = "android (%s) 未能解析出值" % (line)
    return [result, error]

# 从一个Android统计代码中，找到所有统计相关值，包括key，action等
def generate_java_keys(path):
    global RE_KEY_ANDROID
    all_items = {}

    f = file(path)
    note = ""
    pattern = re.compile(RE_KEY_ANDROID)
    index = 0
    for line in f:
        index = index + 1
        # if index > 30:
        #     return
        line = line.strip().strip('\n')
        len_line = len(line)
        if len_line == 0:
            continue
        note_prefix = "//"
        if line.startswith(note_prefix):
            note = line[len(note_prefix) : len_line].strip()
            # print "note: %s" % (note)
            continue
        if line.startswith('String') == False or len(note) == 0:
            continue
        find_java_key_result = find_java_key_with_line(line)
        error = find_java_key_result[1]
        if len(error) > 0:
            hh_print.print_error(index, error)
            continue
        result = find_java_key_result[0]
        key_str = ' '.join(result[:2])
        # 处理%s类型的统计
        key_str = key_str.replace("%s", "%")
        all_items[key_str] = [result[0], result[1], note]
        note = ""
        if check_action(result[0]) == True:
            print line
            hh_print.print_array(result)
    return all_items
