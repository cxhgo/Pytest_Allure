"""   
@Author:LZL  
@Time:2020/6/9 17:40       
"""
import subprocess

"""
执行shell语句的封装
"""

class ComShell:

    def invoke(self, cmd):
        # 在linux环境下，使用shell命令，subprocess.PIPE是创建一个新的管道，使用communicate()，返回标准输出和标准出错，避免如果子进程输出了大量数据到stdout或者stderr的管道，并达到了系统pipe的缓存大小的话，子进程会等待父进程读取管道，而父进程此时正wait着的话，将会产生传说中的死锁
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        #o = output.decode("utf-8")# 解码
        o = output# 解码
        return o
