
# coding=gbk
import re, string
import os
import glob



def deal_dir(path):
    #global name, data_file
    print(path)
    filefilter = path+"\*.TXT"
    index = 0
    for i in glob.glob(filefilter):
        index = index + 1
        name = i[-10:-4]
        print(name)
        if index >= 103:
            break
        data_file = i

if __name__ == '__main__':
    deal_dir(r"D:\ts\PycharmProjects\pyT\data")
