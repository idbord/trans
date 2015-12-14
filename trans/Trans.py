# -*- coding: utf-8 -*-
__author__ = 'idbord'
import sys
import imp
imp.reload(sys)
if sys.version[0:1] == '2':
    sys.setdefaultencoding('utf8')
import locale
import urllib
import json
import re
import requests

from trans.util import network_check

class Trans:
    def __init__(self, word):
        self.word = word
        self.lang = locale.getdefaultlocale()[0]
        self.py_version = sys.version[0:1]

    # 根据输入的query字段判断from,从而匹配to
    def get_trans_from(self):
        word = self.word
        zh_ptr = re.compile(u'[\u4e00-\u9fa5]+')
        try:
            # 匹配到数字时,直接按中文翻译到英文
            match = re.search('[0-9]+', word)

            if match is None:
                # 没有匹配到数字时,进行中文匹配
                match = zh_ptr.search(unicode(word) if self.py_version == '2' else word)
        except Exception as e:
            # 如果没有匹配到中文,则按英文翻译到中文
            match = False
        if match:
            return 'zh'
        return 'en'

    # 获取全部翻译结果,转换为json格式
    @network_check
    def get_trans_content(self, url):
        try:
            switch_dict = {'en': 'zh', 'zh': 'en'}
            trans_from = self.get_trans_from()
            trans_to = switch_dict[trans_from]
            body = {
                'from': trans_from,
                'to': trans_to,
                'query': self.word,
            }
            body = urllib.urlencode(body) if self.py_version == '2' else urllib.parse.urlencode(body)
            url += '?' + body
            result = requests.get(url)
            content = json.loads(result.content if self.py_version == '2' else result.content.decode('ascii'))
            return content
        except Exception as e:
            exit(0)

    def solve_baike(self, dict_result, trans_text):
        # 处理百科内容
        temp = '\033[33m{} >>>\033[0m\n'
        trans_text += temp.format('Baidu Baike') if self.lang == 'en_US' else temp.format('百度百科')
        try:
            baike_means = dict_result['baike_means']
            link = baike_means['link']
            trans_text += '\t' + link + '\n'
        except Exception as e:
            trans_text += '\tno Baike content\n' if self.lang == 'en_US' else '\t没有百科内容\n'
        finally:
            return trans_text

    def parse_content(self, content):
        trans_result = content['trans_result']
        trans_from = trans_result['from']

        simple_data = trans_result['data'][0]
        src = simple_data['src']
        dst = simple_data['dst']

        # 处理公共接口部分
        dict_result = content['dict_result']

        output = '+'*50 + '\n'
        trans_text = '\033[31;01m' + src + '\033[0m'

        # 判断系统语言
        if self.lang == 'en_US':
            # 通过src和dst相同,判断没有该词的翻译,返回信息
            if src == dst:
                trans_text += u'\n\t\033[33mWARNNING:\033[0m No translation for <{}>! Please check your input!\n'.format(trans_text)
                return self.solve_output(output, trans_text)

            # 检查是否有simple_means,没有则返回simple_data的数据
            try:
                simple_means = dict_result['simple_means']
            except Exception as e:
                trans_text += '\n\033[33mSimple Result >>>\033[0m\n' + '\t' + dst + '\n'
                trans_text = self.solve_baike(dict_result, trans_text)
                return self.solve_output(output, trans_text)

            if trans_from == 'en':
                simple_trans = simple_means['symbols'][0]
                prefix = '\t'
                trans_text += '\n' + '******* ' + 'us.[' + simple_trans['ph_am'] + ']\n' + prefix + 'uk.[' + simple_trans['ph_en'] + ']\n'
                trans_text += '\033[33mChinese >>>\033[0m\n'
                item = simple_trans['parts']
                for i in item:
                    trans_text += prefix + i['part'] + ' '
                    for j in i['means']:
                        trans_text += j + ' '
                    trans_text += '\n'
                # 处理英英译内容
                try:
                    edict_trans = dict_result['edict']['item']
                    trans_text += '\033[33mEnglish >>>\033[0m\n'
                    for temp in edict_trans:
                        trans_text += prefix + temp['pos'] + '. ' + temp['tr_group'][0]['tr'][0] + '\n'
                except Exception as e:
                    pass

                trans_text = self.solve_baike(dict_result, trans_text)

            elif trans_from == 'zh':
                simple_trans = simple_means['symbols']
                for i in simple_trans:
                    trans_text += '\t[' + i['word_symbol'] + ']\n'
                    trans_text += '\033[33mEnglish >>>\033[0m\n'
                    for j in i['parts']:
                        for k in j['means']:
                            trans_text += '\t' + k['word_mean'] + '\n'
                trans_text = self.solve_baike(dict_result, trans_text)

        if self.lang == 'zh_CN':
            # 通过src和dst相同,判断没有该词的翻译,返回信息
            if src.lower() == dst.lower():
                trans_text += '\n\t\033[33m警告:\033[0m 没有找到 <{}> 的翻译! 请检查你输入的文字!'.format(trans_text)
                return self.solve_output(output, trans_text)

            # 检查是否有simple_means,没有则返回simple_data的数据
            try:
                simple_means = dict_result['simple_means']
            except Exception as e:
                trans_text += '\n\033[33m简单翻译 >>>\033[0m\n' + '\t' + dst + '\n'
                trans_text = self.solve_baike(dict_result, trans_text)
                return self.solve_output(output, trans_text)

            if trans_from == 'en':
                simple_trans = simple_means['symbols'][0]
                prefix = '\t'
                trans_text += '\n' + '******* ' + 'us.[' + simple_trans['ph_am'] + ']\n' + prefix + 'uk.[' + simple_trans['ph_en'] + ']\n'
                trans_text += '\033[33m中文释义 >>>\033[0m\n'
                item = simple_trans['parts']
                for i in item:
                    trans_text += prefix + i['part'] + ' '
                    for j in i['means']:
                        trans_text += j + ' '
                    trans_text += '\n'
                # 处理英英译内容
                try:
                    edict_trans = dict_result['edict']['item']
                    trans_text += '\033[33m英文释义 >>>\033[0m\n'
                    for temp in edict_trans:
                        trans_text += prefix + temp['pos'] + '. ' + temp['tr_group'][0]['tr'][0] + '\n'
                except Exception as e:
                    pass

                trans_text = self.solve_baike(dict_result, trans_text)

            elif trans_from == 'zh':
                simple_trans = simple_means['symbols']
                for i in simple_trans:
                    trans_text += '\t[' + i['word_symbol'] + ']\n'
                    trans_text += '\033[33m英文释义 >>>\033[0m\n'
                    for j in i['parts']:
                        for k in j['means']:
                            trans_text += '\t' + k['word_mean'] + '\n'
                trans_text = self.solve_baike(dict_result, trans_text)

        return self.solve_output(output, trans_text)

    def solve_output(self, output, trans_text):
        output += trans_text
        output += '+'*50 + '\n'
        return output

    def trans(self):
        url = 'http://fanyi.baidu.com/v2transapi'
        content = self.get_trans_content(url)
        output = self.parse_content(content)
        print (output)

def trans_help():
    print ('tsl word')

def run():
    argv = sys.argv
    length = len(argv)
    if length == 1:
        return trans_help()
    query = ''
    for i in range(1, length):
        query += argv[i] + ' '
    Trans(query).trans()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt as e:
        pass
