import jieba        #分词
from matplotlib import pyplot as plt    #绘图，数据可视化
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算
import sqlite3                          #数据库

def wordcloud():
    #准备词云所需的文字（词）
    con = sqlite3.connect('comments.db')
    cur = con.cursor()
    sql = 'select content from comments'
    data = cur.execute(sql)
    text = ""
    for item in data:
        text =  text + item[0]
        #print(item[0])
    #print(text)
    cur.close()
    con.close()

    #分词
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(len(string))
    num = len(string)

    stopwords = ["我", "你", "她", "的", "是", "了", "在", "也", "和", "就", "都", "这"
                 "很", "有", "吧", "啊", "那", "多", "对", "把", "呢", "没有", "还有", "好",
                 "看", "太"]
    img = Image.open(r'.\static\assets\img\logo.jpg')   #打开遮罩图片
    img_array = np.array(img)   #将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path="msyh.ttc",    #字体所在位置：C:\Windows\Fonts
        stopwords=stopwords
    )
    if string == '':
        return 0
    wc.generate_from_text(string)


    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')     #是否显示坐标轴

    # plt.show()    #显示生成的词云图片

    #输出词云图片到文件
    # plt.savefig(r'.\static\assets\img\word.png', dpi=500)
    wc.to_file(r'.\static\assets\img\word.png')
    print("图片已成功保存")

    return num

def main():
    wordcloud()

if __name__ == '__main__':
    main()















