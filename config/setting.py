# _*_ coding:utf-8 _*_
import os,sys
#文件路径根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
test=os.path.dirname(__file__)
#sys.path是一个列表，包括有所有查找包的目录，直接启动python使用
sys.path.append(BASE_DIR)
#配置文件
Test_Config = os.path.join(BASE_DIR,"config","config.ini")
#测试用例报告
Test_Report = os.path.join(BASE_DIR,"report")




