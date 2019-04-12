import requests
from lxml import etree
url = "https://jobs.51job.com/shenzhen-lhxq/100262409.html?s=01&t=0"

rlt = requests.get(url)
selector = etree.HTML(rlt.text)
r = selector.xpath("//div[@class='bmsg job_msg inbox']/p/text()")
print(r)
print(len(r))
r2 = selector.xpath("//div[@class='bmsg job_msg inbox']/text()")
print(r2)
r3 = selector.xpath("//div[@class='bmsg job_msg inbox']//p//span/text()")
print(r3)