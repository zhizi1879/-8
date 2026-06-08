#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']          #reParams(全局控制字典，调整默认系统参数的函数)
plt.rcParams['axes.unicode_minus'] = False            #axes.unicode_minus(减号-不用unicode版本的,这样防止后面减号变成方框)
fig, ax = plt.subplots(figsize=(10, 1.5))             #subplots（布置画布的函数，figsize(10,1.5)画布的尺寸，fig,ax是画布和轴域）  ;   fig,ax（元组解包,仿佛后面的函数解开后，就多了对象，因此可以赋值给两个变量）
ax.set_xlim(0, 12)                                    #设置x轴的长度
ax.set_ylim(0, 1)                                     #设置y轴的长度
ax.axis('off')                                        #关闭坐标系
steps = [
    (2.0, "前测\n(经典点探测)\n56 trials", "高-低/中-中图片对\n探测点50%:高热量侧"),           #[],()(列表，元组)
    (6.0, "训练\n(修改点探测)\n160 trials, ~30 min", "探测点90%:低热量侧\n10%:高热量侧"),     #(6.0, "训练\n(修改点探测)\n160 trials, ~30 min", "探测点90%:低热量侧\n10%:高热量侧")(x轴坐标，主标题，副标题)
    (10.0, "后测\n(同前测)\n56 trials", "程序同前测")
]
for x, title, subtitle in steps:
    rect = plt.Rectangle((x-1.2, 0.2), 2.4, 0.6, fill=False, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, 0.55, title, ha='center', va='center', fontsize=9)                      #ha,va(horizontal alignment水平居中;vertical alignment垂直居中);x,0.55(横竖坐标轴，定中心文字四周延展，而不是文字塞在一个坐标点里面)
    ax.text(x, 0.3, subtitle, ha='center', va='center', fontsize=7, color='gray')      #ax.text(已经内置添加在画布上了，所以不用ax.daa_patch(rect)了)
for i in range(2):
    ax.annotate('', xytext=(steps[i][0]+1.2, 0.5),xy=(steps[i+1][0]-1.2, 0.5),         #anotate(anotate注释箭头函数，''不需要文字,xytext是起点，xy是终点)
                arrowprops=dict(arrowstyle='->', lw=1))                                #arrowprops(箭头属性),dict（字典，就是存放基本属性的）,arrowstyle(箭头类型),line width(箭头线条粗细)
plt.savefig('exp2_flowchart.png', dpi=150, bbox_inches='tight')                        #bbox_inches='tight'(自动剪切多余空白)
plt.show()

