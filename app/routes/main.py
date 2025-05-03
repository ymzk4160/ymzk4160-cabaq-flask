from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer

# Blueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # データベースから最新の質問を取得
    recent_questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
    
    return render_template('main/index.html', questions=recent_questions)

@bp.route('/about')
def about():
    """サイト紹介ページ"""
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    """データベーステーブルの作成"""
    db.create_all()
    return 'データベーステーブルが作成されました！'

@bp.route('/seed-data')
def seed_data_route():
    try:
        # ユーザーの追加
        users = []
        for i in range(5):
            name = f"ユーザー{i+1}"
            user = User(
                email=f"user{i+1}@example.com",
                nickname=f"ニックネーム{i+1}",
                display_name=name,
                password_hash="hashed_password",
                status="active"
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # 質問と回答の追加
        categories = ["営業", "客層", "出勤", "美容", "恋愛"]
        
        for category in categories:
            for i in range(2):
                question = Question(
                    title=f"{category}についての質問{i+1}",
                    content=f"{category}に関する詳細な質問内容です。{i+1}番目の質問です。",
                    category=category,
                    is_deleted=False,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                if users:
                    question.user_id = random.choice(users).id
                
                db.session.add(question)
                db.session.flush()
                
                for j in range(random.randint(1, 2)):
                    answer = Answer(
                        content=f"{category}についての回答です。{j+1}番目の回答です。",
                        question_id=question.id,
                        created_at=question.created_at + timedelta(hours=random.randint(1, 72))
                    )
                    if users:
                        answer.user_id = random.choice(users).id
                    
                    db.session.add(answer)
        
        db.session.commit()
        return '10件の質問と約15〜20件の回答をデータベースに追加しました！'
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'
