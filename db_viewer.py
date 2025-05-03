# db_viewer.py
from app import create_app
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
from flask import json

app = create_app()
with app.app_context():
    # ユーザー情報を取得
    users = User.query.all()
    users_data = [{"id": u.id, "nickname": u.nickname, "email": u.email} for u in users]
    
    # 質問情報を取得
    questions = Question.query.all()
    questions_data = [{"id": q.id, "title": q.title, "category": q.category, 
                      "user_id": q.user_id, "created_at": q.created_at.isoformat()} 
                     for q in questions]
    
    # 回答情報を取得
    answers = Answer.query.all()
    answers_data = [{"id": a.id, "content": a.content[:50], 
                    "question_id": a.question_id, "user_id": a.user_id}
                   for a in answers]
    
    # 情報を表示
    print(f"===== ユーザー数: {len(users)} =====")
    for user in users_data[:5]:  # 最初の5件のみ表示
        print(f"ID: {user['id']}, 名前: {user['nickname']}")
    
    print(f"\n===== 質問数: {len(questions)} =====")
    for question in questions_data[:5]:  # 最初の5件のみ表示
        print(f"ID: {question['id']}, タイトル: {question['title']}, カテゴリ: {question['category']}")
    
    print(f"\n===== 回答数: {len(answers)} =====")
    for answer in answers_data[:5]:  # 最初の5件のみ表示
        print(f"ID: {answer['id']}, 質問ID: {answer['question_id']}, 内容: {answer['content']}...")
    
    # オプション: JSON形式でデータを保存
    with open('db_contents.json', 'w', encoding='utf-8') as f:
        json.dump({
            'users': users_data,
            'questions': questions_data,
            'answers': answers_data
        }, f, ensure_ascii=False, indent=2)
    
    print("\nデータベース内容をdb_contents.jsonに保存しました。")
