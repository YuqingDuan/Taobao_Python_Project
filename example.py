'''老师演示的数据库 title/link/price/comment列依次为商品名称/链接地址/价格/评论数'''

# 导入相关包
import pymysql
import numpy as npy
import pandas as pda

# 导入数据
conn = pymysql.connect(host = "127.0.0.1", user = "root", passwd = "Devilhunter9527", db = "taotao")
sql = "select * from tb_item"
data = pda.read_sql(sql, conn)
# 通过比较data.describe()和len(data)的值可以发现：缺失数据的条数 = len(data) - data.describe()
print(data.describe())
print(len(data))

# 数据清洗
# 1.下面对price为0的值(也就是缺失值)进行处理
num  = 0
# 对price的缺失值统统赋值为None，方便下面处理。对下面这行代码拆分来看：
# (data['price']==0) 判断data['price']列中哪行price的值等于0，等于的返回True，不等于返回False
# data['price'][(data['price']==0)] 这语句就是一下子把所有price=0的给取出来了 ，然后哪行的price等于0就 赋值为None
data["price"][(data["price"]==0)] = None
# for循环设置price的缺失值
for i in data.columns: # 遍历data的每列
    for j in range(len(data)): # 遍历data的每一行
        # i在这是一维（列）,data[i]等于把这一列的值取出来了，j在这里是二维（行）
        # data[i].isnull是判断整列的某一个值是None那么就返回True,data[i].isnull[j]是逐行逐行的判断是否为nan了，是的话返回True从而进行下面代码块的处理。
        if(data[i].isnull())[j]:
            data[i][j] = "64" # 缺失值设置为均值
            num+=1
print(num) # 输出一共修改了多少个缺失值

# 2.异常值处理
# 首先要找到异常值：通过画散点图（横轴：价格，纵轴：评论数）
# 我们这里的话要选取评论数，价钱。通常的方法就是说通过遍历每一行的数据，取每一行中的price和comment值，但是呢这个方法效率低下。
# 对此我们可以采用转置方法，把price列转置为一行，这样就能够快速取到这价钱的数据，还有评论数。comment同此理。
dataT=data.T # 转置下数据
prices = dataT.values[2] # 取第3行数据
comments = dataT.values[3] # 取第4行数据

# 画散点图
pylab.plot(prices, comments, 'o')   
pylab.xlabel('prices')
pylab.ylabel('comments')
pylab.title(" The Good's price and comments")
pylab.show()

# 处理异常数据，我这里定义的异常数据就是评论数超过20W，价格大于2000
line = len(data.values)   # 取行数
col = len(data.values[0])   # 取列数
davalues = data.values    #取data的所有值
for i in range(0,line):    # 遍历行数
    for j in range(0,col):   #遍历列数
        if davalues[i][3]>200000:    #判断评论数
            davalues[i][j] = 562   # 评论数取平均值
        if davalues[i][2]>2000:
            davalues[i][j] =  64   # 价钱取平均值

# 画处理完异常值之后的散点图
prices2=davalues.T[2]
comments2=davalues.T[3]
pylab.plot(prices2, comments2, 'or')
pylab.xlabel('prices')
pylab.ylabel('comments')
pylab.title(" The Good's price and comments")
pylab.show()

# 显然我们已经对评论数超过20W，价格大于2000的数据处理了，但是呢上图显示的还是不够漂亮,
# 因为异常点与正常点的差距太大了，导致正常点与正常点之间的间隔非常小，小到黏在一块了，所以我们还需要在处理下，
# 把评论数超过2000，价格大于300的处理掉，这样的话，正常点就能够很好的展现在图上，代码如下：
'''
line = len(data.values)   # 取行数
col = len(data.values[0])   # 取列数
davalues = data.values    #取data的所有值
for i in range(0,line):    # 遍历行数
    for j in range(0,col):   #遍历列数
        if davalues[i][3]>2000:    #判断评论数，===主要修改这行
            davalues[i][j] = 562   # 评论数取平均值        
        if davalues[i][2]>300:    # ===主要修改这行
            davalues[i][j] =  64   # 价钱取平均值
prices2=davalues.T[2]
comments2=davalues.T[3]
pylab.plot(prices2,comments2,'or')
pylab.xlabel('prices')
pylab.ylabel('comments')
pylab.title(" The Good's price and comments")
pylab.show()
'''

# 商品数据分布分析
# 我们在这里要分析商品数据的分布，看评论数与价钱的在哪个数量段的分布最多
# 首先我们需要计算出价钱和评论的最值，其次在计算最值之间的极差，最后计算组距（极差/组数，组数自己根据情况定义）。下面请看代码：
da2=davalues.T
pricemax = da2[2].max()
pricemin = da2[2].min()
commentmax = da2[3].max()
commentmin = da2[3].min()
# 极差
pricerg =  pricemax - pricemin
commentrg = commentmax -commentmin
# 组距
pricedst = pricerg/10
commentdst = pricerg/10

# 绘制直方图
# 价钱直方图
pricesty = numpy.arange(pricemin, pricemax, pricedst)
pylab.hist(da2[2],pricesty)
pylab.show()
# 评论直方图
commentty = numpy.arange(commentmin, commentmax, commentdst)
pylab.hist(da2[3],pricesty)
pylab.show()
'''
从图中我们可以看出，评论数最多的集中在100元以内的商品，评论数也间接的说明了购买数，因为购买后才能够评论。
所以可以根据这个来直方图来给商品定价。从价钱直方图中我们可以看出，商品价钱最多的集中在50元以内的商品。
'''








