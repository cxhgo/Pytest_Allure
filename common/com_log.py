"""   
@Author:LZL  
@Time:2020/6/1 16:36       
"""
# -*- coding: utf-8 -*-
import time
import logging
# from pathlib import Path, PurePath  # PurePath用于拼接路径
import os

"""
设置日志文件的基本属性
"""


class ComLog:
    func = None# 保存创建的实例

    def __new__(cls, *args, **kwargs):
        # 单例模式：只能被实例化一次，实例变量在第一次实例化时就已经固定
        if not cls.func:
            # 判断是否存在类变量，如果之前已经实例化了，直接返回。如果是第一次实例化，就会为func类变量绑定实例
            cls.func = super().__new__(cls)# _调用父类object.__new__(Comlog)创建实例：__new__是一个静态方法，会返回一个创建的实例，当创建一个新实例时调用__new__
            return cls.func
        return cls.func# 创建实例，没有初始化

    def use_log(self, log_level=logging.INFO):
        # log_path = PurePath(str(Path.r(target=__file__)), "log", str(time.strftime('%m_%d', time.localtime())) + '_error.log')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log",
                                str(time.strftime('%m_%d', time.localtime())) + '_error.log')# 日志文件路径
        #file = open(log_path, encoding="utf-8", mode="a")
        # logging.basicConfig(
        #     filename=log_path,# 指定日志文件名
        #     filemode='a',# 和file函数意义相同，指定日志文件的打开模式，'w'或者'a'
        #     format='%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[日志信息] ==> %(message)s', # 输出的内容格式；单词错误的话，message报错，格式：日志时间 文件名【代码行数】日志级别==>日志信息
        #     datefmt='%Y-%m-%d %H:%M:%S',#指定时间格式
        #     level=log_level # logging中可以选择很多消息级别，如debug、info、warning、error以及critical，默认为logging.WARNNING
        # )
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #file.close()
        # 设置编码
        encode_header = logging.FileHandler(log_path,encoding='utf-8',mode="a")
        stream_handle = logging.StreamHandler()
        encode_header.setFormatter(fmt)
        logger.addHandler(encode_header)
        logger.addHandler(encode_header)
        # 获取logger
        #logging.getLogger(str(log_path)).addHandler(encode_header)
