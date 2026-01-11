import os
import joblib
import pandas as pd
import numpy as np

# ==================== 编码映射字典（方便理解和使用）====================
# 所在区编码（按GDP排序）
DISTRICT_CODE = {
    '从化区': 0, '荔湾区': 1, '增城区': 2, '花都区': 3, '南沙区': 4,
    '海珠区': 5, '番禺区': 6, '白云区': 7, '越秀区': 8, '黄埔区': 9, '天河区': 10
}

# 房屋朝向编码（朝向越好，标签越大）
ORIENTATION_CODE = {
    '西北': 0, '北': 1, '西南': 2, '西': 3, '东北': 4, '东': 5, '东南': 6, '南': 7
}

# 装修情况编码
DECORATION_CODE = {
    '其他': 0, '毛坯': 1, '简装': 2, '精装': 3
}

# 所在楼层编码
FLOOR_CODE = {
    '地下室': 0, '低楼层': 1, '中楼层': 2, '高楼层': 3
}

# 建筑类型编码
BUILDING_TYPE_CODE = {
    '平房': 0, '板楼': 1, '板塔结合': 2, '塔楼': 3, '联排别墅': 4, '独栋别墅': 5
}

# ==================== 加载模型 ====================
def load_model():
    """加载训练好的模型"""
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'final_best_model.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}\n请先运行 train_random_forest.py 训练模型")
    
    model = joblib.load(model_path)
    print("✅ 模型加载成功！")
    return model

# ==================== 预测函数 ====================
def predict_price(model, 所在区, 房屋户型, 建筑面积, 房屋朝向, 装修情况, 
                  所在楼层, 建筑类型, 建房时长):
    """
    预测房屋价格
    
    参数说明：
    - 所在区: 区名（如'天河区'）或编码（0-10）
    - 房屋户型: 室+厅的总数（如3室2厅=5）
    - 建筑面积: 平方米（浮点数）
    - 房屋朝向: 朝向名称（如'南'）或编码（0-7）
    - 装修情况: 装修类型（如'精装'）或编码（0-3）
    - 所在楼层: 楼层类型（如'中楼层'）或编码（0-3）
    - 建筑类型: 建筑类型（如'塔楼'）或编码（0-5）
    - 建房时长: 房屋年龄（年数，整数）
    """
    # 转换字符串编码为数字
    if isinstance(所在区, str):
        所在区 = DISTRICT_CODE.get(所在区, 所在区)
    if isinstance(房屋朝向, str):
        房屋朝向 = ORIENTATION_CODE.get(房屋朝向, 房屋朝向)
    if isinstance(装修情况, str):
        装修情况 = DECORATION_CODE.get(装修情况, 装修情况)
    if isinstance(所在楼层, str):
        所在楼层 = FLOOR_CODE.get(所在楼层, 所在楼层)
    if isinstance(建筑类型, str):
        建筑类型 = BUILDING_TYPE_CODE.get(建筑类型, 建筑类型)
    
    # 构建特征DataFrame（必须与训练时的特征顺序一致）
    features = pd.DataFrame([{
        '所在区': 所在区,
        '房屋户型': 房屋户型,
        '建筑面积': 建筑面积,
        '房屋朝向': 房屋朝向,
        '装修情况': 装修情况,
        '所在楼层': 所在楼层,
        '建筑类型': 建筑类型,
        '建房时长': 建房时长
    }])
    
    # 预测
    predicted_price = model.predict(features)[0]
    return predicted_price

# ==================== 格式化输出 ====================
def format_output(所在区, 房屋户型, 建筑面积, 房屋朝向, 装修情况, 
                  所在楼层, 建筑类型, 建房时长, predicted_price):
    """格式化输出预测结果"""
    print("\n" + "=" * 50)
    print("🏠 房屋估价结果")
    print("=" * 50)
    print(f"📍 所在区:     {所在区}")
    print(f"🏘️  房屋户型:   {房屋户型}室（室+厅总数）")
    print(f"📐 建筑面积:   {建筑面积} 平方米")
    print(f"🧭 房屋朝向:   {房屋朝向}")
    print(f"🔨 装修情况:   {装修情况}")
    print(f"🏢 所在楼层:   {所在楼层}")
    print(f"🏗️  建筑类型:   {建筑类型}")
    print(f"⏰ 建房时长:   {建房时长} 年")
    print("-" * 50)
    print(f"💰 AI估价:     {predicted_price:.2f} 万元")
    print("=" * 50 + "\n")

# ==================== 主函数 ====================
def main():
    """主函数：演示如何使用模型进行预测"""
    # 加载模型
    model = load_model()
    
    print("\n" + "=" * 50)
    print("开始房屋价格预测...")
    print("=" * 50)
    
    # ========== 示例1：天河区精装房 ==========
    print("\n【示例1】天河区精装房")
    predicted_price = predict_price(
        model=model,
        所在区='天河区',          # 或直接使用 10
        房屋户型=5,               # 3室2厅 = 5
        建筑面积=100.5,
        房屋朝向='南',            # 或直接使用 7
        装修情况='精装',          # 或直接使用 3
        所在楼层='中楼层',        # 或直接使用 2
        建筑类型='塔楼',          # 或直接使用 3
        建房时长=5                # 5年新楼
    )
    format_output('天河区', 5, 100.5, '南', '精装', '中楼层', '塔楼', 5, predicted_price)
    
    # ========== 示例2：越秀区简装房 ==========
    print("\n【示例2】越秀区简装房")
    predicted_price = predict_price(
        model=model,
        所在区=8,                 # 越秀区
        房屋户型=4,               # 2室2厅 = 4
        建筑面积=80.0,
        房屋朝向=6,               # 东南
        装修情况=2,               # 简装
        所在楼层=3,               # 高楼层
        建筑类型=1,               # 板楼
        建房时长=10               # 10年房龄
    )
    format_output('越秀区', 4, 80.0, '东南', '简装', '高楼层', '板楼', 10, predicted_price)
    
    # ========== 示例3：海珠区毛坯房 ==========
    print("\n【示例3】海珠区毛坯房")
    predicted_price = predict_price(
        model=model,
        所在区='海珠区',
        房屋户型=6,               # 4室2厅 = 6
        建筑面积=120.0,
        房屋朝向='东',
        装修情况='毛坯',
        所在楼层='低楼层',
        建筑类型='板塔结合',
        建房时长=2                # 2年新楼
    )
    format_output('海珠区', 6, 120.0, '东', '毛坯', '低楼层', '板塔结合', 2, predicted_price)

if __name__ == '__main__':
    main()
