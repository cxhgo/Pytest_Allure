"""   
@Author:LZL  
@Time:2020/6/2 09:27
"""
import logging

import yaml
from common.com_log import ComLog
from pathlib import Path


"""
封装操作yaml的read
"""

class ComYaml:

    ComLog().use_log()
    # 声明静态方法__read_yaml，静态方法无需实例化,也可以实例化后调用,类或实例均可调用,比如ComYaml.__read_yaml()或者ComYaml().__read_yaml()
    @staticmethod
    def __read_yaml(yaml_path):
        """
        读取yaml文件
        :param yaml_path: yaml文件路径
        :return: {}
        """

        try:
            file = open(yaml_path, 'r', encoding="utf-8").read()
            #print(file)
            dict_data = yaml.load(file,Loader=yaml.FullLoader)# 默认加载全部yaml
            #print(dict_data)
            return dict_data
        except Exception as es:
            logging.error('读取{yaml_path}文件出错，错误是{es}')
            raise ('读取{yaml_path}文件出错，错误是{es}')

    def read_yaml(self, yml_path):
        """
        遍历文件夹下的所有yaml文件，拆分其中的dec和parameters，并设置为字典的键值对，返回字典
        :param yml_path: yaml文件路径 或 yaml文件路径
        :return: {dec1:parameters1, dec2:parameters2}
        """
        values_dict = {}

        # 判断路径是否是文件夹、获取该文件夹下所有的yml文件、并遍历
        try:
            # 判断是否是目录
            if Path(yml_path).is_dir():

                # 获取路径下所有yaml的目录并每个目录都转化为列表
                for file in [x for x in list(Path(yml_path).glob("**/*.yaml"))]:
                    data_dict = self.__read_yaml(file)
                    #print(data_dict)
                    # items()获取读取的yaml文件中的字典键值对，以列表形式返回
                    for test_name, parameters in data_dict.items():
                        values_dict[test_name] = parameters
            # 判断是否以yaml结尾
            elif str(yml_path).endswith(".yaml"):
                file = yml_path  # 为了log服务才这样赋值的
                #print(file)
                data_dict = self.__read_yaml(file)
                #print(data_dict)
                for test_name, parameters in data_dict.items():
                    values_dict[test_name] = parameters
                    #print(values_dict)
        except Exception as es:
            logging.error("解析{file}文件内容出错，错误是{es}")
            raise Exception
        return values_dict






