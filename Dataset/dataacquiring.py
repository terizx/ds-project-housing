# 爬取链家二手房（广州地区）数据
# 为了抓取尽可能多的数据，分别抓取广州11个区的前100页的数据
import pandas as pd # 数据存储
import requests # 网页内容获取
from lxml import etree # 解析数据
import random
import time # 反反爬
from fastprogress import master_bar,progress_bar # 进度条显示

# 目标网站的URL、请求头(包括UA和cookie)
# url = 'https://gz.lianjia.com/ershoufang/tianhe/'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#            'Cookie':'SECKEY_ABVK=7ijNmZBhKKTNL05wX3fWQwp3/P+BXGV+PxcUqq1IybE%3D; BMAP_SECKEY=pm_zu3O3PvVXFELewPdmq-Vl1Nmjjw3NqNCzxjVSxBTE4ccGKXSAiNqXSObh2ca0_07DlRAei4udQ2NTqM1AKvj9ljjTJLKmifqS9USX_G8vkYqrqBp_FMlL5mTMJ0ivCy275hxthVH0sQFC2SE97si8CwEk34uYDhSPeXfE_oLpa72zAoQPJqmX83f0XJIM; _ga=GA1.2.1638032737.1733414490; crosSdkDT2019DeviceId=bqxshf-sbyxd0-51sw1hnyb7hw9rf-0umyvglwd; lianjia_uuid=edf551af-4d98-4a10-bb5b-035f5b31e120; login_ucid=2000000458166819; lianjia_token=2.001222017445e87ebb038f28457f8e4b15; lianjia_token_secure=2.001222017445e87ebb038f28457f8e4b15; security_ticket=ZzDXAx0r7eBJUn73umKpBNP474ks8UQH+KEMwP7J+I5c4XmANd3LvCohTV9v88YZcC1grNJDTb5qhjl/enHphEAwjHojw4nKNfEfe5vDVtu3IdhqL0R0f3skOYrpGRHskcA9SVE4sJ9N8nJlle2i3+EgV/5RiB9KAQTMLYiK744=; ftkrc_=4a6377ed-25f8-4c20-8e4a-ae2159a56202; lfrc_=d5a0a964-f732-4617-a04d-42ba03eb2762; _jzqx=1.1733662121.1733816987.4.jzqsr=gz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=localhost:8888|jzqct=/; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1733414475,1734074443; HMACCOUNT=F148A6E4C02CC6BB; _jzqc=1; _qzjc=1; _gid=GA1.2.681842018.1734074456; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218176271e98939-0f92f5efc96572-57432b14-1327104-18176271e99699%22%2C%22%24device_id%22%3A%2218176271e98939-0f92f5efc96572-57432b14-1327104-18176271e99699%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%E4%BA%8C%E6%89%8B%E6%88%BF%E7%BD%91%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wygz%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1734160138; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1734160138; select_city=440100; _jzqckmp=1; digv_extends=%7B%22utmTrackId%22%3A%2221583074%22%7D; _jzqa=1.3235552081233446400.1733414476.1734163408.1734165251.13; _jzqy=1.1733414476.1734165251.3.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E4%BA%8C%E6%89%8B%E6%88%BF%E7%BD%91; lianjia_ssid=33d7729f-d5da-4bc9-a1b1-b63a96042f0c; _qzja=1.1482741718.1733414476145.1734163408479.1734165251333.1734166199890.1734166335370.0.0.0.42.13; _qzjb=1.1734165251333.9.0.0.0; _qzjto=21.3.0; _jzqb=1.9.10.1734165251.1; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1734166336; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMTQ4OGI3NGFmYzE4YzAxMTE0ZjFmMzZmZDRlYWFlZWFjZTIyMDYyMTg2MjEyODNmNDc4NmRjZTNiYWM0MThhNjNhMjVlYjQ1MjQyZTg5NTIyMzhmNWNmNzM5MjUyMGU4NjIzNzBkNzY4ZmYxYTk5ODBiNWMwNTM4Y2VjYzY4NDJhNzJjYzU0OTE4OGFkMjFkZTI0OTNkMjNjNmQ3M2EzYWRkN2RiNjI5OGY3Yjc5MWQ5NzU3MDVkODk2ODliODIwMjM0MmMwMDM5NTFhNTlmZGRiYTllNzliYmZhZmRjMjNmYmU5OGE2MDYyYjZmODM0MTllMThjMTk5NzkwMzNiOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiMzdlOTZlNVwifSIsInIiOiJodHRwczovL2d6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvdGlhbmhlLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9; _ga_654P0WDKYN=GS1.2.1734165262.13.1.1734166346.0.0.0'}

# 检查请求是否成功
# if response.status_code == 200:
#     print('respone success!')

# print(response.text) # 确认含有内容了，开始爬取

# 获取网页内容
def get_html_content(url,headers):
    response = requests.get(url, headers=headers)
    return response.text

# 爬取每一列信息，验证是否能抓取到数据
# def get_title(res_text):
#     res_text = etree.HTML(res_text)
#     title = res_text.xpath("//div[@class='title']/a/text()")
#     return dict(zip(['标题'], [title]))
#
# def get_position_info_xaioqu(res_text):
#     res_text = etree.HTML(res_text)
#     position_info_xaioqu = res_text.xpath("//div[@class='positionInfo']//a[1]/text()")
#     return dict(zip(['小区'], [position_info_xaioqu]))
#
# def get_position_info_quyu(res_text):
#     res_text = etree.HTML(res_text)
#     position_info_quyu = res_text.xpath("//div[@class='positionInfo']//a[2]/text()")
#     return dict(zip(['区域'], [position_info_quyu]))
#
# def get_house_info(res_text):
#     res_text = etree.HTML(res_text)
#     house_info = res_text.xpath("//div[@class='houseInfo']/text()")
#     return dict(zip(['房源信息'], [house_info]))
#
# def get_total_price(res_text):
#     res_text = etree.HTML(res_text)
#     total_price = res_text.xpath("//div[@class='totalPrice totalPrice2']/span/text()")
#     return dict(zip(['总价'], total_price))
#
# def get_unit_price(res_text):
#     res_text = etree.HTML(res_text)
#     unit_price = res_text.xpath("//div[@class='unitPrice']/span/text()")
#     return dict(zip(['单价（元/平米）'], unit_price))

# 爬取每一页数据
def process_per_page(url):
    data = []
    title = ''
    position_info_xaioqu = ''
    position_info_quyu = ''
    house_info = ''
    total_price = ''
    unit_price = ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': 'SECKEY_ABVK=7ijNmZBhKKTNL05wX3fWQwp3/P+BXGV+PxcUqq1IybE%3D; BMAP_SECKEY=pm_zu3O3PvVXFELewPdmq-Vl1Nmjjw3NqNCzxjVSxBTE4ccGKXSAiNqXSObh2ca0_07DlRAei4udQ2NTqM1AKvj9ljjTJLKmifqS9USX_G8vkYqrqBp_FMlL5mTMJ0ivCy275hxthVH0sQFC2SE97si8CwEk34uYDhSPeXfE_oLpa72zAoQPJqmX83f0XJIM; _ga=GA1.2.1638032737.1733414490; crosSdkDT2019DeviceId=bqxshf-sbyxd0-51sw1hnyb7hw9rf-0umyvglwd; lianjia_uuid=edf551af-4d98-4a10-bb5b-035f5b31e120; login_ucid=2000000458166819; lianjia_token=2.001222017445e87ebb038f28457f8e4b15; lianjia_token_secure=2.001222017445e87ebb038f28457f8e4b15; security_ticket=ZzDXAx0r7eBJUn73umKpBNP474ks8UQH+KEMwP7J+I5c4XmANd3LvCohTV9v88YZcC1grNJDTb5qhjl/enHphEAwjHojw4nKNfEfe5vDVtu3IdhqL0R0f3skOYrpGRHskcA9SVE4sJ9N8nJlle2i3+EgV/5RiB9KAQTMLYiK744=; ftkrc_=4a6377ed-25f8-4c20-8e4a-ae2159a56202; lfrc_=d5a0a964-f732-4617-a04d-42ba03eb2762; _jzqx=1.1733662121.1733816987.4.jzqsr=gz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=localhost:8888|jzqct=/; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1733414475,1734074443; HMACCOUNT=F148A6E4C02CC6BB; _jzqc=1; _qzjc=1; _gid=GA1.2.681842018.1734074456; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218176271e98939-0f92f5efc96572-57432b14-1327104-18176271e99699%22%2C%22%24device_id%22%3A%2218176271e98939-0f92f5efc96572-57432b14-1327104-18176271e99699%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%E4%BA%8C%E6%89%8B%E6%88%BF%E7%BD%91%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wygz%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1734160138; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1734160138; select_city=440100; _jzqckmp=1; digv_extends=%7B%22utmTrackId%22%3A%2221583074%22%7D; _jzqa=1.3235552081233446400.1733414476.1734163408.1734165251.13; _jzqy=1.1733414476.1734165251.3.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E4%BA%8C%E6%89%8B%E6%88%BF%E7%BD%91; lianjia_ssid=33d7729f-d5da-4bc9-a1b1-b63a96042f0c; _qzja=1.1482741718.1733414476145.1734163408479.1734165251333.1734166199890.1734166335370.0.0.0.42.13; _qzjb=1.1734165251333.9.0.0.0; _qzjto=21.3.0; _jzqb=1.9.10.1734165251.1; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1734166336; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMTQ4OGI3NGFmYzE4YzAxMTE0ZjFmMzZmZDRlYWFlZWFjZTIyMDYyMTg2MjEyODNmNDc4NmRjZTNiYWM0MThhNjNhMjVlYjQ1MjQyZTg5NTIyMzhmNWNmNzM5MjUyMGU4NjIzNzBkNzY4ZmYxYTk5ODBiNWMwNTM4Y2VjYzY4NDJhNzJjYzU0OTE4OGFkMjFkZTI0OTNkMjNjNmQ3M2EzYWRkN2RiNjI5OGY3Yjc5MWQ5NzU3MDVkODk2ODliODIwMjM0MmMwMDM5NTFhNTlmZGRiYTllNzliYmZhZmRjMjNmYmU5OGE2MDYyYjZmODM0MTllMThjMTk5NzkwMzNiOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiMzdlOTZlNVwifSIsInIiOiJodHRwczovL2d6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvdGlhbmhlLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9; _ga_654P0WDKYN=GS1.2.1734165262.13.1.1734166346.0.0.0'
    }
    html_content = get_html_content(url, headers)
    res_text = etree.HTML(html_content)
    divs_info = res_text.xpath('//div[@class="info clear"]')
    # 要注意不能使用//，否则会一次抓取多个数据,而且一定要加“./”
    for div in divs_info:
        title = div.xpath("./div[@class='title']/a/text()")
        position_info_xaioqu = div.xpath("./div[@class='flood']/div[@class='positionInfo']//a[1]/text()")
        position_info_quyu = div.xpath("./div[@class='flood']/div[@class='positionInfo']//a[2]/text()")
        house_info = div.xpath("./div[@class='address']/div[@class='houseInfo']/text()")
        total_price = div.xpath("./div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span/text()")
        unit_price = div.xpath("./div[@class='priceInfo']/div[@class='unitPrice']/span/text()")

        data.append({'标题':title, '小区':position_info_xaioqu, '地区':position_info_quyu,
                     '房源信息':house_info, '总价':total_price, '单价':unit_price})

    house_df = pd.DataFrame(data)
    return house_df

# 一次抓取多页数据(存为dataframe格式)，为了防止被检测出来，每采集5页，随机停止一段时间
def process_all_page(region, page_numbers, base_url):
    print(f'正在爬取{region}的二手房源数据，请等候：')
    all_data = pd.DataFrame()
    for page in range(1, page_numbers+1):
        sleep_time = random.randint(2,5)
        if page % 5 == 0:
            time.sleep(sleep_time)
        if page % 10 == 0:
            print(f'正在爬取第{page}页/共100页。。。。。')
        url = f'{base_url}pg{page}/'
        page_data = process_per_page(url)
        all_data = pd.concat([all_data, page_data], ignore_index=True)
    return all_data

# 将爬取的数据保存到CSV中，并且加一列数据为所对应的区，包含11个区，
# '天河区','荔湾区','越秀区','海珠区','白云区','黄埔区','番禺区','花都区','南沙区','从化区','增城区’
def dataframe_to_csv(region, all_data, csv_file_path):
    # 直接加一列全部数据为'region'的'所在区'列
    print(f'正在保存{region}的数据')
    all_data = all_data.assign(所在区=region)
    all_data.to_csv(csv_file_path, index=False)
    print(f'保存{region}的数据成功！')

regions = ['天河区','荔湾区','越秀区','海珠区','白云区','黄埔区','番禺区','花都区','南沙区','从化区','增城区']
base_urls = ['https://gz.lianjia.com/ershoufang/tianhe/',
            'https://gz.lianjia.com/ershoufang/liwan/',
            'https://gz.lianjia.com/ershoufang/yuexiu/',
            'https://gz.lianjia.com/ershoufang/haizhu/',
            'https://gz.lianjia.com/ershoufang/baiyun/',
            'https://gz.lianjia.com/ershoufang/huangpugz/',
            'https://gz.lianjia.com/ershoufang/panyu/',
            'https://gz.lianjia.com/ershoufang/huadou/',
            'https://gz.lianjia.com/ershoufang/nansha/',
            'https://gz.lianjia.com/ershoufang/conghua/',
            'https://gz.lianjia.com/ershoufang/zengcheng/']

csv_file_paths = [r'D:\pycharm\pycharm_projects\Machine-Learning-Work\Dataset\tianhe.csv',
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

# 爬取页数、所在区、所在区网址、保存路径
page_numbers = 100
for region, base_url, csv_file_path in zip(regions, base_urls, csv_file_paths):
    all_data = process_all_page(region, page_numbers, base_url)
    dataframe_to_csv(region, all_data, csv_file_path)





