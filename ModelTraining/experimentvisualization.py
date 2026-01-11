import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 读取 results.csv（路径跟脚本同文件夹最稳）
BASE_DIR = os.path.dirname(__file__)
results_path = os.path.join(BASE_DIR, "results.csv")

df = pd.read_csv(results_path)

# 去掉列名可能存在的空格（很常见）
df.columns = [c.strip() for c in df.columns]

# 只保留你要展示的三列
model_col = "Model"
rmse_col = "Test RMSE"
r2_train_col = "Train Score"
r2_test_col = "Test Score"

# 如果你只想画“你最终选的3个模型”，可以在这里手动指定筛选（可选）
# keep_models = ["Linear Regression", "Decision Tree", "Random Forest"]
# df = df[df[model_col].isin(keep_models)]

# 排序：按 RMSE 从小到大更直观（也可按 Test Score 从大到小）
df = df.sort_values(by=rmse_col, ascending=True)

models = df[model_col].tolist()
rmse = df[rmse_col].tolist()
r2_train = df[r2_train_col].tolist()
r2_test = df[r2_test_col].tolist()

# -------- 图1：RMSE --------
fig1, ax1 = plt.subplots(figsize=(8, 6))
bars = ax1.bar(models, rmse)
ax1.set_xlabel("Model")
ax1.set_ylabel("Test RMSE")
ax1.set_title("Model RMSE Compare")

# 数值标签
for bar in bars:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h, f"{h:.2f}", ha="center", va="bottom")

plt.xticks(rotation=15)
plt.tight_layout()

# -------- 图2：R2 (Train/Test) --------
fig2, ax2 = plt.subplots(figsize=(8, 6))
bar_width = 0.35
index = np.arange(len(models))

b1 = ax2.bar(index, r2_train, bar_width, label="R2_train")
b2 = ax2.bar(index + bar_width, r2_test, bar_width, label="R2_test")

ax2.set_xlabel("Model")
ax2.set_ylabel("R2 Score")
ax2.set_title("Model R2 Score Compare")
ax2.set_xticks(index + bar_width / 2)
ax2.set_xticklabels(models, rotation=15)
ax2.legend()

def add_labels(bars):
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h, f"{h:.3f}", ha="center", va="bottom")

add_labels(b1)
add_labels(b2)

plt.tight_layout()

# ===== 自动保存图片到文件夹 =====
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

rmse_path = os.path.join(OUT_DIR, "rmse.png")
r2_path   = os.path.join(OUT_DIR, "r2.png")

fig1.savefig(rmse_path, dpi=300, bbox_inches="tight")
fig2.savefig(r2_path, dpi=300, bbox_inches="tight")

print("✅ Saved:", rmse_path)
print("✅ Saved:", r2_path)

plt.show()
