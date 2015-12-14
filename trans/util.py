# -*- coding: utf-8 -*-
__author__ = 'idbord'

import re
import subprocess
from functools import wraps

# 检查网络状况
def network_check(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            url = 'www.baidu.com'
            p = subprocess.Popen(["ping -c 1 -w 1 " + url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out = p.stdout.read()
            p.terminate()
            regex = re.compile('100% packet loss')
            if len(regex.findall(out.decode('utf-8'))) == 0:
                return func(*args, **kwargs)
            else:
                print ("network is broken! Please check the network!")
                exit(0)
        except Exception as e:
            print (e)
            print ('network is broken! Please check the network!')
            exit(0)
    return wrapped
