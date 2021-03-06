# coding:utf-8

'''
@author = super_fazai
@File    : my_client.py
@connect : superonesfazai@gmail.com
'''

"""
测试server端的接口签名
"""

import sys
sys.path.append('..')

import hashlib
from base64 import b64encode
from requests import get
from pprint import pprint

from fzutils.common_utils import json_2_dict
from fzutils.time_utils import *

class RequestClient(object):
    """ 接口签名client示例 """
    def __init__(self):
        self._version = "v1"
        self._access_key_id = "yiuxiu"
        self._access_key_secret = "22879be192793e9d80289b58a451f857"
        self.md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
        self.get_current_timestamp = lambda: datetime_to_timestamp(get_shanghai_time())

    def _sign(self, parameters:dict) -> str:
        '''
        签名
        :param parameters: url请求参数(包含除signature外的公共参数)
        :return:
        '''
        if "sign" in parameters:
            parameters.pop("sign")

        # NO.1 参数排序(正序)
        _my_sorted = sorted(parameters.items(), key=lambda parameters: parameters[0])

        # NO.2 排序后拼接字符串
        canonicalized_query_string = ''
        for (k, v) in _my_sorted:
            canonicalized_query_string += '{}={}&'.format(k, v)

        # eg: access_key_id=yiuxiu&goods_link=aHR0cHM6Ly9oNS5tLnRhb2Jhby5jb20vYXdwL2NvcmUvZGV0YWlsLmh0bT9pZD01NTEwNDc0NTQxOTg=&t=1536802300&v=v1&22879be192793e9d80289b58a451f857
        canonicalized_query_string += self._access_key_secret

        # NO.3 加密返回签名: sign(小写, md5加密)
        return self.md5(canonicalized_query_string.encode('utf-8')).lower()

    def _request(self) -> str:
        '''
        测试用例
        :return:
        '''
        # NOTICE:
        # goods_link = 'https://h5.m.taobao.com/awp/core/detail.htm?id=551047454198&umpChannel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&u_channel=libra-A9F9140EBD8F9031B980FBDD4B9038F4&spm=a2141.8147851.1.1'
        # 由于: link中不能带&否则会被编码在sign中加密, 因此先进行b64encode格式化再decode

        # tb
        # goods_link = 'https://item.taobao.com/item.htm?spm=a219r.lmn002.14.1.3b7e12d56SCJjf&id=575507061506&ns=1&abbucket=16'
        # tm
        # goods_link = 'https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-16816054130.101.3e6227dfLIwIrR&id=555709593338&rn=2563b85d76e776e4dd26a13103df62bd&abbucket=6'
        # jd
        # goods_link = 'https://item.m.jd.com/ware/view.action?wareId=3713001'
        # goods_link = 'https://item.jd.com/5025518.html'

        # article_link = 'https://www.toutiao.com/a6623270159790375438/'
        # article_link = 'https://www.jianshu.com/p/1a60bdc3098b'
        # article_link = 'https://post.mp.qq.com/kan/article/2184322959-232584629.html?_wv=2147483777&sig=24532a42429f095b9487a2754e6c6f95&article_id=232584629&time=1542933534&_pflag=1&x5PreFetch=1&web_ch_id=0&s_id=gnelfa_3uh3g5&share_source=0'
        # article_link = 'https://mp.weixin.qq.com/s?src=11&timestamp=1557111601&ver=1589&signature=ALBo1FMtv3X*yJa8CzViSYK*FV-Cr7rHblhsr-96NCZDD5jK8ra2daIg2QWCSVnnqJ4H4KJG*n820P0PULQ6PIQblWXUf*7R69P8ObOCR7UJmpRlKU8s2FgRFiUMrR7N&new=1'
        # 搜狗头条
        # article_link = 'https://sa.sogou.com/sgsearch/sgs_tc_news.php?req=xtgTQEURkeIQnw4p57aSHd9gihe6nAvIBk6JzKMSwdJ_9aBUCJivLpPO9-B-sc3i&user_type=wappage'
        # article_link = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=sf_307868465556099072&vl=http%3A%2F%2Fsofa.resource.shida.sogoucdn.com%2F114ecd2b-b876-46a1-a817-e3af5a4728ca2_1_0.mp4'
        # article_link = 'http://sa.sogou.com/sgsearch/sgs_video.php?mat=11&docid=286635193e7a63a24629a1956b3dde76&vl=http%3A%2F%2Fresource.yaokan.sogoucdn.com%2Fvideodown%2F4506%2F557%2Fd55cd7caceb1e60a11c8d3fff71f3c45.mp4'
        # 东方头条
        # article_link = 'https://mini.eastday.com/mobile/190505214138491.html?qid=null&idx=1&recommendtype=crb_a579c9a168dd382c_1_1_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
        # article_link = 'https://mini.eastday.com/video/vgaoxiao/20190506/190506045241686142077.html?qid=null&idx=6&recommendtype=-1_a579c9a168dd382c_1_6_0_&ishot=1&fr=toutiao&pgnum=1&suptop=0'
        # 百度m站
        # article_link = 'https://mbd.baidu.com/newspage/data/landingpage?s_type=news&dsp=wise&context=%7B%22nid%22%3A%22news_9512351987809643964%22%7D&pageType=1&n_type=1&p_from=-1'
        # bd好看视频
        # article_link = 'https://m.baidu.com/#iact=wiseindex%2Ftabs%2Fnews%2Factivity%2Fnewsdetail%3D%257B%2522linkData%2522%253A%257B%2522name%2522%253A%2522iframe%252Fmib-iframe%2522%252C%2522id%2522%253A%2522feed%2522%252C%2522index%2522%253A0%252C%2522url%2522%253A%2522https%253A%252F%252Fhaokan.baidu.com%252Fvideoui%252Fpage%252Fsearchresult%253Fpd%253Dwise%2526vid%253D8197562812859491736%2526innerIframe%253D1%2522%252C%2522isThird%2522%253Afalse%252C%2522title%2522%253Anull%257D%257D'
        # 推荐栏上边点击视频进入的tab, 所得的到视频地址
        article_link = 'https://sv.baidu.com/videoui/page/videoland?context=%7B%22nid%22%3A%22sv_7865563634675285012%22%7D&pd=feedtab_h5&pagepdSid='

        now_timestamp = self.get_current_timestamp() - 5
        print('请求时间戳为: {}[{}]'.format(now_timestamp, str(timestamp_to_regulartime(now_timestamp))))
        params = {
            'access_key_id': self._access_key_id,
            'v': self._version,
            't': now_timestamp,                                                         # 10位
            # 'goods_link': b64encode(s=goods_link.encode('utf-8')).decode('utf-8'),  # 传str, 不传byte, pc地址或m地址都可, server会识别
            'article_link': b64encode(s=article_link.encode('utf-8')).decode('utf-8'),
        }
        params.update({
            'sign': self._sign(params)
        })

        # url = 'http://127.0.0.1:5000/api/goods'

        # rpc 远程过程调用
        # 淘宝天猫调这个
        # url = 'http://spider.taobao_tmall.k85u.com/api/goods'
        # 京东调这个
        # url = 'http://spider.other.k85u.com/api/goods'

        # article
        # url = 'http://127.0.0.1:5000/api/article'
        url = 'http://118.31.39.97/api/article'
        # url = 'http://23.239.0.250/api/article'

        with get(url, params=params) as response:
            res = response.text
            # print(res)
            data = json_2_dict(
                json_str=res,
                default_res={})
            pprint(data)

            # article
            # print(data.get('data', {}).get('div_body', ''))

        return res

    def __call__(self, *args, **kwargs):
        return self._request()

print(RequestClient()())
