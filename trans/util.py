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
            if len(regex.findall(out)) == 0:
                return func(*args, **kwargs)
            else:
                print "network is broken! Please check the network!"
                exit(0)
        except Exception as e:
            print 'network is broken! Please check the network!'
            exit(0)
    return wrapped

# 根据输入的query字段判断from,从而匹配to
def get_trans_from(query):
    zh_ptr = re.compile(u'[\u4e00-\u9fa5]+')
    try:
        # 匹配到数字时,直接按中文翻译到英文
        match = re.search('[0-9]+', query)
        if match is None:
            # 没有匹配到数字时,进行中文匹配
            match = zh_ptr.search(unicode(query))
    except Exception as e:
        # 如果没有匹配到中文,则按英文翻译到中文
        match = False
    if match:
        return 'zh'
    return 'en'
