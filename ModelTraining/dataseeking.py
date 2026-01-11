import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Songti SC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

file_path = os.path.join(os.path.dirname(__file__), "..", "model_data.csv")
file_path = os.path.abspath(file_path)   # 变成绝对路径，最稳
df = pd.read_csv(file_path)

X = df.drop('总价', axis=1)
y = df['总价']
# 计算所有特征和总价的相关性
correlations = X.corrwith(y).abs()
print(correlations)
# 按照相关性排序并选择前n个特征
n_top_features = 5
top_features = correlations.nlargest(n_top_features).index
X_selected = X[top_features]
print(f"前{n_top_features}的特征有：", top_features.tolist())
# 由于无论是否增加或减少特征，对于机器学习的得分几乎没有什么变化

# 绘制热力图
corr_matrix = df.corr()
plt.figure(figsize=(10, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .5})
plt.title(f'Correlation Heatmap of Features with Target')

# ===== 3) 保存到统一文件夹 outputs/figures =====
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_dir = os.path.join(project_root, "outputs")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "heatmap.png")
plt.savefig(out_path, dpi=300, bbox_inches="tight")

print("✅ Heatmap saved to:", out_path)

plt.show()