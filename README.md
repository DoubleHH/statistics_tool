# statistics_tool
用于做统计代码生成，统计iOS和Android归纳整理的一系列脚本


## 使用前的准备工作

### 脚本使用准备前的工具安装

以下命令需要再Terminal内使用~

1. [安装brew](https://brew.sh/)。brew是mac系统下的包安装工具。安装命令：`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
2. 安装pip。pip也是安装工具，需要用它安装openpyxl。pip安装命令：`sudo easy_install pip`
3. 安装openpyxl。openpyxl是python下的excel处理工具。安装命令: `pip install openpyxl`

### 源文件Excel的格式

查看本文件夹下的Excel文件：`端统计埋点规范1.0.xlsx`

该Excel是PM用来定制他们需要的埋点用的，PM需要根据里面的要求填写完成。

## 使用方法

准备工作完成后，可以使用了。

命令：

~~~
python generate_ios_android_stat_code.py 骑士端统计埋点1.0.0.xlsx -m
~~~

骑士端统计埋点1.0.0.xlsx 是PM编辑好的具体埋点文件。
-m 代表输出mtj需要导入的excel文件（如果项目中用的是mtj）。

最后输出的方式有两种：

1. 直接在Terminal内显示Android及iOS代码
2. 在脚本同级文件夹的output文件夹内有Android和iOS代码文件。并且有mtj需要导入的excel，还有一个用于便利查询代码需要用到的key得excel文件