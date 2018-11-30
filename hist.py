# 直方图
import matplotlib.pylab as pyl
import numpy

data = numpy.random.normal(10.0, 1.0, 10000)
style = numpy.arange(0,50,8)
# pyl.hist(data)
pyl.hist(data, histtype='stepfilled')
# pyl.hist(data, style, histtype='stepfilled')
pyl.show()
