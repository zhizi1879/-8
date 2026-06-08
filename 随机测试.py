import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 2.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 2)
ax.axis('off')
boxes = [
    (1.2, 1, 1.5, 1.2, "+", "500 ms"),
    (4.0, 1, 2.5, 1.2, "高-低热量食物图片对", "1000 ms / 2000 ms"),
    (7.5, 1, 2.5, 1.2, "探测点出现\n按F或J反应", ""),
    (10.0, 1, 1.5, 1.2, "空屏", "500 ms")
]
for x, y, w, h, main_text, sub_text in boxes:
    rect = plt.Rectangle((x - w/2, y - h/2), w, h, fill=False, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y, main_text, ha='center', va='center', fontsize=10)
    if sub_text:
        ax.text(x, y - 0.3, sub_text, ha='center', va='center', fontsize=9, color='gray')
arrows = [(boxes[i][0] + boxes[i][2]/2, 1, boxes[i+1][0] - boxes[i+1][2]/2, 1) for i in range(len(boxes)-1)]
for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', lw=1))
plt.tight_layout()
plt.savefig('flowchart.png', dpi=150, bbox_inches='tight')
plt.show()










