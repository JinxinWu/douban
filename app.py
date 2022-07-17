from flask import Flask, render_template, request
import sqlite3
import douban
import WordCloud
import feelings

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
    # 获得前端传来的数据
    if request.method == 'POST':
        val = request.form["val"]
    elif request.method == 'GET':
        val = ''
    global name_real    # 声明全局变量给别的函数用
    name_real = val
    if val == '':
        return render_template("search.html", name=val)
    else:
        id = douban.find_ID(val)
        if id != '':
            douban.main(id)
            num = WordCloud.wordcloud()
            if num == 0:   # 找到了相对应的id，但是没有评论
                return render_template("search.html", name='请输入正确的影视剧名称')
            global yes
            yes = feelings.Feelings(val)
            return render_template("index.html", name=name_real, num=num, id=id)
        else:      # 没找到相对应的id
            return render_template("search.html", name='请输入正确的影视剧名称')


@app.route('/index')
def home():
    id = eval(douban.find_ID(name_real))
    num = WordCloud.wordcloud()
    return render_template("index.html", name=name_real, num=num, id=id)


@app.route('/comment')
def comment():
    datalist  = []
    con = sqlite3.connect("comments.db")
    cur = con.cursor()
    sql = "select * from comments"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    # print(datalist)
    return render_template("comment.html",comments=datalist, name=name_real)



@app.route('/rank')
def rank():
    rank = []   # 评分
    num = []    # 每个评分所统计出的电影数量
    rank1 = ['力荐', '推荐', '还行', '较差', '很差', '未评分']
    num1 = [0, 0, 0, 0, 0, 0]
    con = sqlite3.connect("comments.db")
    cur = con.cursor()
    sql = "select rank,count(rank) from comments group by rank"
    data = cur.execute(sql)
    for item in data:
        rank.append(item[0])
        num.append(item[1])
    # print(rank, num)
    for i in range(0, len(rank)):     # 给内容重新排序，形成柱状图
        if rank[i] == '力荐':
            num1[0] = num[i]
        if rank[i] == '推荐':
            num1[1] = num[i]
        if rank[i] == '还行':
            num1[2] = num[i]
        if rank[i] == '较差':
            num1[3] = num[i]
        if rank[i] == '很差':
            num1[4] = num[i]
        if rank[i] == '未评分':
            num1[5] = num[i]


    cur.close()
    con.close()
    return render_template("rank.html", rank=rank1, num=num1, name=name_real)

@app.route('/word')
def word():
    # WordCloud.wordcloud()
    return render_template("word.html", name=name_real)

@app.route('/team')
def team():
    return render_template("team.html", name=name_real, yes=yes)


if __name__ == '__main__':
    app.run()
