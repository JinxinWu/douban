# 导入工具包
import requests
from bs4 import BeautifulSoup
import random
import time
import xlwt
import os
import sqlite3
import pandas as pd
import numpy as np
import urllib
import re

# 请求头
head = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
]
headers = {
    # 'Cookie': 'bid=90wm4A_Shis; __utmc=30149280; __utmc=223695111; ll="118172"; __gads=ID=bef10c51f52b7e32-225206732cd50067:T=1657612227:RT=1657612227:S=ALNI_MZ45WFX8jxxMjhRzkgMxp9_MncQhA; __gpi=UID=0000079c99943bb7:T=1657612227:RT=1657612227:S=ALNI_MYUsgphyNd61itSu5-5cP4UeLa8Ug; _vwo_uuid_v2=D037CF37D4A864556206273F5BCBDD191|630efaf3ba53bb43d0b2bfdac0d93f59; dbcl2="259315007:qzHzrzgOJ6w"; ck=AhlI; __utmz=30149280.1657682222.5.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1657682222.5.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.4cf6=["","",1657725109,"https://accounts.douban.com/"]; _pk_id.100001.4cf6=0c21d9bc10293477.1657611212.6.1657725109.1657684337.; _pk_ses.100001.4cf6=*; __utma=30149280.815997105.1657611212.1657682222.1657725109.6; __utmb=30149280.0.10.1657725109; __utma=223695111.1970637892.1657611212.1657682222.1657725109.6; __utmb=223695111.0.10.1657725109; ap_v=0,6.0',
    'User-Agent': random.choice(head),
    # 'Referer': 'https://movie.douban.com/subject/34841067/comments?start=',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9'
}
# =============================================================================

def main(id):
    url = ['https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=new_score'.format(id, i) for i in range(0, 200, 20)]
    # 获得数据 []内为0则获得两列数据，1则获得所有数据
    datalist = getData(url)[1]

    # 数据保存到excel中
    # savepath = "豆瓣电影评论.xls"
    # saveData2(datalist, savepath)

    # 数据保存到SQLite数据库中
    dbpath = "comments.db"
    saveDataDB(datalist, dbpath)

def getData(url):
    lis1 = []
    lis2 = []

    for urli in url:
        # 获取信息
        html = requests.get(urli, headers=headers)
        # 获取内容
        data = html.text
        soup = BeautifulSoup(data, 'lxml')
        # 用户
        names = soup.select('#comments > div > div.comment > h3 > span.comment-info > a')
        # 评级
        grades = soup.select('#comments > div > div.comment > h3 > span.comment-info')
        # 日期
        dates = soup.select('#comments > div > div.comment > h3 > span.comment-info > span.comment-time')
        # 内容
        contents = soup.select('#comments > div > div.comment > p > span')

        for name, grade, date, content in zip(names, grades, dates, contents):
            grade_re = grade.find_all('span')
            # 星级评价处理
            if (len(grade_re[1]['class']) > 1):
                xing = grade_re[1]['class'][0] + " " + grade_re[1]['class'][1]
            else:
                xing = grade_re[1]['class'][0]
            # 对部分未进行评价的用户进行处理
            if (len(grade_re[1]['title']) != 2):
                tuijian = '未评分'
            else:
                tuijian = grade_re[1]['title']
            # 评论中的单引号全部换成双引号
            name = name.get_text().replace("'", '"')
            content = content.get_text().replace("'", '"')
            # 对未评论的数据进行处理
            if content == '':
                content = '/'
            # 写入列表中
            lis1.append([grade_re[1]['title'],
                        content])
            lis2.append([name,
                        # grade_re[1]['class'],
                        xing,
                        # grade_re[1]['title'],
                        tuijian,
                        date.get_text().strip(),
                        content])
        print('完成:', urli)
        # time.sleep(np.random.randint(5, 10))

    result1 = pd.DataFrame(lis1, columns=['等级', '内容'])
    result2 = pd.DataFrame(lis2, columns=['用户', '评级', '等级', '日期', '内容'])
    # result1.to_csv('douban_comments.txt', index=False, encoding='UTF-8')
    result2.to_excel('douban_comments.xls', index=False, encoding='UTF-8')
    print("爬取完毕")
    return lis1, lis2

# 保存数据（保存全部爬取数据的excel文件）
def saveData(datalist, savepath):
    print("保存所有数据")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影评论', cell_overwrite_ok=True)  # 创建工作表
    col = ("用户", "评级", "等级", "日期", "内容")
    for i in range(0, 5):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 100):        # 爬取评论的数量
        # print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 5):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存

# 保存数据2（只保存等级和内容的excel文件）
def saveData2(datalist, savepath):
    print("保存等级和内容")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影评论', cell_overwrite_ok=True)  # 创建工作表
    col = ("等级", "内容")
    for i in range(0, 2):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 100):        # 爬取评论的数量
        # print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 2):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存

# 将数据保存到SQLite数据库中
def saveDataDB(datalist, dbpath):
    if not os.path.exists(dbpath):
        init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    # 清空表中原有数据
    sql = '''
            delete from comments
    '''
    cur.execute(sql)
    conn.commit()

    i = 0
    for data in datalist:
        for index in range(len(data)):
            if index != 1:
                data[index] = "'" + str(data[index]) + "'"
            else:
                data[index] = '"' + str(data[index]) + '"'
        sql = '''
                insert into comments(
                user, grade, rank, data, content
                )values(%s)''' % ",".join('%s' %a for a in data)
        i += 1
        print("第{}条评论".format(i))
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("数据已成功写入数据库")

# 初始化SQLite数据库
def init_db(dbpath):
    sql = '''
        create table comments
        (
        user varchar,
        grade varchar,
        rank varchar,
        data varchar,
        content text
        )
    '''
    # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 获取id(不支持泛型搜索)
def find_ID(name):  # name即剧名
    try:
        url1 = 'https://movie.douban.com/j/subject_suggest?q='
        url2 = urllib.parse.quote(name)  # URL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，此时就要进行编码。
        url = url1 + url2  # 生成针对该剧的链接，上面链接红字部分即为编码的name
        html = requests.get(url, headers=headers)  # 访问链接，获取html页面的内容
        html = html.content.decode()  # 对html的内容解码为utf-8格式
        html_list = html.replace('\/', '/')  # 将html中的\/全部转换成/，只是为了看着方便（不换也行）
        html_list = html_list.split('},{')  # 将html页面中的每一个条目提取为列表的一个元素。

        # 定义正则，目的是从html中提取想要的信息（根据title提取id）
        str_title = '"title":"' + name + '"'  # 匹配剧名name
        pattern_title = re.compile(str_title)

        str_id = '"id":"' + '[0-9]*'  # 匹配该剧的id值
        pattern_id = re.compile(str_id)

        # 从html_list中的每个item中提取对应的ID值
        id_list = []  # ID存放列表
        for l in html_list:  # 遍历html_list
            find_results_title = re.findall(pattern_title, l, flags=0)  # 找到匹配该剧name的条目item
            if find_results_title != []:  # 如果有title=name的条目，即如果有匹配的结果
                find_results_id = re.findall(pattern_id, l, flags=0)  # 从该匹配的item中的寻找对应的id之
                id_list.append(find_results_id)  # 将寻找到的id值储存在id_list中

        # 可能匹配到了多个ID（可能是同名不同剧），根据产生的id的数量，使剧名name匹配产生的id，使两个list相匹配
        name_list = [name] * len(id_list)

        # 对id_list的格式进行修整，使之成为标准列表格式
        id_list = str(id_list).replace('[', '').replace(']', '').replace("'", '').replace('"id":"', '').replace(' ', '')
        id_list = id_list.split(',')

    except:  # 如果不能正常运行上述代码（不能访问网页等），输出未成功的剧名name。
        print('ERROR:', name)
    return id_list[0]

def search(name):
    id = eval(find_ID(name))
    print(id)
    main(id)
    return id

if __name__ == '__main__':
    name = input("请输入想要查询的电影名称：")
    search(name)
