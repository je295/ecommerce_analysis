#读取宽表 跑出4张图
import pandas as pd
import os
import matplotlib.pyplot as plt

from ecommerce_analysis.ecommerce_analysis import engine

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#连接数据库
print(">>>加载sales_fact...")
with engine.connect() as conn:
    df =pd.read_sql('select * from sales_fact',conn)
    df ['order_date'] = pd.to_datetime(df['order_date'])
print(f"    记录数:{len(df)}")

#==========月度销售趋势表=======
def monthly_trend():
    monthly = df.groupby('year_month').agg(
        revenue=('revenue','sum'),
        orders=('order_id','nunique'),
    ).reset_index()

    #画图
    fig, ax1 = plt.subplots(figsize=(12,5))
    ax1.bar(monthly['year_month'],monthly['revenue'],color='blue',label='营收')
    ax1.set_ylabel('营收(元)')
    ax1.tick_params(axis='x', rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(monthly['year_month'],monthly['orders'],color='orange',marker='o',label='订单数')
    ax2.set_ylabel('订单数')
    ax2.legend()

    plt.title('月度销售趋势')
    plt.tight_layout()
    if not os.path.exists("output"):
        os.makedirs("output")
    plt.savefig('output/trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    已输出 output/trend.png")

def category_share():
    if not os.path.exists("output"):
        os.makedirs("output")
    cat = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).reset_index()

    top_n = 5
    top_cat = cat.head(top_n)
    other_sum = cat[top_n:]['revenue'].sum()
    # 拼接“其他”这一行
    if other_sum > 0:
        row_other = pd.DataFrame({"product_name": ["其他"], "revenue": [other_sum]})
        cat_final = pd.concat([top_cat, row_other], ignore_index=True)
    else:
        cat_final = top_cat

    print("调用的数据:")
    print(cat_final)
    plt.figure(figsize=(8,8))
    plt.pie(cat['revenue'],labels=cat['product_name'],autopct='%.1f%%',startangle=90)
    plt.title('品种分类销售额占比')
    plt.tight_layout()
    plt.savefig('output/category_share.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    已输出 output/category_share.png")

def city_top10():
    city = df.groupby('city')['revenue'].sum().nlargest(10).sort_values()

    plt.barh(city.index,city.values,color='blue')
    plt.title('城市排名前十')
    plt.tight_layout()
    plt.savefig('output/city_top10.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    已输出 output/city_top10.png")

def rfm():
    print("!!!!!!!! 进入 RFM 函数 !!!!!!!!")
    try:
        snapshot = df['order_date'].max() + pd.Timedelta(days=1)
        rfm = df.groupby('customer_id').agg(last_order=('order_date','max'),frequency=('order_id','nunique'),
                                        monetary=('revenue','sum'),
        ).reset_index()
        print(f"    RFM基础表:{len(rfm)}")
        rfm['recency'] = (snapshot - rfm['last_order']).dt.days
        rfm['R'] = pd.qcut(rfm['recency'],5,labels=[5,4,3,2,1]).astype(int)
        rfm['F'] = pd.qcut(rfm['frequency'].rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
        rfm['M'] = pd.qcut(rfm['monetary'],5,labels=[1,2,3,4,5]).astype(int)
        print(" R/F/M打印完成")
    except Exception as e:  # ← 加这个
        import traceback
        print("!!!!! RFM 函数报错 !!!!!")
        traceback.print_exc()

    def segment(r):
        if r['R'] >= 4 and r['F'] >= 4 and r['M'] >= 4:
            return '重要价值'
        if r['R'] >= 4 and r['F'] <= 2:
            return '新客户'
        if r['R'] <= 2 and r['F'] >= 4:
            return '高价值流失'
        if r['R'] <= 2 and r['F'] <= 2:
            return '流失客户'
        return '一般客户'

    rfm['segment'] = rfm.apply(segment, axis=1)
    print("    分层完成")

    rfm.to_sql('rfm_segments', con=engine, if_exists='replace', index=False)
    print(f"    已写入 rfm_segments：{len(rfm)} 行")

    seg = rfm['segment'].value_counts()
    plt.figure(figsize=(8, 5))
    seg.plot(kind='barh', color='#4e79a7')
    plt.title('客户分层图')
    plt.tight_layout()
    plt.savefig('output/segment.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("    已输出 output/segment.png")

    print("    客户分层：")
    for s, c in seg.items():
        print(f"      {s}: {c}")

if __name__ == '__main__':
    monthly_trend()
    category_share()
    city_top10()
    rfm()
    print(">>>分析完成,图片在output/目录")
