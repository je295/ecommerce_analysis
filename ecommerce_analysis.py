#生成数据 + Faker
import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine,text
from datetime import datetime,timedelta
#创建实例
faker = Faker('zh-CN') #zh-CN生成中文名字，城市

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/ecommerce_analysis?charset=utf8')

with engine.connect() as conn:
    conn.execute(text("drop table if exists order_items"))
    conn.execute(text("drop table if exists orders"))
    conn.execute(text("drop table if exists products"))
    conn.execute(text("drop table if exists customers"))
    conn.commit()
#生成客户数据
customers = []
for i in range(1,1001):
    customers.append({
        'customer_id':i,
        'customer_name': faker.name(),
        'gender': random.choice(['M', 'F']),
        'age': random.randint(18, 65),
        'city':faker.city(),
        'register_date':faker.date_between(start_date='-2y', end_date='today')
    })

#生成产品数据
categories = ['电子产品','服装','家居','食品','美妆']
products = []
for i in range(1,201):
    price = round(random.uniform(20,2000),2)
    products.append({
        'product_id':i,
        'product_name':f'{random.choice(categories)},-{i:03d}',
        'category':random.choice(categories),
        'price':price,
        'cost':round(price * random.uniform(0.4,0.7),2)
    })
#
orders,order_items = [],[]
for order_id   in range(1,5001):
    cust_id = random.randint(1,1000)
    order_date = faker.date_time_between(start_date='-1y', end_date='now')
    status=random.choices(['completed','cancelled','returned'],weights=[0.85,0.08,0.07])[0]
    orders.append({
        'order_id':order_id,
        'customer_id':cust_id,
        'order_date':order_date,
        'status':status,
    })
    for _ in range(1,5):
        pid = random.randint(1,200)
        order_items.append({
            'order_id':order_id,
            'product_id':pid,
            'quantity':random.randint(1,5),
            'unit_price':round(random.uniform(20,2000),2),
        })
pd.DataFrame(customers).to_sql('customers', engine, index=False, if_exists='append')
pd.DataFrame(products).to_sql('products', engine, index=False, if_exists='append')
pd.DataFrame(orders).to_sql('orders', engine, index=False, if_exists='append')
pd.DataFrame(order_items).to_sql('order_items', engine, index=False, if_exists='append')