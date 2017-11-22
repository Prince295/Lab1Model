import os
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from matplotlib import mlab


def save(name='', fmt='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(fmt)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)
    #plt.close()


h=float(input("Введите шаг интегрирования "))
k=1; l=10; m=1;n=5; kt=110; b=29000; i1=10; i2=2; s=100; V=500; T=14;sigma_max=0.5
x1=0.7; x2=0.7; x3=0; x4=0; x5=700
x1b=0.7; x2b=0.7; x3b=0; x4b=0; x5b=700
g=9.81; t=0; y=0
array1=[]; array2=[]; array3=[]; array4=[]; array5=[]
array1b=[]; array2b=[]; array3b=[]; array4b=[]; array5b=[]
tarray = mlab.frange(0, T, h)
tarray2 = mlab.frange(0, T, h/2)



def eyler(x, f, array):
    xd = x + h * f
    x=xd
    array.append(xd)
    return x

def new_X1(x1,x2):
    x1 = k * x2 - k * x1
    return x1

def new_X2(x3):
    x2 = x3;
    return x2

def new_X3(x1,x2,x3,x4):
    x3 = l*x1-l*x2-m*x3+n*x4
    return x3

def new_X4(x2,x3,x4,x5,tay,sigma_max):
    opera=(10000-x5)/(b-V*tay)
    sigma = -kt*x4-i1*x2-i2*x3+s*(opera-x2)
    if np.fabs(sigma)<=sigma_max:
        x4 = sigma
        return x4
    else:
        sigma_max = sigma

        return sigma_max

def new_X5(x1):
    x5 = V*np.sin(x1)
    return x5

def accuracy(array,array2):
    acc=np.empty(len(tarray))
    ao_acc=np.empty(len(tarray))
    for t in tarray:
        acc[int(t)]=np.fabs(array[int(t*2)]-array2[int(t)])
        ao_acc[int(t)]=np.fabs((array[int(t*2)]-array2[int(t)])/array[int(t*2)])
    o_acc=np.mean(acc)
    a_acc=np.mean(ao_acc)
    return o_acc, a_acc


while True:
    for t in range(len(tarray)):
        tay = tarray[t]
        x1=eyler(x1,new_X1(x1,x2),array1)
        x2=eyler(x2,new_X2(x3),array2)
        x3=eyler(x3,new_X3(x1,x2,x3,x4),array3)
        x4=eyler(x4,new_X4(x2,x3,x4,x5,tay,sigma_max),array4)
        x5=eyler(x5,new_X5(x1),array5)
        for i in range(1):
            tay = tarray[t]+h/2
            x1b = eyler(x1b, new_X1(x1b, x2b), array1b)
            x2b = eyler(x2b, new_X2(x3b), array2b)
            x3b = eyler(x3b, new_X3(x1b, x2b, x3b, x4b), array3b)
            x4b = eyler(x4b, new_X4(x2b,x3b,x4b,x5b, tay, sigma_max), array4b)
            x5b = eyler(x5b, new_X5(x1b), array5b)

    print1,print2=accuracy(array5b,array5)
    print2=print2*100
    if print2<1:
        break
    else:
        h=h/2
        k = 1;  l = 10;        m = 1;        n = 5;        kt = 110;        b = 29000;        i1 = 10;
        i2 = 2;        s = 100;        V = 500;        T = 14;        sigma_max = 0.5
        x1 = 0.7;        x2 = 0.7;        x3 = 0;        x4 = 0;
        x5 = 700
        x1b = 0.7;        x2b = 0.7;        x3b = 0;        x4b = 0;        x5b = 700
        g = 9.81;        t = 0;
        y = 0
        array1 = []; array2 = []; array3 = []; array4 = []; array5 = []
        array1b = []; array2b = []; array3b = []; array4b = []; array5b = []
        tarray = mlab.frange(0, T, h)
        tarray2 = mlab.frange(0, T, h / 2)


print("Абсолютная погрешность на шаге " + str(h) + " = " + str(print1))
print("Относительная погрешность на шаге "+ str(h) + " = " + str(print2) + " %")


text_style = dict(horizontalalignment='right', verticalalignment='center',fontsize=12, fontdict={'family': 'monospace'})
color = 'cornflowerblue'
fig = plt.figure(1)

plt.plot(tarray,array1,"-b", color="orange", linestyle="-.", label="график X1")
plt.plot(tarray,array2,"-b", color="yellow", linewidth=0.5, label="график X2")
plt.plot(tarray,array3,"-b", color="blue", linewidth=0.5, label="график X3")
plt.plot(tarray,array4,"-b", color="green", label="график X4")
plt.ylabel("значения X")
plt.xlabel("период T")
plt.legend()
plt.grid(True)

fig2 = plt.figure(2)

plt.plot(tarray,array5,"-b", color="red", linewidth=0.5, label="график X5")
plt.ylabel("значения X")
plt.xlabel("период T")
plt.legend()
plt.grid(True)


save(name='pic_1_4_2', fmt='pdf')
save(name='pic_1_4_2', fmt='png')

plt.show()
