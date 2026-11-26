# -*-coding:utf-8-*-

import argparse

# 命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument("-file")  # 输入文件
parser.add_argument("-o", "--output")  # 输出文件
parser.add_argument("--width", type=int, default=50)  # 输出字符画宽
parser.add_argument("--height", type=int, default=30)  # 输出字符画高

# 获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

print("IMG is %s" % (IMG))
print("WIDTH is %d" % (WIDTH))
print("HEIGHT is %d" % (HEIGHT))
print("OUTPUT is %s" % (OUTPUT))
