from flask import Blueprint, render_template, current_app
from app.models.question import Question
from app.models.answer import Answer
from app.models.category import Category
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    try:
        # データベースから質問を取得
        questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
        return render_template('main/index.html', questions=questions)
    except Exception as e:
        # エラーの詳細を表示
        error_html = f"<h1>データベース接続エラー</h1><p>{str(e)}</p>"
        
        # デバッグ情報も表示
        error_html += "<h2>デバッグ情報</h2>"
        error_html += f"<p>SQLALCHEMY_DATABASE_URI: {current_app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}</p>"
        error_html += f"<p>app_context: {current_app._get_current_object() is not None}</p>"
        
        return error_html

@bp.route('/debug')
def debug():
    """詳細なデバッグ情報を表示"""
    info = {}
    
    # アプリケーション情報
    info['app'] = {
        'name': current_app.name,
        'debug': current_app.debug,
        'testing': current_app.testing,
        'config_keys': list(current_app.config.keys())
    }
    
    # データベース情報
    try:
        info['db'] = {
            'uri': current_app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set'),
            'track_mods': current_app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'Not set'),
            'has_engine': hasattr(db, 'engine'),
            'engine_initialized': bool(getattr(db, 'engines', {}))
        }
        
        # テーブル情報の取得を試みる
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        info['tables'] = inspector.get_table_names()
    except Exception as e:
        info['db_error'] = str(e)
    
    # HTMLを生成
    html = "<h1>アプリケーションデバッグ情報</h1>"
    for section, data in info.items():
        html += f"<h2>{section}</h2>"
        if isinstance(data, dict):
            html += "<ul>"
            for k, v in data.items():
                html += f"<li><strong>{k}:</strong> {v}</li>"
            html += "</ul>"
        elif isinstance(data, list):
            html += "<ul>"
            for item in data:
                html += f"<li>{item}</li>"
            html += "</ul>"
        else:
            html += f"<p>{data}</p>"
    
    return html
