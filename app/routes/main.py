from flask import Blueprint, render_template, current_app
from sqlalchemy import inspect
from app.extensions import db

# ブループリントを定義
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    return render_template('main/index.html')

@bp.route('/db-info')
def db_info():
    tables = []
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
    except Exception as e:
        return f'データベース接続エラー: {str(e)}'
    
    html = '<h1>データベーステーブル一覧</h1>'
    html += f'<p>テーブル数: {len(tables)}</p>'
    html += '<ul>'
    
    for table in tables:
        html += f'<li><h3>{table}</h3>'
        try:
            html += '<table border="1"><tr><th>カラム名</th><th>タイプ</th><th>NULL可</th></tr>'
            
            for column in inspector.get_columns(table):
                html += f'<tr><td>{column["name"]}</td><td>{column["type"]}</td><td>{"はい" if column.get("nullable") else "いいえ"}</td></tr>'
            
            html += '</table>'
        except Exception as column_err:
            html += f'<p>カラム情報の取得中にエラー: {str(column_err)}</p>'
        
        html += '</li>'
    
    html += '</ul>'
    return html

@bp.route('/setup-db')
def setup_db():
    try:
        # データベースを操作
        db.drop_all()
        db.create_all()
        return 'データベーステーブルを全て再作成しました！'
    except Exception as e:
        return f'テーブル作成エラー: {str(e)}'
