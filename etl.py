import pandas as pd
from sqlalchemy import create_engine,text
from urllib.parse import quote_plus

#连接数据库
pwd = quote_plus('123456')
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/ecommerce_analysis?charset=utf8',pool_pre_ping=True)

#从MySQL里面读取四张表，join数据
QUERY = """
SELECT
    o.order_id,o.order_date,o.status,
    c.customer_id,c.customer_name,c.gender,c.age,c.city,
    p.product_id,p.product_name,p.category,p.price,p.cost,
    oi.quantity,oi.unit_price,
    oi.quantity * oi.unit_price as revenue,
    oi.quantity * (oi.unit_price - p.cost) as profit
FROM orders o
JOIN order_items oi on o.order_id = oi.order_id
left join  customers c on c.customer_id = o.customer_id
JOIN products p on oi.product_id = p.product_id
WHERE o.status = 'completed'
"""

def extract ():
    print(">>>抽取数据...")
    with engine.connect() as conn:
        df = pd.read_sql(text(QUERY),conn)
        print(f"    原始记录:{len(df)}")
        return df

def transform (df):
    print(">>>转换数据...")
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['quarter'] = df['order_date'].dt.quarter
    df['hour'] = df['order_date'].dt.hour
    df['weekday'] = df['order_date'].dt.weekday
    df['year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['age_group'] = pd.cut(df['age'],
                             bins=[0,25,35,45,55,100],
                             labels=['18-25','26-35','35-45','45-55','55+'])
    print(f"    转换后:{len(df)}行,{df.shape[1]}列")
    return df

def load (df):
    print(">>>写入sales_fact表...")
    df.to_sql('sales_fact',con=engine,if_exists='replace',index=False)
    print(" 完成")

if __name__ == "__main__":
    df = extract()
    df = transform(df)
    load(df)
    print(">>>ETL完成")

