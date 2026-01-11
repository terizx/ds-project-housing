import os
import time
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# 日志配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

def main():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, '..', 'model_data.csv')
    data_path = os.path.abspath(data_path)

    # 读取数据
    data = pd.read_csv(data_path)
    X = data.drop(columns=['总价'], axis=1)
    y = data['总价']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 先测试默认参数的性能
    logger.info('Testing default parameters...')
    default_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(random_state=42, n_estimators=100))
    ])
    default_pipeline.fit(X_train, y_train)
    default_pred = default_pipeline.predict(X_test)
    default_rmse = np.sqrt(mean_squared_error(y_test, default_pred))
    logger.info(f'Default parameters Test RMSE: {default_rmse:.4f}')
    print(f'Default parameters Test RMSE: {default_rmse:.4f}')

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(random_state=42))
    ])

    # 使用 RandomizedSearchCV 进行快速参数搜索（比GridSearchCV快很多）
    param_distributions = {
        'model__n_estimators': [50, 100, 150],
        'model__max_depth': [None, 15, 20],
        'model__min_samples_split': [2, 5],
        'model__min_samples_leaf': [1, 2],
        'model__max_features': [None, 0.5, 'sqrt']
    }

    logger.info('Starting RandomizedSearchCV for RandomForest...')
    start = time.time()
    # 使用 RandomizedSearchCV，只搜索20个随机组合，2折交叉验证
    random_search = RandomizedSearchCV(
        pipeline, 
        param_distributions=param_distributions, 
        n_iter=20,  # 只尝试20个随机参数组合（而不是全部32个）
        cv=2,  # 减少交叉验证折数从3到2
        scoring='neg_root_mean_squared_error',
        n_jobs=-1, 
        verbose=1,
        random_state=42
    )
    random_search.fit(X_train, y_train)
    elapsed = time.time() - start
    logger.info(f'RandomizedSearchCV finished in {elapsed:.2f}s')

    best_params = random_search.best_params_
    logger.info(f'Random search best params: {best_params}')

    # 在测试集上评估最佳搜索结果
    best_pipeline = random_search.best_estimator_
    y_pred = best_pipeline.predict(X_test)
    tuned_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logger.info(f'Random search best model Test RMSE: {tuned_rmse:.4f}')
    print(f'Random search best model Test RMSE: {tuned_rmse:.4f}')

    # 比较默认参数和调参结果，选择更好的
    if default_rmse <= tuned_rmse:
        logger.info(f'Default parameters are better! Using default parameters for final model.')
        print(f'Default parameters are better! Using default parameters for final model.')
        # 使用默认参数
        est_params = {
            'n_estimators': 100,
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'max_features': 'sqrt'
        }
    else:
        logger.info(f'Tuned parameters are better! Using tuned parameters for final model.')
        print(f'Tuned parameters are better! Using tuned parameters for final model.')
        # 把 random_search.best_params_ 从 'model__param' 转换为 estimator 参数
        est_params = {}
        for k, v in best_params.items():
            if k.startswith('model__'):
                est_params[k.split('__', 1)[1]] = v
        # 保持搜索到的最佳 n_estimators，不强制改为200
        if 'n_estimators' not in est_params:
            est_params['n_estimators'] = 100

    # 用最佳参数在整个数据集上重训练，并保存最终模型
    final_rf = RandomForestRegressor(random_state=42, **est_params)
    final_pipeline = Pipeline([('scaler', StandardScaler()), ('model', final_rf)])
    final_pipeline.fit(X, y)

    out_path = os.path.join(base_dir, 'final_best_model.pkl')
    joblib.dump(final_pipeline, out_path)
    logger.info(f'Final best model (refit on full data) saved to {out_path}')
    print(f'Final best model saved to {out_path}')

    # 保存最佳参数到文件
    params_path = os.path.join(base_dir, 'final_best_model_params.json')
    try:
        import json
        with open(params_path, 'w', encoding='utf-8') as f:
            json.dump(est_params, f, ensure_ascii=False, indent=2)
        logger.info(f'Best params saved to {params_path}')
    except Exception:
        logger.exception('Failed to save best params')


if __name__ == '__main__':
    main()
