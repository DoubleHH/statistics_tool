#! /usr/bin/python
# -*- coding:utf-8 -*-

# 有颜色的打印工具

import os
from sys import argv

COLORS  = {
    "blue": "0;34m",
    "green": "0;32m",
    "cyan": "0;36m",
    "red": "0;31m",
    "purple": "0;35m",
    "brown": "0;33m",
    "yellow": "1;33m",
    "lred": "1;31m",
}

def print_color_string(string, color="red"):
    print ("\033[" + COLORS[color])
    print string
    print '\033[0m'

def print_error(index, string):
    error = "Error! \nLine:%d: %s" % (index, string)
    print_color_string(error)

def print_array(array, title="Unknown"):
    print_color_string("print array(%s, count:%d) start:\n" % (title, len(array)), "brown")
    for value in array:
        print value
    print_color_string("print array(%s, count:%d) end:\n" % (title, len(array)), "brown")
