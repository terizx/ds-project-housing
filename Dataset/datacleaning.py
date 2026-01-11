'''
目前数据存在的问题有：
1、需要将所有数据合并
2、数据以列表形式保存，需要删除字符
3、‘房源信息’字段中含有多个信息，需要拆解并保存为合适的字段
'''

# 处理爬取好广州的11个区的二手房源数据
import pandas as pd

# 数据路径
data_paths = [r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\tianhe.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\liwan.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\yuexiu.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\haizhu.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\baiyun.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\huangpugz.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\panyu.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\huadou.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\nansha.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\conghua.csv',
                r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\zengcheng.csv']

def data_process(data_path):
    data = pd.read_csv(data_path)
    columns = ['标题', '小区', '地区', '房源信息', '总价', '单价']
    # 处理无用的字符
    for column in columns:
        data[column] = data[column].str.replace("['", "").str.replace("']", "")
    # 处理房源信息字段，存在多个字段，进行分割（删除首尾的空格和换行，遇到'|'就分割开）
    houseinfo_columns = ['房屋户型', '建筑面积', '房屋朝向', '装修情况', '所在楼层', '建房时间', '建筑类型']
    houseinfo_data = []
    # 删除字段大于7的数据，大多都是别墅，没有分析的必要
    count = 0
    # data['房源信息']返回一个series，data[['房源信息']]返回一个dataframe
    for line in data['房源信息']:
        split_line = line.strip().split('|')
        if len(split_line) < 8:
            houseinfo_data.append(split_line)
        else:
            count += 1
    df = pd.DataFrame(houseinfo_data, columns=houseinfo_columns)
    result = pd.concat([data, df], axis=1) #按列合并
    final_result = result.drop(columns=['房源信息'], axis=1)
    print(f'共计删除了{count}条数据，请悉知！')
    return final_result, count

regions = ['天河区','荔湾区','越秀区','海珠区','白云区','黄埔区','番禺区','花都区','南沙区','从化区','增城区']
# 正常执行：天河区、荔湾区、越秀区、海珠区、白云区、黄埔区、番禺区、花都区
# 非正常执行：南沙区、从化区、增城区(房源信息存在八个字段，主要是多了一个房屋类型，多出来的都是清一色的别墅)
# 合并所有区的数据
all_house_data = pd.DataFrame()
csv_file_path = './广州市链家二手房数据(初).csv'
drop_count = 0
for region, data_path in zip(regions, data_paths):
    print(f'正在处理{region}的数据，请等待。。。')
    data, count = data_process(data_path)
    print(f'处理完成{region}的数据！')
    print('------------------------------------------------')
    drop_count += count
    all_house_data = pd.concat([all_house_data, data], axis=0) #按行合并
    all_house_data.to_csv(csv_file_path, index=False)
print(f'总共去除了{drop_count}条脏数据！')
