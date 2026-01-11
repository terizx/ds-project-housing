# 缺失值、重复值、异常值处理
'''
一、缺失值处理：
（√）1、'房屋户型', '建筑面积', '房屋朝向', '装修情况', '所在楼层', '建房时间', '建筑类型'六个字段，共计24条记录是没有数据，直接删去
（√）2、‘建筑类型’还剩827条记录没有数据，使用众数‘塔楼’填充；
二、重复值处理：
（√）1、删除所有字段重复的记录，仅保留第一条数据
三、异常值处理（将所有数据处理规整）：
（√）1、'所在楼层'：存在很多没有表明中高低楼层的人，只写了几层；人为定义为{0-10层：‘低楼层’，11-20层:‘中楼层’，21以上：‘高楼层’}
（√）2、'建房时间':共计7640条记录是‘暂无数据’；由于缺失数量过大，使用基于概率分布的随机抽样填充；
（√）3、'建筑类型':共计197条记录是‘暂无数据’，全部使用众数‘塔楼’填充；
'''
import numpy as np
import pandas as pd
import re

data_path = 'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\广州市链家二手房数据(终).csv'
data = pd.read_csv(data_path)
print(f'三大项处理前：共{len(data)}条数据')
house_columns = ['标题', '小区', '地区', '总价', '单价', '所在区', '房屋户型', '建筑面积', '房屋朝向', '装修情况', '所在楼层', '建房时间', '建筑类型']

# 查看缺失值，删除'房屋户型'包含缺失值的行（24条）
data = data.dropna(axis=0, subset=['房屋户型'])
# 填充‘建筑类型’为nan的827条记录，用众数‘塔楼’填充
data['建筑类型'] = data['建筑类型'].fillna('塔楼')
print(f'缺失值处理后：共计{len(data)}条数据')

# 查看重复值，仅保留第一条数据，删除32959-25261=7698
data = data.drop_duplicates(keep='first')
print(f'重复值处理后：共计{len(data)}条数据')

# 查看异常值，处理'所在楼层'字段：（要先把‘所在楼层’列的数据取前3个字符，然后再进行匹配）
data['所在楼层'] = data['所在楼层'].str[:3]
def categorize_floor(floor_str):
    match = re.search(r'(\d+)',floor_str)
    # 如果找到了数字
    if match:
        # group(1):匹配到第一个分组的结果
        floor = int(match.group(1))
        if 0 <= floor <= 10:
            return '低楼层'
        elif 10 <= floor <= 20:
            return '中楼层'
        elif 20 < floor:
            return '高楼层'
    # 如果没有数字，返回原字符
    else:
        return floor_str
data['所在楼层'] = data['所在楼层'].apply(categorize_floor)

# 处理'建房时间'
# 1. 计算每个年份出现的概率
data_filtered = data[data['建房时间'] != '暂无数据']  # 先删除 '暂无数据'
value_counts = data_filtered['建房时间'].value_counts(normalize=True)
valid_years = value_counts.index.tolist()
probabilities = value_counts.values
# 2. 使用该分布对缺失值进行随机填充，并设置随机种子，保证数据的重复性
np.random.seed(42)
if '暂无数据' in data['建房时间'].values:
    mask = data['建房时间'] == '暂无数据'
    data.loc[mask, '建房时间'] = np.random.choice(valid_years, size=mask.sum(), p=probabilities)

# 处理'建筑类型'
data.loc[data['建筑类型'] == '暂无数据','建筑类型'] = '塔楼'
data.to_csv('./广州链家二手房数据(三大项处理后).csv', index=False)
print(f'异常值处理后：共计{len(data)}条数据')

