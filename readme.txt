以下是对整个项目《基于机器学习的广州链家二手房房价预测》的说明：
运行平台：Pycharm

dataset目录：
-广州链家二手房数据(三大项处理后).csv：三大项（缺失值、重复值、异常值）处理后的数据


整体项目可通过以下顺序大致进行阅读：
Machine-Learning-Work目录（包含代码和各种中间数据集）：
-Dataset目录：
	-dataacquiring.py：爬取链家二手房数据
	-datacleaning.py：对爬取的数据进行合并和初步清洗
	-dataprocessing.py：对数据进行进一步清洗
	-11个英文名.csv：广州链家网站各个区的爬取初始数据
	-广州市链家二手房数据(初).csv：合并且清洗得到的数据
	-广州市链家二手房数据(终).csv：进一步清洗得到的数据

-DataPreprocessing目录：
	-datapreprocessing.py：对数据进行预处理（三大项）
	-广州链家二手房数据(三大项处理后).csv：三大项处理后的数据

-ModelTraining目录：
	-dataseeking.py：数据探索，对特征进行探索
	-featureengineering.py：特征工程
	-modelpipeline.py：构建模型流水线
	-rf_tuning.py：随机森林算法调优
	-randomforest.py：随机森林算法模型评估并保存
	-gb_tuning.py：梯度提升树算法调优
	-gradientboosting.py：梯度提升树算法模型评估并保存
	-modelfusion.py：融合模型并评估
	-best_random_forest_model.pkl：随机森林最优模型
	-best_gradient_boosting_model.pkl：梯度提升树最优模型
	-best_fusion_model.pkl：融合模型
	-experimentvisualization.py：一些实验可视化
	-模型数据.csv：特征工程后得到的数据
	-runlog：包含modelpipeline.py的运行日志
