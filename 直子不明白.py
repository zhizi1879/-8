#!/usr/bin/python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']

# 创建示例数据
np.random.seed(42)
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')  #date.range函数
data = {
    'date': np.random.choice(dates, 1000),                #有重复值
    'product': np.random.choice(['A', 'B', 'C'], 1000, p=[0.5, 0.3, 0.2]),
    'quantity': np.random.randint(1, 10, 1000),           #随机整数
    'price': np.random.uniform(50, 500, 1000),            #随机浮点数
    'customer_id': np.random.randint(1000, 2000, 1000)
}
df = pd.DataFrame(data)
df['revenue'] = df['quantity'] * df['price']

# 数据清洗
print(f"缺失值: {df.isnull().sum().sum()}")        #第一个sum()是每一列的缺失值计算，而第二个sum()是缺失值的总和
df = df.drop_duplicates()

# 1. 月度销售趋势分析
df['month'] = df['date'].dt.to_period('M')    #dt.to_period以日为单位，转换成月为单位，变成12个月，方便每个月做数据分析
monthly_sales = df.groupby('month')['revenue'].agg(['sum', 'mean', 'count'])   #［revenue］数据里面的那一serious；eggregate是聚合，直接集合计算多种类型           df.groupby(by='要分组的列名')[ '要计算的列' ].聚合函数()

# 2. 产品分析
product_analysis = df.groupby('product').agg({                        # groupby后面聚合运算是不同列那么就用字典打包
    'revenue': 'sum',
    'quantity': 'sum',
    'customer_id': 'nunique'               #count统计        nunique去重统计
}).round(2)
product_analysis.columns = ['总销售额', '总销量', '客户数']      #右边赋值左边，你认为是某个库的，带函数，但实际上它就是一个简单的属性，所以因此是在赋值号的左边而不是在右边
                                                              #而在另外，因为你觉得复制号右边一般都是这个库的函数带列表或元组，然后这里单单只有列表，所以你觉得比较缺，所以你认为不应该这样写，

# 可视化
fig, axes = plt.subplots(2, 2, figsize=(14, 10))             #2，2生成2×2列联表，然后是有4个子图，生产右边画布尺寸4个，在这个过程中，它就会产生轴域，而轴域就是前面序列解包给的axes

# 月度销售趋势
axes[0,0].plot(monthly_sales.index.astype(str), monthly_sales['sum'], marker='o')    #axes［0.0］第一个是行第二个是列，实际上应该在左上角建立直角坐标系； plot是画折线图（x，y）；因为是从日期转到月份所以index就是每个月份最后一天而不是一月等于0 ;0→o  o→实心圆   s→□
axes[0,0].set_title('月度销售趋势', fontsize=12)
axes[0,0].set_xlabel('月份')
axes[0,0].set_ylabel('销售额')
plt.setp(axes[0,0].xaxis.get_majorticklabels(), rotation=45)            #setp(set property) xaxis.get_majorticklabels()(x的横坐标对象)  rotation(旋转角度)

# 产品销售占比
axes[0,1].pie(product_analysis['总销售额'], labels=product_analysis.index, autopct='%1.1f%%')  #pie饼图 index(可表示标签)  "%1.1f%%"(写法分三步)（格式化字符串）   autopct(扇形统计图的定义绘画)
axes[0,1].set_title('产品销售分布')

# 价格分布
axes[1,0].hist(df['price'], bins=30, edgecolor='black', alpha=0.7)#hist(直方图)  bin=30是柱子数量  alpha(透明度0-1，1完全不透明)
axes[1,0].set_title('商品价格分布')
axes[1,0].set_xlabel('价格')
axes[1,0].set_ylabel('频次')

# 客户购买频次
customer_freq = df.groupby('customer_id').size()
axes[1,1].hist(customer_freq, bins=20, edgecolor='black', alpha=0.7)
axes[1,1].set_title('客户购买频次分布')
axes[1,1].set_xlabel('购买次数')
axes[1,1].set_ylabel('客户数')

plt.tight_layout()   #plt.tight.layout()(自动化排班版优化)
plt.show()

print("\n产品分析结果:")
print(product_analysis)
print(f"\n总销售额: ¥{df['revenue'].sum():,.2f}")  #f-string 格式化字符串 :开始标记 ，千位字符  .2f小数




































#读代码习惯，从右往左，从内往外
#括号元组()表动作，［］表示选取
#leetcode
#①看懂  ②能结构复述  ③刻意练习
#终端   面向对象编程→偏简单
#《笨办法学python》
#python三剑客
#pythoncookbook字典
#我觉得每天抄代码，复刻代码还是很有必要的，第1点会有一个量变到质变，第2个点我觉得是进一步理解代码的进阶方式
#我感觉就三个①看得懂代码②能理解代码结构③能写出代码
#spychopy
#pingouin Vs scipy
#seaborn 和 plotly（更偏交互）
#真正的能力  a.解决实际问题的思维  b.一周能掌握一个库的能力
#眼动数据接口eyelink  pygaze（能操作眼动仪器）    文本分析transforms
#psychopy  编实验程序的  pytorch深度学习的
#print(1,2,3,4,sep="→")
#soup3D
#pydorid3
#一个能力一个能力的学习→动手写代码的能力非常强（复刻能力）
# Ai算法工程师Future的人工智能课程
#scipy（基于numpy;通用计算工具；正常操作） 与 pingouin（潘盖in）(基于pandas;贴合适配心理学专业分析；方便快捷)
#streamlit简单搭建网页
#claude
#总结来说，这不是作弊，这是新一代的科研和开发素养。 就像我们现在不会认为“用 SPSS 算回归”是作弊
#python数据分析与挖掘实战
#基础语法——numpy,pandas,matplotlib--SPSS复刻--web开发，plotly可视化，自动化处理数据--贝叶斯因子，混合效应模型，网络分析（谁和谁说八卦，八卦是怎么传开的），文本情感分析（这些人说的八卦是好话还是坏话）
#streamlit可视化比较牛的用法