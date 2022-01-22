# シンプル家計簿 #
heroku  
https://simplecashbook.herokuapp.com/  
(FastAPIの機能で後ろにdocsを付けるとAPI仕様ドキュメントが自動生成される https://simplecashbook.herokuapp.com/docs )

## 概要 ##
一画面のみで完結するシンプルな家計簿アプリ。カテゴリ別の支出やカテゴリ別の割合の円グラフを表示する機能あり

## 開発環境 ##  
OS  
Debian GNU/Linux 11 (bullseye)
言語  
python3.9  

Webフレームワーク  
FastAPI 0.71.0  
Bootstrap  

テンプレートエンジン  
Jinja2 3.0.3  

データベース  
AQLAlchemy/SQlite3  

pythonライブラリ  
fastapi           0.71.0  
Jinja2            3.0.3  
python-multipart  0.0.5  
SQLAlchemy        1.4.29  
starlette         0.17.1  
uvicorn           0.17.0  
matplotlib          3.5.1  
japanize-matplotlib 1.1.3  

# ファイルの説明 #
controllers.py  
コントローラー。メインの処理を含む  
create_table.py  
データベース生成ファイル。実行には関係ない  
db.py  
データベース定義  
db.sqlite3  
データベース  
models.py  
モデル。今回はItem（項目）モデルのみ  
run.py  
実行ファイル。コマンドラインからでも実行可  


# 参考 #  
https://rightcode.co.jp/blog/information-technology/fastapi-tutorial-todo-apps-environment  
https://pyhaya.hatenablog.com/entry/2018/11/04/180000  
