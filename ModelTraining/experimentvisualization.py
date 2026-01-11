import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

x = ['随机森林', '梯度提升树', '融合模型']
RMSE = [137.3, 142.05, 134.87]
R2_train = [0.939, 0.927, 0.929]
R2_test = [0.836, 0.831, 0.845]

# 创建一个图形和一个轴
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.bar(x, RMSE, label='RMSE')
# 添加标签和标题
ax1.set_xlabel('Model')
ax1.set_ylabel('RMSE')
ax1.set_title('Model RMSE Compare')
ax1.set_ylim(100, 150)
ax1.legend()
# 添加数值标签到条形图上
for i, v in enumerate(RMSE):
    ax1.text(i, v + 1, str(v), ha='center', va='bottom')

# 创建第二个图形和一个轴，用于绘制R²分数条形图
fig2, ax2 = plt.subplots(figsize=(8, 6))
# 设置柱状图的宽度
bar_width = 0.35
index = np.arange(len(x))

bar1 = ax2.bar(index, R2_train, bar_width, label='R2_train', color='red')
bar2 = ax2.bar(index + bar_width, R2_test, bar_width, label='R2_test', color='green')
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height, '%.3f' % height, ha='center', va='bottom')

add_labels(bar1)
add_labels(bar2)
ax2.set_xlabel('Model')
ax2.set_ylabel('R2 Score')
ax2.set_title('Model R2 Score Compare')
ax2.set_xticks(index + bar_width / 2, x)  # 设置x轴刻度位置在两组柱状图的中间
ax2.set_ylim(0.8, 0.95)
ax2.legend()

plt.tight_layout()
plt.show()