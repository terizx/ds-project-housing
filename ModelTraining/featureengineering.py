# 准备好模型训练所需要的数据（全部数据都进行好编码）
import numpy as np
import pandas as pd
import re

data_path = r'D:\pycharm\pycharm_projects\Machine-Learning-Work\DataPreprocessing\广州链家二手房数据(三大项处理后).csv'
data = pd.read_csv(data_path)

house_columns = ['标题', '小区', '地区', '总价', '单价', '所在区', '房屋户型', '建筑面积', '房屋朝向', '装修情况', '所在楼层', '建房时间', '建筑类型']

# 去除标题、单价（总价=单价*面积）、小区和地区（包含在所在区里面了，不考虑）
df = pd.DataFrame(data[['总价', '所在区', '房屋户型', '建筑面积', '房屋朝向', '装修情况', '所在楼层', '建房时间', '建筑类型']])

# 所在区（按广州2023年GDP情况来排，GDP指数越高，标签越大，从0-11依次排序）
# 从化区：0，荔湾区：1，增城区：2，花都区：3，南沙区：4，海珠区：5，番禺区：6，白云区：7，越秀区：8，黄埔区：9，天河区：10；
diqu_code = {
    '从化区': 0,
    '荔湾区': 1,
    '增城区': 2,
    '花都区': 3,
    '南沙区': 4,
    '海珠区': 5,
    '番禺区': 6,
    '白云区': 7,
    '越秀区': 8,
    '黄埔区': 9,
    '天河区': 10
}
df['所在区'] = df['所在区'].map(diqu_code)

# 房屋户型（多少室多少厅加起来的数字作为编码）
def sum_rooms(rooms):
    # 找到所有数字,返回一个列表
    numbers = re.findall(r'\d+', rooms)
    if len(numbers) == 2:
        rooms = int(numbers[0]) + int(numbers[1])
        return rooms
    else:
        return None
df['房屋户型'] = df['房屋户型'].apply(sum_rooms)

# 建筑面积（152.32平米 -> 152.32）
def sum_areas(mianji):
    match = re.search(r'(\d+(?:\.\d+)?)', mianji)
    # 如果找到了数字
    if match:
        # group(1):匹配到第一个分组的结果
        area = float(match.group(1))
        return area
df['建筑面积'] = df['建筑面积'].apply(sum_areas)

# 房屋朝向（南 西南 -> 南），依据大家通俗的说法来编码，取前两个字符，并查找每一行的前后是否有空格(否则分类会有问题)，然后进行编码
# 这里有(南、东南、北、东、东北、西南、西北、西)，接下来按传统风水学来排序，朝向越好，标签越大
# 西北：0，北：1，西南：2，西：3，东北：4，东：5，东南：6，南：7；
df['房屋朝向'] = df['房屋朝向'].str[:2].str.strip()
chaoxiang_code = {
    '西北': 0,
    '北': 1,
    '西南': 2,
    '西': 3,
    '东北': 4,
    '东': 5,
    '东南': 6,
    '南': 7
}
df['房屋朝向'] = df['房屋朝向'].map(chaoxiang_code)

# 装修情况（其他：0，毛坯：1，简装：2，精装：3；）
zhuangxiu_code = {
    '其他': 0,
    '毛坯': 1,
    '简装': 2,
    '精装': 3
}
df['装修情况'] = df['装修情况'].map(zhuangxiu_code)

# 所在楼层（地下室：0，低楼层：1，中楼层：2，高楼层：3；）
louceng_code = {
    '地下室': 0,
    '低楼层': 1,
    '中楼层': 2,
    '高楼层': 3
}
df['所在楼层'] = df['所在楼层'].map(louceng_code)

# 建房时间（2004年 -> 2004），为了减少量纲之间的差异，将其改为‘建房时长’：定义为（2024-“建房时间”=“建房时长”）
df['建房时间'] = df['建房时间'].str.extract(r'(\d{4})年')[0].astype(int)
df['建房时长'] = 2024 - df['建房时间']
df = df.drop('建房时间', axis=1)

# 建筑类型（平房：0，板楼：1，板塔结合：2，塔楼：3，联排别墅：4，独栋别墅：5）
jianzhu_code = {
    '平房': 0,
    '板楼': 1,
    '板塔结合': 2,
    '塔楼': 3,
    '联排别墅': 4,
    '独栋别墅': 5,
}
df['建筑类型'] = df['建筑类型'].map(jianzhu_code)

df.to_csv('./模型数据.csv', index=False)
