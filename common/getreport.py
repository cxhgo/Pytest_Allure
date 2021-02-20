# _*_ coding:utf-8 _*_
import os


def new_report(testreport):
    """
    生成最新的测试报告文件
    :param testreport:报告所在文件夹
    :return:返回文件
    """
    # 返回指定的文件夹包含的文件或文件夹的名字的列表
    lists = os.listdir(testreport)
    """
    sort按key的关键字进行升序排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间，所以最终以文件时间从小到大排序
    最后对lists元素，按文件修改时间大小从小到大排序。
    testreport获取最新文件的绝对路径,lists[-1]列表中最后一个值,组合为文件夹+文件名
    """
    # 兼容linux环境路径格式
    #print(lists)
    lists.sort(key = lambda fn:os.path.getmtime(testreport +"/"+fn))
    #lists.sort(key = lambda fn:os.path.getmtime(testreport +"\\"+fn))
    # 连接testreport和list[-1]的值
    file_new = os.path.join(testreport,lists[-1])
    #print(file_new)
    list_copy =os.listdir(file_new)
    #print(list_copy)
    list_copy.sort(key = lambda fn:os.path.getmtime(file_new +"/"+fn))
    #print(list_copy[-1])
    file_new_suite = os.path.join(file_new,list_copy[-1])
    #print(file_new_suite)
    #return file_new
    list_copys =os.listdir(file_new_suite)
    list_copys.sort(key = lambda fn:os.path.getmtime(file_new_suite +"/"+fn))
    file_new_suites = os.path.join(file_new_suite,list_copys[2])
    print(file_new_suites)
    return file_new_suites
