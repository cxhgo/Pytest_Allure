"""
@Author:LZL
@Time:2020/6/10 14:28
"""

import allure
import pytest
import time
from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_log import ComLog
from common.com_manage import ComManage
from allure_commons.types import LinkType
@allure.parent_suite('父节点testcase/case')
@allure.suite('测试套test_test.py')
@allure.sub_suite('子测试套:类Testtest')
@allure.epic("接口测试")# 定义项目、当有多个项目是使用。往下是feature
@allure.feature("test接口")
@allure.story("听芝部分接口")# 用例按照模块区分，有多个模块时给每个起名字，功能点的描述
class Testtest:
    ComLog().use_log()
    yaml_path = ComConfig().test_params_path()
    #获取指定测试用例的用例信息
    test_params = ComParams().test_params(yaml_path, yaml_name="testone.yaml")
    url ='http://localhost:63342/API_Pytest-master/report/'+time.strftime("%m-%d-%H")+'/html/index.html'
    #test_param = ComParams().test_params(yaml_path, yaml_name="testone.yaml")
    #testparam = test_params + test_param
    #print(test_params[0][1])


    @allure.title("{title}")# 测试用例名称
    @allure.severity(allure.severity_level.CRITICAL)
   # @allure.link("http://localhost:63342/API_Pytest-master/report/12-14-11/html/index.html", link_type=LinkType.LINK, name="baidu")
    @allure.link(url, link_type=LinkType.LINK, name="baidu")
    @allure.issue(url,  name="issue")
    @allure.testcase(url,  name="testcase")
    #@allure.description("测试用例")
   # @allure.attach.file('F:/工作/自动化/API_Pytest_Allure/report/12-18-19/html/html/index.html', attachment_type=allure.attachment_type.HTML)
    @pytest.mark.parametrize("param, title", test_params)# 测试用例参数化：参数名，列表数据

    def test_example(self, param, title):
        allure.dynamic.description(title)
        result = ComManage().assert_manner(param)
        assert result

if __name__ == '__main__':
    # -s：显示程序中的print/logging输出
    pytest.main(["-s", "test_test.py","-q","--alluredir","API_Pytest_Allure/report"])
