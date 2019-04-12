import csv
import random
import time
import requests
from lxml import etree
import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s')

import Headers
import threading


def job51(url, writer, writer2):
    logging.error("请求url：{}".format(url))
    rlt = requests.get(url)
    # print(rlt.text)
    # 创建对象 html为网页代码
    selector = etree.HTML(rlt.text)
    # 职位名
    job_title = selector.xpath("//h1")[0].text.strip()
    # 薪水
    salary = selector.xpath('//h1/following-sibling::strong')[0].text

    info_list = selector.xpath("//p[@class='msg ltype']/text()")
    # 岗位地点
    address = info_list[0].strip()
    # 工作经验
    work_experience = info_list[1].strip()
    #  学历要求
    education = info_list[2].strip()
    # 发布日期
    start_data = info_list[-1].strip()

    # print(address, work_experience, education, start_data)
    # 福利待遇
    welfare = selector.xpath("//div[@class='t1']//span/text()")
    # 公司名
    try:
        company = selector.xpath("//div[@class='tBorderTop_box']//a[@class='com_name ']/p")[0].text.strip()
    except Exception:
        company = selector.xpath('//p[@class="cname"]/a/@title')[0].strip()
    # 公司性质
    company_nature = selector.xpath("//div[@class='com_tag']//p[@class='at'][1]/text()")[0].strip()
    try:
        # 公司人数
        people_num = selector.xpath("//div[@class='com_tag']//p[@class='at'][2]/text()")[0].strip()
        # 公司类型
        company_cage = selector.xpath("//div[@class='com_tag']//p[@class='at'][3]/@title")[0].strip()
    except Exception:
        people_num = 0
        company_cage = "无"
    # 要求和职责
    requirements = selector.xpath("//div[@class='bmsg job_msg inbox']/p/text()")
    if len(requirements) <= 5:
        requirements = selector.xpath("//div[@class='bmsg job_msg inbox']/text()")
        # print("第二种")
        # print(requirements)
        # print(type(requirements))
        # print(url)
        # print("-----")
    if len(requirements)<=5:
        requirements = selector.xpath("//div[@class='bmsg job_msg inbox']//p//span/text()")
        # print("第三种")
    print(requirements)
        # print(url)
        # print("-----")
    s = ""
    for _ in requirements:
        s += _ + "\t"
    if not s or len(s) < 10:
        pass
    else:
        writer.writerow([job_title, salary, address, start_data, work_experience, education,
                          company, company_nature, people_num, company_cage, welfare, s, url])
        writer2.writerow([job_title, salary, address, start_data, work_experience, education,
                      company, company_nature, people_num, company_cage, welfare, s, url])


def get_url(job, page, data=0):
    """
    :param job: 搜索的岗位
    :param page: 页数
    :param data: 0 24小时  1 近三天  2 近一周 3 近一月 4 其他 9所有
    :return:
    """
    url = "https://search.51job.com/list/000000,000000,0000,00,{},99,{},2,{}.html?".format(data, job, page)
    headers = random.choice(Headers.USER_AGENTS)
    headers = {"User-Agent": headers}
    rlt = requests.get(url, headers=headers)
    selector = etree.HTML(rlt.text)
    url_list = selector.xpath("//div[@class='el']/p//a/@href")

    return url_list


def read_url():
    return open("51job_url.txt", 'r').readlines()

def run():
    logging.error("爬虫开启。。。")
    csvfile = open("前程无忧.csv", "w", encoding="utf_8_sig")
    writer = csv.writer(csvfile)
    writer.writerow(
        ["岗位名称", "岗位薪资", "工作地点", "发布日期", "工作经验", '学历要求', '公司名', "公司性质", '公司人数', '公司类型', '福利', '岗位要求', "职位链接"])

    csvfile2 = open("51job.csv", "w", encoding="utf_8_sig")
    writer2 = csv.writer(csvfile2)
    writer2.writerow(["title", "salary", "address", "data", "work_experience", 'education', 'company', 'company_nature',
                      'company_cage', 'people_num', 'welfare', 'requirements','url'])

    # url = 'https://jobs.51job.com/wuhan-dhxjs/112437255.html?s=01&t=0'
    url_list = read_url()
    for url in url_list:
        if url.split(".")[0] == "https://jobs":
            threading.Thread(target=job51, kwargs={"url":url.strip(),"writer":writer, "writer2":writer2}).start()
            time.sleep(0.1)
            # job51(url.strip(), writer, writer2)


def UrlRun():
    url_list = []
    with open("51job_url.txt", "w") as f:
        for i in range(1, 100):
            time.sleep(0.2)
            url_list = get_url("大数据工程师", 1, 0)
            for url in url_list:
                f.write(url)
                f.write("\n")

if __name__ == '__main__':

   run()