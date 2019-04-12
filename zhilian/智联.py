import requests
import random
import json
import time
import logging
from selenium import webdriver
import csv

import Headers

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def getUrl(headers, job, page):
    logging.error("开始第{}次爬虫。。。".format(page))
    url = "https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=100&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3"
    url = url.format(page, job)
    print(url)
    rlt = requests.get(url, headers=headers)
    # print(rlt.json())
    # print(type(rlt.json()))
    info_dict = json.loads(rlt.text)
    data = info_dict.get("data").get("results")
    url_list = []
    for i in data:
        url_list.append(i.get("positionURL"))
    # print(type(info_dict))
    logging.error("爬去{}个url".format(len(url_list)))
    with open("zhilian_url.txt", 'a') as f:
        for url in url_list:
            f.write(url + "\n")
    logging.error("写入文件完毕")


def get_info(url, driver:webdriver, writer2, writer):
    logging.error("开始爬数据，url：{}".format(url))
    driver.get(url)
    time.sleep(0.5)
    # 职位名称
    job_title = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/h3').text
    # 工资
    salary = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/span').text
    # 职位关键字 list
    try:
        keyword = driver.find_element_by_xpath('//div[@class="highlights"]/div').text
    except Exception as e:
        keyword = "无"
    # keyword = keyword.split("\n")
    # 地点 省份
    address = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/ul/li[1]/a').text
    # 工作经验要求
    work_experience = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/ul/li[2]').text
    # 学历要求
    education = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/ul/li[3]').text
    # 公司名
    company = driver.find_element_by_xpath('//div[@class="company"]/a[1]').text
    # 要求
    requirements = driver.find_element_by_xpath("//div[@class='describtion']").text
    # 福利
    welfare = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[1]/div[1]/div[1]/div').text
    logging.error("开始写入文件")
    # 写入文件
    writer2.writerows([[job_title.strip(), salary.strip(), address.strip(), keyword.strip(), work_experience.strip(), education.strip(), company.strip(), welfare.strip(), requirements.strip(), url]])
    writer.writerows([[job_title.strip(), salary.strip(), address.strip(), keyword.strip(), work_experience.strip(), education.strip(), company.strip(), welfare.strip(), requirements.strip(), url]])
    logging.error("写入结束")

if __name__ == '__main__':

    csvfile = open("智联.csv", "w", encoding="utf-8")
    writer = csv.writer(csvfile)
    writer.writerow(["岗位名称", "岗位薪资", "工作地点", "岗位关键词", "工作经验", '学历要求', '公司名', '福利', '岗位职责', "职位链接"])

    csvfile2 = open("zhilian.csv", "w", encoding="utf-8")
    writer2 = csv.writer(csvfile2)
    writer2.writerow(["title", "salary", "address", "keyword", "work_experience", 'education', 'company', 'welfare', 'requirements', 'url'])

    url = "https://jobs.zhaopin.com/CC137755791J00234827804.htm"
    driver = webdriver.Chrome()
    with open("zhilian_url.txt", "r") as f:
        url_list = f.readlines()
    # with open("zhilian_url.txt", "w") as f:
    #     for url in url_list:
    #         f.write(url.strip())
    for url in url_list:
#         f.write(url.strip())
        if url != "\n" and url != None and url != "\t":
            get_info(url.strip(), driver, writer, writer2)





    # print(headers)
    # print(type(headers))
    # for i in range(0, 100):
    #     headers = random.choice(Headers.USER_AGENTS)
    #     headers = {"User-Agent": headers}
    #     getUrl(headers, "大数据", i)
    #     time.sleep(0.1)