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
        db_questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
        
        # テンプレート用に整形
        questions = []
        for q in db_questions:
            category_name = q.category.name if q.category else "未分類"
            answers_list = []
            for a in q.answers:
                if not a.is_deleted:
                    answers_list.append({'content': a.content})
            
            questions.append({
                'id': q.id,
                'title': q.title,
                'content': q.content,
                'category': category_name,
                'answer_count': len(answers_list),
                'answers': answers_list
            })
        
        return render_template('main/index.html', questions=questions)
    except Exception as e:
        # エラーが発生した場合はダミーデータを使用
        return f"データベースエラー: {str(e)}"

@bp.route('/debug')
def debug():
    """デバッグ情報表示"""
    html = "<h1>デバッグ情報</h1>"
    try:
        # データベース接続情報
        html += f"<p>データベースURI: {current_app.config.get('SQLALCHEMY_DATABASE_URI', '未設定')}</p>"
        
        # テーブル情報
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        html += f"<p>テーブル数: {len(tables)}</p>"
        html += "<ul>"
        for table in tables:
            html += f"<li>{table}</li>"
        html += "</ul>"
    except Exception as e:
        html += f"<p>エラー: {str(e)}</p>"
    
    return html
