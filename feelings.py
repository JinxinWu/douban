from snownlp import SnowNLP
# from snownlp import sentiment
import pandas as pd
# 导入绘图的库
import matplotlib.pyplot as plt
# 导入将数据导入Excel的库
import xlwt

def Feelings(name):
    # 导入Excel里的样例数据
    aa = 'douban_comments.xls'
    # 读取文本数据
    df = pd.read_excel(aa)
    # 提取所需要评论的所有数据
    df1 = df['内容']
    # print(df1)
    # 遍历每条评论进行预测
    values = [SnowNLP(i).sentiments for i in df1]
    # 输出积极的概率，大于0.5积极的，小于0.5消极的
    # myval保存每一条评论的情感预测值
    myval = []
    # good和bad分别用于统计正面和负面评论的数量，用于计算后面的好评率
    good=0
    bad=0
    for i in values:
        if (i>=0.5):
            myval.append("正面")
            good=good+1
        else:
            myval.append("负面")
            bad=bad+1
    df['预测值']=values
    df['评价类别']=myval
    # 重新创一个叫“douban_comments”将结果输出到Excel
    # df.to_excel('douban_comments.xlsx')
    # 计算好评率
    rate=good/(good+bad)
    print('好评率','%.f%%' % (rate * 100)) # 格式化为百分比
    # 绘制将每一个用户评论进行情感分析的作每一个评论情感预测值的折线图
    y=values
    plt.figure(figsize=(10,6))
    # 确定图的样式
    plt.rc('font', family='SimHei', size=18)
    # 绘制折线图
    plt.plot(y, marker='o', mec='r', mfc='w',label=u'评价分值')
    # X和Y的坐标的小标题
    plt.xlabel('用户')
    plt.ylabel('评价分值')
    # 让图例生效
    plt.legend()
    # 添加总标题
    plt.title(name + '评论情感分析',family='SimHei',size=20,color='blue')
    # plt.show()
    plt.savefig(r'.\static\assets\img\feelings.png',dpi=500)

    yes = '%.f%%' % (rate * 100)
    return yes

if __name__ == '__main__':
    Feelings("影视剧")