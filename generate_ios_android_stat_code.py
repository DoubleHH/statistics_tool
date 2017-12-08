#coding:utf-8

# 描述：把统计的excel表生成对应的 iOS 及 Android 代码

import os
import time
import glob
from sys import argv
import operator
from optparse import OptionParser

from public_pythons import all_stat_keys_from_code
from public_pythons import hh_excel_tool
from public_pythons import hh_print

GLOBAL_PREFIX = "SF"

# 生成安卓统计代码
def generate_android_one_key_code(key, action, variable_name, note):
    dealed_key = key.replace("%", "%s")
    dealed_note = "/**\n *" + note + "\n */"
    code = "" + dealed_note + "\n" + "public static final String " + variable_name + " = \"" + dealed_key + " " + action + "\";"
    return code

# 生成代码中的key值
def generate_variable_code(key, action):
    global GLOBAL_PREFIX
    name = (GLOBAL_PREFIX + "_" + key.upper().replace('.', '_') + "_" + action.upper())
    name = name.replace("%", "")
    return name

# 生成iOS统计.h代码
def generate_ios_one_key_code_h(variable_name, note):
    code = "/// " + note + "\n" + ("FOUNDATION_EXPORT NSString *const %s;" % (variable_name))
    return code

# 生成iOS统计.m代码
def generate_ios_one_key_code_m(key, action, variable_name, note):
    key = key.replace("%", "%@")
    code = "/// " + note + "\n" + ("NSString *const %s = @\"%s %s\";" % (variable_name, key, action.lower()))
    return code

def string_with_value(value):
    if value == None:
        return ""
    else:
        return value.strip().strip('\n')

def generate_keys_array(ws, already_existed_keys):
    index = 0
    key_wappers = []
    android_code = ""
    ios_code_h = ""
    ios_code_m = ""
    # 当前excel生成的所有的代码key数组
    variable_array = []
    total_new_items = 0
    for row in ws.rows:
        index = index + 1
        row_array = []
        if index < 3:
            continue
        if index == 3:
            row_array.append("CODE_KEYS")
            for value in row:
                value_string = string_with_value(value.value)
                row_array.append(value_string)
            key_wappers.append(row_array)
            continue
        key = string_with_value(row[4].value)
        action = string_with_value(row[5].value)
        excel_note = string_with_value(row[3].value)
        excel_note = excel_note.replace("\n", "; ")
        note = string_with_value(row[1].value) + ", " + excel_note
        # print "key:%s, value:%s, note:%s" % (key, action, note)
        if len(key) == 0:
            if len(excel_note) > 0:
                hh_print.print_error(index, "(%s) key为空" % (key))
            row_array.append("非统计行")
        else:
            if all_stat_keys_from_code.check_action(action) == False:
                print "line:%s, key:%s" % (index, key)
                hh_print.print_error(index, "(%s) 统计action有问题，必须是click等" % (key))
            if len(note) == 0:
                hh_print.print_error(index, "(%s) 注释为空" % (key))
            variable_name = generate_variable_code(key, action)
            append_string = ""
            if variable_array.count(variable_name) == 0:
                key_action = key + " " + action
                if already_existed_keys.count(key_action) != 0:
                    hh_print.print_color_string(variable_name + " [ " + key_action + " ] SAME as in project", "lred")
                else:
                    variable_array.append(variable_name)
                    android_code = android_code + "\n" + generate_android_one_key_code(key, action, variable_name, note)
                    ios_code_h = ios_code_h + "\n" + generate_ios_one_key_code_h(variable_name, note)
                    ios_code_m = ios_code_m + "\n" + generate_ios_one_key_code_m(key, action, variable_name, note)
                    total_new_items = total_new_items + 1
            else:
                hh_print.print_color_string(variable_name + " SAME in excel", "cyan")
            row_array.append(variable_name)

        for value in row:
            if value.value != None:
                row_array.append(value.value.strip().strip('\n'))
            else:
                row_array.append("")
        key_wappers.append(row_array)

    print "\n\nAndroid code:"
    hh_print.print_color_string(android_code, "purple")
    print "\niOS code.h:"
    hh_print.print_color_string(ios_code_h, "red")
    print "\niOS code.m:"
    hh_print.print_color_string(ios_code_m, "brown")
    hh_print.print_color_string("新的统计key共有%s个" % (total_new_items), "lred")
    write_to_file(output_folder() + "android_code.txt", android_code)
    write_to_file(output_folder() + "ios_code.txt", ios_code_h + '\n' + ios_code_m)
    return key_wappers

def output_folder():
    return os.path.dirname(os.path.abspath(__file__)) + '/output/'

def excel_name():
    time_string = time.strftime('%Y%m%d_%H%M_%S', time.localtime(time.time()))
    return output_folder() + ("new_stat_" + time_string)

def config_code_prefix_from_excel(ws):
    global GLOBAL_PREFIX 
    GLOBAL_PREFIX = (ws['D2'].value).strip()

def write_to_file(file_name, text):
    file_object = open(file_name, 'w')
    file_object.write(text)
    file_object.close()

def mtj_name():
    time_string = time.strftime('%Y%m%d_%H%M_%S', time.localtime(time.time()))
    return output_folder() + ("MTJ事件模板_" + time_string)

def create_mtj_file(sheet_array):
    mtj_array = []
    mtj_array.append([u'事件ID', u'事件名称'])
    index = 0
    for item_array in sheet_array:
        index = index + 1
        key = item_array[5]
        if index < 2 or len(key) == 0:
            continue
        key_action = key
        if len(key_action) > 30:
            error = 'Length of ' + key_action + ': ' + str(len(key_action)) + '!! ERROR！大哥，超过30个字符不能插入SB MTJ ！！！';
            hh_print.print_color_string(error, 'lred')
        name = item_array[2] + u"，" + item_array[4]
        mtj_array.append([key_action, name])
    hh_excel_tool.generate_csv(mtj_array, mtj_name())

if __name__ == '__main__':
    # print (os.path.abspath(__file__))
    # print (os.path.dirname(os.path.abspath(__file__)))
    # exit(0)
    parser = OptionParser(usage="python %prog [options] excel_path ios_original_statistics_file")
    parser.add_option("-m", "--mtj",
                    action = "store_true",
                    dest = "mtj",
                    default = False,
                    help = u"生成MTJ事件的文件"
                    )
    (options, args) = parser.parse_args()
    if len(args) < 1:
        print "参数错误：\n参数一：PM填好的标准统计文件，\n参数二：已有的iOS统计代码，用于对PM生成的统计做过滤\n[options]：指定其他功能，用--help或-h来查看"
        print "\nUsage:python %s [options] excel_path ios_original_statistics_file" % (__file__)
        exit(0)
    ws = hh_excel_tool.read_excel_sheet(args[0], 0)
    if ws == None:
        hh_print.print_error(0, "sheet doesn't exist")
        exit(0)
    config_code_prefix_from_excel(ws)
    already_existed_keys = []
    if len(args) > 1:
        already_existed_items = all_stat_keys_from_code.generate_ios_keys(args[1])
        already_existed_keys = already_existed_items.keys()
    array = generate_keys_array(ws, already_existed_keys)
    hh_excel_tool.generate_excel([ ["keys", array], ], excel_name())
    if options.mtj:
        create_mtj_file(array)
