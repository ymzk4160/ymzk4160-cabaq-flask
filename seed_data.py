from app import create_app, db
from app.models.user import User
from app.models.question import Question, Answer
from datetime import datetime, timedelta
import random

# ダミーデータのテンプレート
categories = ["初心者", "営業", "出勤", "メンタル", "身バレ", "店への不満", "美容", "恋愛", "バースデイ", "プライベート"]

# 質問のテンプレート（各カテゴリ10個ずつ）
question_templates = {
    "初心者": [
        "キャバクラ初めてですが、最初の挨拶はどうすればいいですか？",
        "お給料はいつもらえますか？",
        "ドレスは何着くらい必要ですか？",
        "初めての接客で気をつけることは？",
        "メイクの濃さはどのくらいがいいですか？",
        "キャバ嬢のバッグの中身って何が必要？",
        "初出勤の日に持っていくべきものリスト教えてください",
        "お酒が弱いけどキャバ嬢できますか？",
        "ヘアセットはお店でやってもらえますか？",
        "研修期間はどんな感じですか？"
    ],
    "営業": [
        "指名をもらうコツを教えてください",
        "売上を上げるためにしていることは？",
        "お客さんとの連絡先交換どうしてる？",
        "ボトルを入れてもらうテクニック",
        "話題に困った時の切り返し方法",
        "常連さんを作るコツは？",
        "他の子との差別化の方法",
        "お客さんの名前を覚えるコツ",
        "お酒が進むトークのネタ",
        "初めて来たお客さんへのアプローチ方法"
    ],
    # 他のカテゴリも同様に追加...
}

# 回答のテンプレート
answer_templates = [
    "私の場合は{}をしています。結構効果がありますよ！",
    "{}がおすすめです。私もそれで上手くいきました。",
    "{}というのがポイントだと思います。それを意識するだけでも変わるはず！",
    "経験から言うと、{}が一番重要です。あとは慣れもあるので、焦らずにね。",
    "私も最初は悩みましたが、{}するようになってからうまくいくようになりました！",
    "先輩から教わったんですが、{}だそうです。試してみる価値ありますよ！",
    "{}というのが基本ですね。あとは自分らしさを出すことも大事だと思います。",
    "{}がいいと思います！あと、笑顔も忘れずに♪",
    "私の店では{}というやり方が主流ですね。お店によって違うかもしれませんが参考までに。",
    "{}してみてください！それでダメなら、また相談してくださいね。"
]

# 回答の具体的な内容
answer_contents = {
    "初心者": [
        "笑顔で元気よく挨拶する", "基本的なマナーを押さえておく", "先輩の真似をしてみる",
        "自分らしさを忘れない", "メモを取っておく", "恥ずかしがらない",
        "積極的に質問する", "身だしなみに気を配る", "体調管理をしっかりする",
        "焦らず一つずつ覚えていく"
    ],
    "営業": [
        "お客さんの話をしっかり聞く", "名前と顔を覚える", "特技や個性を出す",
        "SNSを活用する", "お店以外での話題を作る", "さりげなく連絡先を渡す",
        "お客さんの趣味に合わせた話題を用意する", "気配りを忘れない", "タイミングを見極める",
        "自然体でいること"
    ],
    # 他のカテゴリも同様に追加...
}

def seed_database(num_users=20, questions_per_category=15):
    """大量のダミーデータをデータベースに追加する"""
    app = create_app()
    with app.app_context():
        print("データベース初期化中...")
        
        # ユーザーの追加
        users = []
        for i in range(num_users):
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
        print(f"{len(users)}人のユーザーを追加しました")
        
        # 質問と回答の追加
        total_questions = 0
        total_answers = 0
        
        for category in categories:
            for _ in range(questions_per_category):
                # ランダムな質問テンプレートを選択
                if category in question_templates:
                    title = random.choice(question_templates[category])
                else:
                    title = f"{category}についての質問です"
                
                # 質問の作成
                content = f"{title} 詳しく教えてください。"
                created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                question = Question(
                    title=title,
                    content=content,
                    category=category,
                    user_id=random.choice(users).id if random.random() > 0.3 else None,
                    created_at=created_at
                )
                db.session.add(question)
                db.session.flush()  # IDを取得するためにflush
                total_questions += 1
                
                # 回答の作成（1〜5件）
                num_answers = random.randint(1, 5)
                for j in range(num_answers):
                    # ランダムな回答テンプレートとコンテンツを選択
                    answer_template = random.choice(answer_templates)
                    if category in answer_contents:
                        answer_content = answer_template.format(random.choice(answer_contents[category]))
                    else:
                        answer_content = answer_template.format("自分の経験を活かすこと")
                    
                    # 回答を追加
                    hours_later = random.randint(1, 72)
                    answer = Answer(
                        content=answer_content,
                        question_id=question.id,
                        user_id=random.choice(users).id if random.random() > 0.4 else None,
                        created_at=created_at + timedelta(hours=hours_later)
                    )
                    db.session.add(answer)
                    total_answers += 1
                
                # 20件ごとにコミット（パフォーマンス向上）
                if total_questions % 20 == 0:
                    db.session.commit()
        
        # 最終コミット
        db.session.commit()
        print(f"合計 {total_questions} 件の質問と {total_answers} 件の回答を追加しました")

if __name__ == "__main__":
    # 各カテゴリ15件ずつ、全部で150件の質問を生成
    seed_database(num_users=20, questions_per_category=15)
