#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['font.sans-serif'] = ['SimHei']   # Windows用黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')  # 隐藏坐标轴

# 三个阶段的坐标 (x, y, 宽, 高)
boxes = [
    {"label": "前测", "x": 1, "y": 4, "w": 2, "h": 1, "color": "#dae3f3"},
    {"label": "训练", "x": 4, "y": 4, "w": 2, "h": 1, "color": "#d5e8d4"},
    {"label": "后测", "x": 7, "y": 4, "w": 2, "h": 1, "color": "#f8cecc"}
]

# 画矩形和文字
for b in boxes:
    rect = mpatches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                                    boxstyle="round,pad=0.1",
                                    facecolor=b["color"], edgecolor="black")
    ax.add_patch(rect)
    ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]/2, b["label"],
            ha='center', va='center', fontsize=12, fontweight='bold')

# 画箭头
for i in range(2):
    ax.annotate('', xy=(boxes[i+1]["x"], boxes[i]["y"]+0.5),
                xytext=(boxes[i]["x"]+boxes[i]["w"], boxes[i]["y"]+0.5),
                arrowprops=dict(arrowstyle='->', lw=1.5))

# 添加详细说明文字
notes = [
    ("经典点探测任务\n高-低图片对40张 + 中-中16张\n共56 trial", 2, 2.5),
    ("修改的点探测任务\n高-低图片对40张（每张重复2次）\n共160 trial\n探测点90%出现在低热量图片位置", 5, 2.0),
    ("程序同前测", 8, 2.5)
]
for text, x, y in notes:
    ax.text(x, y, text, ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f5f5", edgecolor="gray"))

# 训练时长标注
ax.annotate("~30 min", xy=(5, 5.2), ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig("exp2_overview.png", dpi=150)
plt.show()


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 3))
ax.set_xlim(0, 12)
ax.set_ylim(0, 2)
ax.axis('off')

# 四个阶段
steps = [
    {"label": "+", "sub": "500 ms", "x": 1, "color": "#e1d5e7"},
    {"label": "高-低热量\n食物图片对", "sub": "1000 ms / 2000 ms", "x": 4, "color": "#dae3f3"},
    {"label": "探测点出现\n按 F 或 J 反应", "sub": "90% 出现在低热量图片位置", "x": 7, "color": "#d5e8d4"},
    {"label": "空屏", "sub": "500 ms", "x": 10, "color": "#fff2cc"}
]

for s in steps:
    # 矩形框
    rect = mpatches.FancyBboxPatch((s["x"]-0.8, 0.2), 1.6, 1.2,
                                    boxstyle="round,pad=0.1",
                                    facecolor=s["color"], edgecolor="black")
    ax.add_patch(rect)
    # 主文字
    ax.text(s["x"], 0.9, s["label"], ha='center', va='center', fontsize=10, fontweight='bold')
    # 副文字
    ax.text(s["x"], 0.4, s["sub"], ha='center', va='center', fontsize=8)

# 画箭头
for i in range(3):
    ax.annotate('', xy=(steps[i+1]["x"]-0.9, 0.8),
                xytext=(steps[i]["x"]+0.9, 0.8),
                arrowprops=dict(arrowstyle='->', lw=1.5))

plt.suptitle("实验2训练阶段 —— 1个trial流程图", y=0.95, fontsize=12)
plt.tight_layout()
plt.savefig("exp2_trial.png", dpi=150)
plt.show()