import collections
import csv
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

#------词云图
def WordcloudImg(mytext:str):
    wc = WordCloud(
        background_color="white", #背景颜色
        max_words=500, #显示最大词数
        font_path="./simsun.ttf",  #使用字体
        min_font_size=10,
        max_font_size=150,
        width=1000,  #图幅宽度
        height=1000,
        )
    wc.generate(mytext)
    wc.to_file("pic.png")


def cut_word():

    f = open('./51job/51job.csv','r', encoding="utf-8")
    f2 = open('./zhilian.csv','r', encoding="utf-8")
    a = csv.reader(f)
    l = [ i[-2].strip() for i in a] # 岗位关键词

    l = l + [i[3] for i in csv.reader(f2)]
    l = l + [i[-2] for i in csv.reader(f2)]

    s = ""
    for i in l:
        s += i.strip()
    word_list = []
    stopwords = read_stopword()

    for i in jieba.cut(s):
        if i not in stopwords and i != "\n" and i != " " and i != "\t":
            if len(i) >= 2:
                word_list.append(i)
    f2.close()
    f.close()
    return word_list


def word_count(word_list):
    # 词频统计
    word_counts = collections.Counter(word_list) # 对分词做词频统计
    word_counts = word_counts.most_common(200) # 获取前10最高频的词
    print (word_counts) # 输出检查
    return word_counts


def read_stopword():
    with open("stopwords.txt", "r") as f:
        words_list = [ word.strip() for word in f.readlines()]
    return words_list


def write_stopwords(list_words):
    with open("stopwords.txt", "a") as f:
        for word in list_words:
            f.write(word[0])
            f.write("\n")


def Histogram(word_counts,title):
    name_list = []
    num_list = []
    for word in word_counts:
        name_list.append(word[0])
        num_list.append(word[1])
    #
    # x = name_list
    # y = num_list
    # plt.figure(figsize=(20, 8), dpi=100)
    plt.bar(range(len(num_list)), num_list, color='rgb', tick_label=name_list)
    for a, b in zip(range(len(num_list)), num_list):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    plt.title(title)
    plt.show()


def address():
    """
    岗位地区分布柱状图
    :return:
    """
    f = open('./51job/51job.csv','r', encoding="utf-8")
    f2 = open('./zhilian.csv','r', encoding="utf-8")
    a = csv.reader(f)
    l = [_[2] for _ in a]
    l = l + [_[2] for _ in csv.reader(f2)]
    # print(l)
    addres_list = []
    for _ in l[1:]:
        addres_list.append(_.split("-")[0])
    f.close()
    f2.close()
    return addres_list


def salary():
    f = open('./51job/51job.csv','r', encoding="utf-8")
    s = [_[1] for _ in csv.reader(f)]
    s = [float(_.split("-")[0])*10000 for _ in s[1:] if _ ]
    salary_list = []
    print(s)
    # float
    f.close()
    return s


def salary_address():
    f = open('./51job/51job.csv','r', encoding="utf-8")
    # _ = csv.reader(f)
    sa = [(_[2].split("-")[0], _[1]) for _ in csv.reader(f) if _[1]]
    # sa = [ (_[0],float(_[1])*10000) for _ in sa[1:] if "万" in _[1]]
    sa_list = []
    for _ in sa[1:]:
        if _[1]:
            if "万" in _[1]:
                sa_list.append((_[0],float(_[1].split("-")[0])*10000))
            else:
                sa_list.append((_[0],float(_[1].split("-")[0])*1000))

    address_dict = {}
    num_address = {}
    for _ in sa_list:
        if address_dict.get(_[0]):
            salary_total = address_dict.get(_[0])
            address_dict[_[0]] = salary_total + _[1]
            num_address[_[0]] =  num_address[_[0]] + 1
        else:
            address_dict[_[0]] = _[1]
            num_address[_[0]] = 1

    print(num_address)
    for k, v in num_address.items():

        address_dict[k] = round(address_dict.get(k) / v, 2)


    # print(address_dict)
    f.close()
    address_dict = tuple(address_dict.items())
    return address_dict


def exp_salary():
    f = open('./51job/51job.csv','r', encoding="utf-8")
    exp_sa = [( _[4], _[1]) for _ in csv.reader(f)]
    exp_list = []
    for _ in exp_sa[1:]:
        if _[1]:
            if "万" in _[1]:
                exp_list.append((_[0],float(_[1].split("-")[0])*10000))
            else:
                exp_list.append((_[0],float(_[1].split("-")[0])*1000))

    exp_dict = {}
    num_exp = {}
    for _ in exp_list:
        if exp_dict.get(_[0]):
            salary_total = exp_dict.get(_[0])
            exp_dict[_[0]] = salary_total + _[1]
            num_exp[_[0]] = num_exp[_[0]] + 1
        else:
            exp_dict[_[0]] = _[1]
            num_exp[_[0]] = 1

    print(num_exp)
    for k, v in num_exp.items():
        exp_dict[k] = round(exp_dict.get(k) / v, 2)

    print(exp_dict)
    return tuple(exp_dict.items())



def exp():
    f = open('./51job/51job.csv','r', encoding="utf-8")
    exp_sa = [ _[4] for _ in csv.reader(f)]

    # print(exp_sa)

    return tuple(collections.Counter(exp_sa[1:]).items())

if __name__ == '__main__':
    # 地区柱状图------
    # addres_list = address()
    # print(addres_list)
    # word_counts = word_count(addres_list)
    # print(word_counts)
    # Histogram(word_counts, "大数据岗位分布图")

    # 工资
    # salart_list = salary()
    # word_counts = word_count(salart_list)
    # Histogram(word_counts, "工资分布")

    # # 工资地图
    # sa = salary_address()
    # Histogram(sa, "大数据岗位地区分布与平均工资")

    # 工作经验-工资
    # Histogram(exp_salary(), "大数据工作经验与工资对比图")

    # 工作经验-岗位
    # Histogram(exp(), "工作经验与岗位对应关系")


    word_list = cut_word()
    print(word_list)
    word_counts = word_count(word_list)
    # Histogram(word_counts)
    words = ""
    for s in word_counts:
        words += "\t" + s[0]
    WordcloudImg(words)
    # write_stopwords(word_counts)
