# app/scripts/assign_users_to_content.py
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer
import random

def assign_users_to_content():
    """ユーザーを作成し、質問や回答に割り当てる関数"""
    # アプリケーションコンテキストを作成
    app = create_app()
    with app.app_context():
        try:
            # キャバクラ業界でよく使われるニックネーム20名分
            user_data = [
                {'nickname': 'リリカ', 'email': 'lilica@example.com'},
                {'nickname': 'みゆき', 'email': 'miyuki@example.com'},
                {'nickname': 'えりな', 'email': 'erina@example.com'},
                {'nickname': 'れいな', 'email': 'reina@example.com'},
                {'nickname': 'きらり', 'email': 'kirari@example.com'},
                {'nickname': 'あやか', 'email': 'ayaka@example.com'},
                {'nickname': 'ゆきな', 'email': 'yukina@example.com'},
                {'nickname': 'まりあ', 'email': 'maria@example.com'},
                {'nickname': 'かおり', 'email': 'kaori@example.com'},
                {'nickname': 'さくら', 'email': 'sakura@example.com'},
                {'nickname': 'あすか', 'email': 'asuka@example.com'},
                {'nickname': 'りりあ', 'email': 'liria@example.com'},
                {'nickname': 'まお', 'email': 'mao@example.com'},
                {'nickname': 'ななみ', 'email': 'nanami@example.com'},
                {'nickname': 'みさき', 'email': 'misaki@example.com'},
                {'nickname': 'かれん', 'email': 'karen@example.com'},
                {'nickname': 'るな', 'email': 'runa@example.com'},
                {'nickname': 'ちあき', 'email': 'chiaki@example.com'},
                {'nickname': 'えま', 'email': 'emma@example.com'},
                {'nickname': 'みれい', 'email': 'mirei@example.com'}
            ]
            
            # 作成したユーザーIDを保存するリスト
            user_ids = []
            
            # ユーザーをデータベースに作成・保存
            for data in user_data:
                # すでに存在するかチェック
                existing_user = User.query.filter_by(email=data['email']).first()
                if not existing_user:
                    user = User(
                        email=data['email'],
                        nickname=data['nickname'],
                        password_hash='hashed_password'  # 実際の環境では適切にハッシュ化する
                    )
                    db.session.add(user)
                    db.session.flush()  # IDを取得するためにflush
                    user_ids.append(user.id)
                else:
                    user_ids.append(existing_user.id)
            
            db.session.commit()
            
            # 既存の質問と回答にユーザーIDを割り当てる
            questions = Question.query.all()
            for question in questions:
                random_user_id = random.choice(user_ids)
                question.user_id = random_user_id
            
            answers = Answer.query.all()
            for answer in answers:
                # 質問者とは別のユーザーが回答するようにする
                question = Question.query.get(answer.question_id)
                question_user_id = question.user_id if question else None
                available_user_ids = [uid for uid in user_ids if uid != question_user_id]
                random_user_id = random.choice(available_user_ids if available_user_ids else user_ids)
                answer.user_id = random_user_id
            
            db.session.commit()
            print('ユーザーを登録し、コンテンツに割り当てました')
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f'処理エラー: {str(e)}')
            return False

if __name__ == '__main__':
    assign_users_to_content()
