以下是对整个项目《基于机器学习的广州链家二手房房价预测》的说明：
运行平台：Pycharm / Python 3.x

项目结构说明：
本项目是一个完整的机器学习项目，从数据获取到模型应用的完整流程。

==================================================
一、Dataset目录（数据获取与清洗）
==================================================
-dataacquiring.py：爬取链家二手房数据
-datacleaning.py：对爬取的数据进行合并和初步清洗
-dataprocessing.py：对数据进行进一步清洗
-11个区的CSV文件（baiyun.csv, conghua.csv, haizhu.csv等）：
  广州链家网站各个区的爬取初始数据
-广州市链家二手房数据(初).csv：合并且初步清洗得到的数据
-广州市链家二手房数据(终).csv：进一步清洗得到的数据

==================================================
二、DataPreprocessing目录（数据预处理）
==================================================
-datapreprocessing.py：对数据进行预处理（三大项处理）
  1. 缺失值处理：删除缺失关键字段的记录，用众数填充部分缺失值
  2. 重复值处理：删除完全重复的记录
  3. 异常值处理：规范化楼层、建房时间等字段
-广州链家二手房数据(三大项处理后).csv：三大项处理后的数据

==================================================
三、ModelTraining目录（模型训练与评估）
==================================================
【数据探索与特征工程】
-dataseeking.py：数据探索，对特征进行探索分析（相关性分析、热力图等）
-featureengineering.py：特征工程，将原始数据转换为模型可用的特征
  - 所在区编码（按GDP排序）
  - 房屋户型编码（室+厅总数）
  - 房屋朝向编码（按风水学排序）
  - 装修情况、楼层、建筑类型编码
  - 建房时长计算（2024-建房年份）

【模型训练】
-modelpipeline.py：构建模型流水线，对比多个模型性能
  - 线性回归（Linear Regression）
  - 决策树（Decision Tree）
  - 随机森林（Random Forest）
  - 输出：results.csv（包含各模型的RMSE、R²分数、训练时间等）

-train_random_forest.py：随机森林模型调优和训练
  - 使用RandomizedSearchCV进行超参数搜索
  - 对比默认参数和调参结果，选择最优参数
  - 在完整数据集上训练最终模型
  - 输出：final_best_model.pkl（最终模型）
  - 输出：final_best_model_params.json（最佳参数）

【模型应用】
-predict.py：使用训练好的模型进行房屋价格预测
  - 支持中文名称或数字编码输入
  - 提供友好的预测接口和格式化输出
  - 包含多个预测示例

【可视化与日志】
-experimentvisualization.py：实验结果可视化（模型对比图表）
-results.csv：模型对比结果（各模型的性能指标）
-runlog/：运行日志目录
  - modelpipeline.log：模型训练日志

==================================================
四、项目根目录
==================================================
-model_data.csv：特征工程后的最终数据（用于模型训练）

==================================================
项目运行流程建议
==================================================
1. 数据获取：运行 Dataset/dataacquiring.py（如需要更新数据）
2. 数据清洗：运行 Dataset/datacleaning.py 和 dataprocessing.py
3. 数据预处理：运行 DataPreprocessing/datapreprocessing.py
4. 特征工程：运行 ModelTraining/featureengineering.py（生成model_data.csv）
5. 数据探索：运行 ModelTraining/dataseeking.py（可选）
6. 模型训练：
   - 运行 ModelTraining/modelpipeline.py（多模型对比）
   - 运行 ModelTraining/train_random_forest.py（随机森林调优）
7. 模型应用：运行 ModelTraining/predict.py（进行房屋价格预测）

==================================================
模型性能
==================================================
根据 results.csv 的结果：
- 线性回归：Test RMSE = 284.18，Test R² = 0.299
- 决策树：Test RMSE = 179.42，Test R² = 0.720
- 随机森林：Test RMSE = 137.99，Test R² = 0.835（最优）

最终模型使用随机森林，默认参数（n_estimators=100），性能最佳。

==================================================
注意事项
==================================================
1. 确保所有依赖库已安装（pandas, numpy, sklearn, matplotlib, seaborn等）
2. 运行脚本时注意文件路径，建议在项目根目录运行
3. 特征工程后的数据保存在根目录的 model_data.csv
4. 最终训练好的模型保存在 ModelTraining/final_best_model.pkl
5. 使用 predict.py 进行预测时，确保模型文件存在
