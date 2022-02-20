from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from datetime import datetime
from sqlalchemy import extract, and_, func
import db
from models import Item
import matplotlib.pyplot as plt
import japanize_matplotlib
from io import BytesIO
import base64

app = FastAPI(
    title='CashBook'
)

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env 

TODAY = str(datetime.now()).split('-')
this_year = TODAY[0] # 現在選択されている年
this_month = TODAY[1] # 現在選択されている月

# 支出・収入の計算
def calc_money(items): 
    income = 0
    expense = 0
    for i in items:
        if not i.cost:
            pass
        elif i.is_in:
            income += i.cost
        else:
            expense += i.cost
    return income, expense

# カテゴリごとの円グラフ、表の作成
def make_graph(items): 
    #itemsの中かつis_in==Falseの中からcategoryでgroupbyし、costの合計をカウント
    res = db.session.query(
        Item.category, func.sum(Item.cost).label("cnt")).filter(
        Item.is_in==False, Item.id.in_([i.id for i in items])).group_by(Item.category).order_by("cnt")
    if len(list(res))==0: # データが無かったらreturn
        return 
    else:
        x = [i[1] for i in res] # categoryごとのcost
        y = [i[0] for i in res] # category名

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1) # テーブル
        ax2 = fig.add_subplot(2, 1, 2) # 円グラフ

        ax1.table(cellText=[x], colLabels=y, colWidths=[0.12]*len(x), rowLabels=["金額"])
        ax1.axis('off')

        cmap=plt.get_cmap("tab10") # カラーマップ
        col = cmap(range(len(x)))
        ax2.pie(x, counterclock=True, startangle=90, colors=col,
                autopct=lambda p:"{:.1f}%".format(p) if p>= 4.0 else "") # 4%未満は非表示
        ax2.axis('equal')
        plt.title('月のカテゴリ別支出')
        ax2.legend(y, fontsize=12,bbox_to_anchor=(1, 1)) 
        
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()
        img = buffer.getvalue()
        graph = base64.b64encode(img)
        graph = graph.decode("utf-8")
        buffer.close()
        return graph

@app.get("/")
def index(request: Request):
    global this_year, this_month
    items = db.session.query(Item).filter(
            and_(extract('year',Item.date) == this_year,
            extract('month', Item.date) == this_month)).order_by('date') # 現在選択されているyear/monthのitem
    income, expense = calc_money(items)
    db.session.close()
    graph= make_graph(items)

    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'item': items,
                                       'year' : this_year,
                                       'month' : this_month,
                                       'income' : income,
                                       'expense' : expense,
                                       'graph' : graph                                     
                                       })

# 追加
@app.post("/add")
async def add(request: Request):
    data = await request.form()
    date_str = data.get('date')
    if not date_str: # 無かったらreturn
        return
    else:
        date = datetime.strptime(date_str, '%Y-%m-%d') # str->datetimeに変換

    cost = data.get('cost')
    detail = data.get('detail')
    category = data.get('category')
    is_in = data.get('radio') 
    if str(is_in) == "radio1":
        is_in = True
    else:
        is_in = False

    item = Item(
        date=date,
        cost=cost,
        detail=detail,
        category=category,
        is_in=is_in
    )
    db.session.add(item) # データベースに追加
    db.session.commit()
    global this_year, this_month
    items = db.session.query(Item).filter(
            and_(extract('year',Item.date) == this_year,
            extract('month', Item.date) == this_month)).order_by('date')
    income, expense = calc_money(items)
    db.session.close()
    graph = make_graph(items)    

    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'item': items,
                                       'year' : this_year,
                                       'month' : this_month,
                                       'income' : income,
                                       'expense' : expense,
                                       'graph' : graph                                     
                                       })

# 年/月選択
@app.post("/select")
async def select(request: Request):
    data = await request.form()
    year_month = data.get('month')
    global this_year, this_month
    this_year = year_month.split('-')[0] # datetime->str
    this_month = year_month.split('-')[1]

    items = db.session.query(Item).filter(
        and_(extract('year',Item.date) == this_year,
        extract('month', Item.date) == this_month)).order_by('date')

    income, expense = calc_money(items)
    db.session.close()   
    graph = make_graph(items)

    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'item': items,
                                       'year' : this_year,
                                       'month' : this_month,
                                       'income' : income,
                                       'expense' : expense,
                                       'graph' : graph                                       
                                       })

# 削除
@app.get("/delete/{id}")
async def delete(request: Request, id): 
    item = db.session.query(Item).filter(Item.id == id).first()
    db.session.delete(item) # データベースから削除
    db.session.commit()
    global this_year, this_month
    items = db.session.query(Item).filter(
        and_(extract('year',Item.date) == this_year,
        extract('month', Item.date) == this_month)).order_by('date')
    income, expense = calc_money(items)
    db.session.close()    
    graph = make_graph(items)
    
    return templates.TemplateResponse('index.html',
                                      {'request': request,
                                       'item': items,
                                       'year' : this_year,
                                       'month' : this_month,
                                       'income' : income,
                                       'expense' : expense,
                                       'graph' : graph                                       
                                       })