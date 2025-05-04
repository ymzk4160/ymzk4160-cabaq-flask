from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random
from app.models.user import User
from app.models.question import Question, Answer

# Blueprint を作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    recent_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
    return render_template('main/index.html', questions=recent_questions)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    db.create_all()
    return 'データベーステーブルが作成されました！'

@bp.route('/seed-data')
def seed_data_route():
    try:
        users = []
        for i in range(20):
            name = f"ユーザー{i+1}"
            user = User(
                email=f"user{i+1}@odaiba.info",
                nickname=f"ニックネーム{i+1}",
                display_name=name,
                password_hash="hashed_password",
                status="active"
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()

        categories = ["初心者", "営業", "出勤", "メンタル", "身バレ", "店への不満", "美容", "恋愛", "バースデイ", "プライベート"]
        
        for category in categories:
            for i in range(5):
                question = Question(
                    title=f"{category}についての質問{i+1}",
                    content=f"{category}に関する詳細な質問内容です。{i+1}番目の質問です。",
                    category=category,
                    user_id=random.choice(users).id if random.random() > 0.3 else None,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.session.add(question)
                db.session.flush()

                for j in range(random.randint(1, 3)):
                    answer = Answer(
                        content=f"{category}についての回答です。{j+1}番目の回答です。",
                        question_id=question.id,
                        user_id=random.choice(users).id if random.random() > 0.4 else None,
                        created_at=question.created_at + timedelta(hours=random.randint(1, 72))
                    )
                    db.session.add(answer)

        db.session.commit()
        return '50件の質問と約100件の回答をデータベースに追加しました！'
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'

@bp.route('/debug-questions')
def debug_questions():
    questions = Question.query.all()
    output = [f"{q.id}: {q.title}（{q.category}） - {len(q.answers)}件の回答" for q in questions]
    return "<br>".join(output)

@bp.route('/debug-schema')
def debug_schema():
    result = []

    def describe_model(model):
        return [f"{column.name}: {column.type}" for column in model.__table__.columns]

    result.append("<h2>User テーブル</h2><ul>")
    result += [f"<li>{c}</li>" for c in describe_model(User)]
    result.append("</ul><h2>Question テーブル</h2><ul>")
    result += [f"<li>{c}</li>" for c in describe_model(Question)]
    result.append("</ul><h2>Answer テーブル</h2><ul>")
    result += [f"<li>{c}</li>" for c in describe_model(Answer)]
    result.append("</ul>")

    return "<html><body>" + "\n".join(result) + "</body></html>"

@bp.route('/debug-all-tables')
def debug_all_tables():
    tables = db.metadata.tables
    result = ["<h2>全テーブル構造</h2><ul>"]
    for table_name, table in tables.items():
        result.append(f"<li><strong>{table_name}</strong><ul>")
        for col in table.columns:
            result.append(f"<li>{col.name}: {col.type}</li>")
        result.append("</ul></li>")
    result.append("</ul>")
    return "<html><body>" + "\n".join(result) + "</body></html>"
