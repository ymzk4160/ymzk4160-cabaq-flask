from flask import Blueprint, render_template, current_app
from sqlalchemy import inspect

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # ハードコードされたダミーデータを使用
    dummy_questions = [
        # ダミーデータは省略
    ]
    return render_template('main/index.html', questions=dummy_questions)

@bp.route('/debug-info')
def debug_info():
    """デバッグ情報を表示"""
    info = {}
    try:
        # Flaskアプリの設定情報を取得
        info['app_config'] = {k: str(v) for k, v in current_app.config.items() if k != 'SECRET_KEY'}
        
        # SQLAlchemyの状態を確認
        from app.extensions import db
        info['db_initialized'] = hasattr(db, 'engine')
        
        # データベース接続情報
        info['db_uri'] = current_app.config.get('SQLALCHEMY_DATABASE_URI', 'Not found')
        
        # 環境変数確認
        import os
        info['environ'] = {k: v for k, v in os.environ.items() if 'DATABASE' in k or 'POSTGRES' in k}
    except Exception as e:
        info['error'] = str(e)
    
    # HTMLとして整形
    html = '<h1>デバッグ情報</h1>'
    for section, data in info.items():
        html += f'<h2>{section}</h2>'
        html += '<ul>'
        if isinstance(data, dict):
            for k, v in data.items():
                html += f'<li><strong>{k}:</strong> {v}</li>'
        else:
            html += f'<li>{data}</li>'
        html += '</ul>'
    
    return html
