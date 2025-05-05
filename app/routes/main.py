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
        # カテゴリー一覧を取得
        categories = Category.query.all()
        
        # データベースから質問を取得
        db_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
        
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
        
        return render_template('main/index.html', questions=questions, categories=categories)
    except Exception as e:
        # エラーが発生した場合はエラーメッセージを表示
        return f"<h1>データベース接続エラー</h1><p>{str(e)}</p>"

@bp.route('/debug')
def debug():
    """デバッグ情報表示"""
    html = "<h1>デバッグ情報</h1>"
    try:
        # データベース接続情報
        from flask import current_app
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
        
        # カテゴリー情報の表示
        categories = Category.query.all()
        if categories:
            html += "<h2>カテゴリー一覧</h2>"
            html += "<ul>"
            for cat in categories:
                html += f"<li>{cat.id}: {cat.name}</li>"
            html += "</ul>"
        else:
            html += "<p>カテゴリーが見つかりません。</p>"
        
        # Question取得テスト
        questions = Question.query.limit(5).all()
        if questions:
            html += "<h2>質問データテスト</h2>"
            html += "<ul>"
            for q in questions:
                category_name = q.category.name if q.category else "未分類"
                html += f"<li>{q.id}: {q.title} (カテゴリー: {category_name})</li>"
            html += "</ul>"
        else:
            html += "<p>質問データがありません。データベースにデータを投入してください。</p>"
    except Exception as e:
        html += f"<p>エラー: {str(e)}</p>"
    
    return html
