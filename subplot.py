import matplotlib.pylab as pyl
import numpy

pyl.subplot(221)
x1 = [1,2,3,4,5]
y1 = [5,3,5,23,5]
pyl.plot(x1, y1)

pyl.subplot(222)
x2 = [5,2,3,8,6]
y2 = [7,9,12,12,3]
pyl.plot(x2, y2)

pyl.subplot(212)
x3 = [5,6,7,10,19,12,11]
y3 = [6,2,4,21,5,13,8]
pyl.plot(x3, y3)

pyl.show()
