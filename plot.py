# 绘制折线图和散点图
import matplotlib.pylab as pyl
import numpy

x1=[1,2,3,4,8]
y1=[5,7,2,1,5]
x2=[1,3,6,8,10,12,19]
y2=[1,6,9,10,19,23,35]
# pyl.plot(x1, y1)
# pyl.plot(x1, y1, 'o')
# pyl.show()

# 颜色
    # c-cyan
    # r-red
    # m-magente
    # g-green
    # b-blue
    # y-yellow
    # k-black
    # w-white
# pyl.plot(x1, y1, 'or')
# pyl.show()

# 线条样式
    # - 直线
    # -- 虚线
    # -. 点划线
    # ：细小虚线
# pyl.plot(x1, y1, '-.')
# pyl.show()

# 点的样式
    # s 方形
    # h 六角形
    # H 六角形
    # * 星型
    # + 加号
    # x x型
    # d 菱形
    # D 菱形
    # p 五角形
pyl.plot(x1, y1, "*")
pyl.plot(x2, y2, "D")
pyl.title("title")
pyl.xlabel("xlabel")
pyl.ylabel("ylabel")
pyl.xlim(0, 20)
pyl.ylim(0, 40)
pyl.show()




    
