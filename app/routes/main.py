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
    with current_app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        html = '<h1>データベーステーブル一覧</h1>'
        html += f'<p>テーブル数: {len(tables)}</p>'
        html += '<ul>'
        
        for table in tables:
            html += f'<li><h3>{table}</h3>'
            html += '<table border="1"><tr><th>カラム名</th><th>タイプ</th><th>NULL可</th></tr>'
            
            for column in inspector.get_columns(table):
                html += f'<tr><td>{column["name"]}</td><td>{column["type"]}</td><td>{"はい" if column.get("nullable") else "いいえ"}</td></tr>'
            
            html += '</table></li>'
        
        html += '</ul>'
    return html

@bp.route('/setup-db')
def setup_db():
    with current_app.app_context():
        # 既存のテーブルを全て削除
        db.drop_all()
        # 新しいテーブルを作成
        db.create_all()
    return 'データベーステーブルを全て再作成しました！'
