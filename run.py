"""   
@Author:LZL  
@Time:2020/6/10 15:08       
"""  

import logging
import time
import pytest
import os
import allure
from common.com_log import ComLog
from common.com_config import ComConfig
from common.com_shell import ComShell
from allure_commons.types import LinkType
from common.sendmail import send_mail
from common.getreport import new_report
class Run:

    def __init__(self):
        ComLog().use_log()
        # 报告文件文件夹，防止生成的报告内容叠加
        self.time = time.strftime('%m-%d-%H-%M', time.localtime())
        self.report_path = ComConfig().get_report_path()

    def run_case(self):
        # 执行测试
        args = ["-s","./testecase/case/test_test.py", "--alluredir", self.report_path[0]]
        pytest.main(args)
        # 生成测试报告
        #cmd = "allure generate --clean self.report_path[0] -o self.report_path[1]"
        cmd ="allure generate --clean "+self.report_path[0]+" -o "+self.report_path[1]
        print(cmd)
        ComShell().invoke(cmd)

        #send_mail()#发送邮件

if __name__ == '__main__':
    Run().run_case()

