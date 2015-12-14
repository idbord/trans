# -*- coding: utf-8 -*-
__author__ = 'idbord'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import locale
import urllib
import requests
import json

from util import network_check, get_trans_from

class Trans:
    def __init__(self, word):
        self.word = word
        self.lang = locale.getdefaultlocale()[0]

    # 获取全部翻译结果,转换为json格式
    @network_check
    def get_trans_content(self, url):
        switch_dict = {'en': 'zh', 'zh': 'en'}
        trans_from = get_trans_from(self.word)
        trans_to = switch_dict[trans_from]
        body = {
            'from': trans_from,
            'to': trans_to,
            'query': self.word,
        }
        body = urllib.urlencode(body)
        url += '?' + body
        result = requests.get(url)
        content = json.loads(result.content)
        return content

    def solve_baike(self, dict_result, trans_text):
        # 处理百科内容
        temp = '\033[33m{} >>>\033[0m\n'
        trans_text += temp.format('Baidu Baike') if self.lang == 'en_US' else temp.format('百度百科')
        try:
            baike_means = dict_result['baike_means']
            link = baike_means['link']
            trans_text += '\t' + link + '\n'
        except Exception as e:
            trans_text += 'no Baike content' if self.lang == 'en_US' else '没有百科内容'
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
            if src.lower() == dst.lower():
                trans_text += '\n\t\033[33mWARNNING:\033[0m No translation for <{}>! Please check your input!'.format(trans_text)
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
                edict_trans = dict_result['edict']['item']
                trans_text += '\033[33mEnglish >>>\033[0m\n'

                for temp in edict_trans:
                    trans_text += prefix + temp['pos'] + '. ' + temp['tr_group'][0]['tr'][0] + '\n'

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
                edict_trans = dict_result['edict']['item']
                trans_text += '-'*50 + '\n\033[33m英文释义 >>>\033[0m\n'

                for temp in edict_trans:
                    trans_text += prefix + temp['pos'] + '. ' + temp['tr_group'][0]['tr'][0] + '\n'

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
        print output

def trans_help():
    print 'trans word'

def run():
    argv = sys.argv
    length = len(argv)
    if length == 1:
        return trans_help()
    query = ''
    for i in range(1, length):
        query += argv[i]
    Trans(query).trans()

if __name__ == '__main__':
    run()
