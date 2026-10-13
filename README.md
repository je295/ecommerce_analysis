# 电商销售数据分析平台

> 基于 MySQL + Python + Power BI 的电商数据分析项目

## 📋 项目简介

基于模拟电商平台销售数据，从**数据建模、ETL 加工、RFM 客户分层到可视化分析**全流程独立完成，为业务方提供可执行的运营建议。

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| 存储 | MySQL 8.0 |
| 处理 | Python（pandas、SQLAlchemy、Faker）|
| 可视化 | Power BI Desktop |

## 📊 数据规模

- **原始订单**：5,000 笔
- **有效订单明细**：17,060 条
- **客户数**：977 人
- **商品数**：200 个
- **数据完整率**：85% → 100%

## ✨ 项目亮点

1. **完整 ETL 流程**：从 MySQL 抽取 → Python 清洗 → 写回宽表
2. **特征工程**：从原始时间字段派生 6 个维度（年/月/季/周/时/年月）
3. **RFM 客户分层**：5 类客户，展示二八法则
4. **帕累托分析**：验证 Top 10 商品贡献 30% 营收
5. **Power BI 4 个分析页面**

## 📈 分析结论

- **总营收**：5,142.85 万元
- **利润率**：37.5%（高于行业均值）
- **客单价**：1.21 万元
- **重要价值客户**：187 人（19.1%），贡献近半营收
- **高价值流失客户**：86 人（8.8%），需优先召回

## 📂 项目文件

| 文件 | 说明 |
|------|------|
| `ecommerce_analysis.py` | 数据生成脚本 |
| `etl.py` | ETL 数据清洗脚本 |
| `sales_fact.py` | 宽表生成脚本 |
| `ecommerce_analysis_sales_fact.sql` | 宽表结构 |
| `ecommerce_analysis_rfm_segments.sql` | RFM 分层表结构 |
| `ecommerce_analysis.pbix` | Power BI 仪表板 |

## 🚀 使用方法

### 1. 建库建表
```bash
mysql -u root -p < ecommerce_analysis_create_tables.sql
```

### 2. 生成数据 + ETL 清洗
```bash
python ecommerce_analysis.py
python etl.py
python sales_fact.py
```

### 3. 打开 Power BI
用 Power BI Desktop 打开 `ecommerce_analysis.pbix`



