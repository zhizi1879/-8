#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import numpy as np
import pandas as pd
from scipy import stats                          #scipy以及stats是什么工具(scipy是统计分析，stats是检验分析)
import matplotlib.pyplot as plt     #为什么是这样的写法呢？（plt.pyplot.plot()这个样就很冗杂,而前面的写法只需要plt.plot()）

np.random.seed(42)

# 样本量
n = 200

# 性别：0=女，1=男
gender = np.random.choice([0, 1],p=[0.6, 0.4], size=n,)  #choice是什么函数？（这个是有放回抽样，里面的位置是不能改变的）
gender_label = np.select([gender==0,gender==1],['女','男'],default='未知')    #select函数里default是必须的吗（是的  ）



# 年级：1=大一，2=大二，3=大三，4=大四
grade = np.random.choice([1, 2, 3, 4], p=[0.3, 0.3, 0.2, 0.2],size=n,)
grade_label = np.select([grade==1,grade==2,grade==3,grade==4],['大一','大二','大三','大四'],default='未知')    #为什么不打引号？（因为是布尔值’==‘是布尔关系的标志，’=‘才是赋值）（相当于if从句，if,grade==1关系成立的话，就是对应“大一”）


anxiety = np.random.normal(loc=15, scale=5,size=n)    #normal是什么函数？（正态分布）       括号里面能改变位置吗？（可以的）
print(anxiety)