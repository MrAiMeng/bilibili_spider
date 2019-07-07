import requests
from lxml import etree
import re

class BiLiBiLi_Spider(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

    def parse_url(self,url):
        # 返回的数据类型为bytes类型
        response = requests.get(url,headers=self.headers)
        return response.content

    def cid_ep_id_message(self,content):# 获取响应中包含弹幕的信息
        html = etree.HTML(content)# 将获取的响应转化为html格式，方便xpath取信息
        # 此处url地址下response中含需提取信息，而element中无，注意信息的提取方法
        content_list = html.xpath('//script[contains(text(),"epList")]/text()')
        text = content_list[0]if len(content_list) > 0 else None
        # 先从response中提取文本信息，再利用正则从文本中获取所需要的信息
        cid_list = re.findall(r'"cid":(\d+)',text)# 因文本中cid两端有引号，正则时也要加上
        # 此处不需要进入下一页就可获得弹幕信息，但是要注意url地址如何选
        ep_id_list = re.findall(r'"ep_id":(\d+)', text)# 每一话的url地址后缀在ep_id中
        # group(1)取括号中内容，group（）取匹配到的所有内容
        print(cid_list[0])
        return cid_list

    def dan_mu_message(self,dan_mu_content):
        # 将bytes类型数据转化为element文件
        dan_mu_xml = etree.XML(dan_mu_content)
        # 再用xpath提取element数据
        # 此处要根据xml的内容进行xpath，而不是网页检查时看到的element
        dan_mu_list = dan_mu_xml.xpath("//d/text()")
        print(dan_mu_list)
        return dan_mu_list

    def save_message(self,dan_mu_list):
        file_name = "我的英雄学院弹幕.text"
        with open(file_name,"a",encoding='utf-8') as f:
            for content in dan_mu_list:
                f.write(content)
                f.write('\n')

    def run(self):
        # 1.请求url地址获取响应
        first_url = "https://www.bilibili.com/bangumi/play/ep205865"
        content = self.parse_url(first_url)
        # 2.解析响应，利用xpath获取页面信息
        cid_list = self.cid_ep_id_message(content)
        for cid in cid_list:
            # 3.将提取的cid与默认网址header合并组成xml文件，获取弹幕信息
            dan_mu_url = 'https://comment.bilibili.com/{}.xml'.format(cid)
            dan_mu_content = self.parse_url(dan_mu_url)
            dan_mu_list = self.dan_mu_message(dan_mu_content)
            # 4.保存数据
            self.save_message(dan_mu_list)
if __name__ == '__main__':
    bilibili_spider = BiLiBiLi_Spider()
    bilibili_spider.run()