from datetime import datetime, timedelta
import random
from app.models.user import User
from app.models.question import Question, Answer

@bp.route('/seed-data')
def seed_data_route():
    """開発用：ダミーデータを追加"""
    try:
        # ユーザーの追加
        users = []
        for i in range(20):
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
        categories = ["初心者", "営業", "出勤", "メンタル", "身バレ", "店への不満", "美容", "恋愛", "バースデイ", "プライベート"]
        
        for category in categories:
            for i in range(5):  # 各カテゴリ5件ずつ
                question = Question(
                    title=f"{category}についての質問{i+1}",
                    content=f"{category}に関する詳細な質問内容です。{i+1}番目の質問です。",
                    category=category,
                    user_id=random.choice(users).id if random.random() > 0.3 else None,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
                )
                db.session.add(question)
                db.session.flush()
                
                # 各質問に1-3件の回答を追加
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
