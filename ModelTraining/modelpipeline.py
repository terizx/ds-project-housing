import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import time
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

# 创建文件日志处理器（确保目录存在）
log_dir = './runlog'
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, 'modelpipeline.log'), encoding='utf-8')
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'))

# 添加文件日志处理器到logger
logger.addHandler(fh)

# 构建模型流水线（
data_path = './model_data.csv'
data = pd.read_csv(data_path)

# 特征和标签
X = data.drop(columns=['总价'], axis = 1)
y = data['总价']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义要使用的模型字典
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42)
}

# 创建一个DataFrame来保存结果
results = pd.DataFrame(columns=['Model', 'Test RMSE', 'Train Score', 'Test Score', 'Training Time'])
count = 0

for name, model in models.items():
    start_time = time.time()
    pipeline = Pipeline([('scaler', StandardScaler()),
                         ('model', model)
                         ])
    # 训练模型
    pipeline.fit(X_train, y_train)
    # 预测
    y_pred = pipeline.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    training_time = time.time() - start_time
    count += 1
    total = len(models)
    logger.info(f'{name} 模型训练中：{count}/{total}，已用时{training_time:.2f}秒。')
    print(f'{name} 模型训练中：{count}/{total}，已用时{training_time:.2f}秒。')
    # 打印结果
    new_row = pd.DataFrame({
        'Model': [name],
        'Test RMSE': [rmse],
        'Train Score': [train_score],
        'Test Score': [test_score],
        'Training Time': [training_time]
    })
    results = pd.concat([results, new_row], axis=0, ignore_index=True) #按行

logger.info(results)
print(results)
# 保存结果到 CSV（ModelTraining/results.csv）
results_path = os.path.join(os.path.dirname(__file__), 'results.csv')
results.to_csv(results_path, index=False, encoding='utf-8-sig')
logger.info(f'Results saved to {results_path}')
print(f'Results saved to {results_path}')