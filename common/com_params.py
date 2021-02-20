"""   
@Author:LZL  
@Time:2020/6/2 10:46
"""
import json
import logging
import re
from pathlib import PurePath
from jsonpath_rw import parse

from common.com_yml import ComYaml
from common.com_log import ComLog

"""
被ComManage调用，对请求数据进行处理
"""


class ComParams(object):

    def __init__(self):
        ComLog().use_log()

    def yaml_params(self, yml_params_path):
        """
        格式处理yaml测试用例的数据
        :param yml_params_path:
        :return: {"yaml测试用例dec标题_0": url:xx, method:xx, data:xxx, header:xxx, relevance:xxx, variables:[{xx:yy}], variables_data:[xx,xx]}, {},...}
        """
        #print(yml_params_path)
        params_title = list()
        datas = ComYaml().read_yaml(yml_params_path)
        #print(datas)
        param_value = {}
        pytest_values = list()  # 为了提供符合parametrize的数据
        try:
            for data in [x for x in datas.items()]:
                params = {}
                pytest_values = list()  # 为了提供符合parametrize的数据
                # data为元组格式（"XX","XX"）,取第一个为yaml文件中的Collections后面内容
                value = data[1]
                #print(value)
                parameters = value["parameters"]
                #print(parameters)
                i = 0
                # 一个用例文件可能有多个parameter，即多个请求
                for parameter in parameters:
                    i += 1

                    # 标题
                    title = str(parameter["title"])

                    # url
                    url = str(parameter["url"])
                    if url.startswith("http") or url.startswith("https"):
                        param_value["url"] = url
                    else:
                        if not url.startswith("/"):
                            url = "/" + url
                        param_value["url"] = value["host"] + url# 同域名的拼接
                    #print(param_value["url"])
                    # method
                    method = str(parameter["method"])
                    param_value["method"] = method
                    #print(param_value["method"])
                    # data
                    re_data = str(parameter["data"])
                    param_value["data"] = re_data
                    #print(param_value["data"])
                    # header
                    #header = str(parameter["header"])
                    header = data[1]['header']# 头信息很长的情况，用str会超出长度
                    param_value["header"] = header
                    #print(param_value["header"])

                    # validate
                    validate = str(parameter["validate"])
                    #print(validate)
                    param_value["validate"] = validate
                    #print(param_value["validate"])
                    # 非必须：提取依赖数据（前置用例），给其他用例使用的变量
                    if "relevance" in parameter:
                        relevance = str(parameter["relevance"])
                        param_value["relevance"] = relevance
                        #print(param_value["relevance"])

                    # 非必须：依赖数据（后置用例），获取parameter中所有以$开头的字段，给本用例使用的变量
                    variables_data = re.findall("\$[A-za-z0-9]+", str(parameter))# 数组形式返回匹配的字符串，$开头的
                    #print(variables_data)
                    if variables_data:
                        values = []
                        for j in variables_data:
                            values.append(j.split("$")[1])# 取$后面的内容
                        param_value["variables_data"] = values
                        #print(param_value["variables_data"])
                    # 非必须：指定依赖数据的来源用例以及对应的依赖数据变量名
                    if "variables" in parameter:
                        variables = str(parameter["variables"])
                        param_value["variables"] = variables
                        #print(param_value["variables"])
                    # 键值对 name_i:param_value
                    key = data[0] + "_{i}"
                    #print(key)
                    params[key] = param_value
                    #print(params)
                    #print(params[key])

                    # 组成param
                    params_title.append(params)
                    params_title.append(title)
                    #print(params_title)
                    # 以list形式拼接每个用例[[],[],...]
                    pytest_values.append(params_title)

                    # 开辟新的内存地址
                    params_title = list()
                    params = dict()
                    param_value = dict()

                    # 不能使用这个。得到的结果是params_title中params的值为空，因为内存地址相同
                    # params.pop(key)
            #print(pytest_values)
        except Exception as es:
            logging.error("格式处理yaml测试用例的数据报错，报错的数据是：{parameter}，错误信息：{es}")
            #raise ("格式处理yaml测试用例的数据报错，报错的数据是：{parameter}，错误信息：{es}")
        return pytest_values
        # return params_title
        # return params

    def test_params(self, yaml_path, yaml_name):
        """
        获取指定yaml测试文件的数据 （为了配合pytest的pytest.mark.parametrize；对应test_xx.py）
        :param yaml_path: yaml所在文件夹路径
        :param yaml_name: yaml文件名称
        :return:
        """
        try:
            new_params_titles = list()
            if yaml_name.endswith(".yaml"):
                # 判断是否是.yaml结尾的
                file_path = PurePath(yaml_path, yaml_name)# 将字符串拼接
                #print(file_path)
                params_titles = ComParams().yaml_params(file_path)
                #print(params_titles)

                #new_params_titles = list()
                param_title = list()
                new_param = dict()
                # params_titles的显示格式为[[a,b][a,b]]
                for values in params_titles:
                    old_params = values[0]
                    #print(values)
                    #print(values[0])
                    #print(old_params)
                    for key in old_params:
                        new_param = old_params[key]
                        #print(new_param)
                    param_title.append(new_param)
                    param_title.append(values[1])
                    #print(param_title)
                    new_params_titles.append(param_title)
                    #print(new_params_titles)
                    param_title = list()
            #print(new_params_titles)
            return new_params_titles
        except Exception as es:
            logging.error("yaml文件解析出错，路径是：{yaml_path}, 文件名是：{yaml_name}")
            raise ("yaml文件解析出错，路径是：{yaml_path}, 文件名是：{yaml_name}")

    def list_in_dict(self, variables_list, dict):
        """
        判断['key1', 'key2'...]里的所有key，是否都一一对应dict的key
        比如['key1', 'key2'...], {'key1':'value1', 'key2':'value2'}则true
        如果是 {'key1':'value1', 'key2':'value2', 'key3': 'value3'}则false
        :param variables_list:
        :param dict:
        :return:
        """
        try:
            len_variables = len(variables_list)
            for variable in variables_list:
                if len_variables == 1:
                    if variable in dict and len(dict) == 1:
                        return True
                    else:
                        return False
                if variable in dict:
                    new_variables_list = variables_list[1:]
                    dict.pop(variable)# 移除variable项
                    return self.list_in_dict(new_variables_list, dict)
                else:
                    logging.error("依赖数据获取用例中的relevance_data：{dict}中，没有全部对应或存在重复的key：{variables_list}")
                    return False
        except Exception as es:
            logging.error("依赖数据获取用例中的relevance_data：{dict}中，没有全部对应或存在重复的key：{variables_list}")
            raise ("依赖数据获取用例中的relevance_data：{dict}中，没有全部对应或存在重复的的key：{variables_list}")

    def content_to_json(self, response):
        """
        判断响应内容是否是json，将json格式转化为字典
        :param response:响应内容
        :return json_response:响应内容
        """
        try:
            json_response = json.loads(response.content) # 将json格式数据转换为字典
            return json_response
        except Exception as es:
            logging.error("响应文本不是json格式, 响应文本是：{response.text}")
            raise ("响应文本不是json格式, 响应文本是：{response.text}")

    def relevance_value(self, variable_key, variable_data, response):
        """
        根据key，获取response.content的值,，返回[{}, {}]
        :param variable_data:
        :param response:
        :return:
        """
        try:
            variable_dict = dict()
            # 把"content.xx.yy"转成["xx.yy"]再转成"xx.yy"
            #print(variable_data)
            keys = str(variable_data.split("content.")[1:][0])# 切片
            #print(keys)
            json_content = self.content_to_json(response)  # byte转dict
            #print(json_content)
            # jsonpath_rw，根据key（"xx.yy.zz"），返回dict中该key的值
            re_content = [match.value for match in parse(str(keys)).find(json_content)][0]# 查找key对应下的目标内容，获取目标值，目标值有多个时，选第一个
            #print(re_content)
            variable_dict[variable_key] = re_content
            #print(variable_dict)
            return variable_dict# 返回目标键值对
        except Exception as es:
            logging.error("依赖数据提取出错，想要提取的值：{variable_data}, 响应content是{response.content}")
            raise ("依赖数据提取出错，想要提取的值：{variable_data}, 响应content是{response.content}")

    def replace_request(self, request_dict, variables_value):
        """
        把请求信息中的依赖数据参数，替换成对应的依赖数据的值
        :param request_dict:
        :param variables_value:
        :return:
        """

        try:
            # ['data_value', 'code_value']
            #print(request_dict)
            variable_keys = [
                str(key).split("$")[1]
                for key in re.findall("\$[A-za-z0-9]+", str(request_dict))]# 本用例使用变量

            print(variable_keys)
            print( variables_value)
            i = 0
            for variable_dict in variables_value:
                variable_key = variable_keys[i]
                #print(variable_key)
                if variable_key in variable_dict:
                    # print(F"un_request_dict:{request_dict}")
                    request_dict = str(request_dict).replace("$"+variable_key, str(variable_dict[variable_key]))# 替换变量
                    #print(request_dict)
                    #print(variable_dict[variable_key])
                i += 1
            try:
                request_dict = eval(request_dict)# 执行字符串，返回字符串
            except Exception as es:
                logging.error("依赖数据替换后的请求信息无法转成dict，请求信息：{request_dict}")
                raise ("依赖数据替换后的请求信息无法转成dict，请求信息：{request_dict}")
            return request_dict
        except Exception as es:
            logging.error("请求信息中的依赖数据替换失败，只能提取content.的数据，并且依赖数据的值不能是字典类型，依赖数据是：{variables_value}，"
                          "\n请求数据是：{request_dict}")
            raise ("请求信息中的依赖数据替换失败，只能提取content.的数据，并且依赖数据的值不能是字典类型，依赖数据是：{variables_value}，"
                   "\n请求数据是：{request_dict}")
