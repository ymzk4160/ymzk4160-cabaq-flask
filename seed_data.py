from app import create_app, db
from app.models.user import User
from app.models.question import Question, Answer
from datetime import datetime, timedelta
import random

app = create_app()

# ダミーユーザーデータ
dummy_users = [
    {"email": "misaki@example.com", "nickname": "美咲", "display_name": "みなみ", "password_hash": "hashed_password"},
    {"email": "reina@example.com", "nickname": "れいな", "display_name": "れいな", "password_hash": "hashed_password"},
    {"email": "sakura@example.com", "nickname": "さくら", "display_name": "さくら", "password_hash": "hashed_password"},
    {"email": "maria@example.com", "nickname": "まりあ", "display_name": "まりあ", "password_hash": "hashed_password"},
    {"email": "yukina@example.com", "nickname": "ゆきな", "display_name": "ゆきの", "password_hash": "hashed_password"},
    {"email": "yuriko@example.com", "nickname": "ゆりこ", "display_name": "ゆりな", "password_hash": "hashed_password"},
    {"email": "misaki2@example.com", "nickname": "みさき", "display_name": "美咲", "password_hash": "hashed_password"},  
    {"email": "yukina2@example.com", "nickname": "ゆき", "display_name": "ゆきな", "password_hash": "hashed_password"},
    {"email": "yuki@example.com", "nickname": "ゆき", "display_name": "ゆき", "password_hash": "hashed_password"},
    {"email": "mana@example.com", "nickname": "まな", "display_name": "まな", "password_hash": "hashed_password"}
]

# ダミー質問データ
dummy_questions = [
    {
        "title": "初めてのキャバクラ勤務、何から準備すれば？",
        "content": "来月から初めてキャバクラで働くことになりました。ドレスや小物、メイク用品など何を準備すればいいですか？先輩方のアドバイスをいただきたいです。",
        "category": "初心者"
    },
    {
        "title": "お客さんとのLINE交換、みんなどうしてる？",
        "content": "最近、常連さんからLINE交換を求められることが増えました。みなさんはどう対応していますか？店側のルールはないのですが...",
        "category": "営業"
    },
    {
        "title": "出勤日数の調整について悩んでいます",
        "content": "今月から学校も始まり、両立が難しくなってきました。週3日の出勤でも稼げている方いますか？効率よく稼ぐコツを教えてください。",
        "category": "出勤"
    },
    {
        "title": "人間関係のストレスでメンタルが限界",
        "content": "先輩との関係がうまくいかず、お店に行くのが辛くなってきました。でも収入は必要だし...。同じような経験のある方、どう乗り越えましたか？",
        "category": "メンタル"
    },
    {
        "title": "地元で働くのが怖い、身バレしないか心配",
        "content": "地元のお店で働き始めたのですが、知り合いに会わないか毎日ヒヤヒヤしています。身バレ対策や、もし会ってしまった時の対処法を知りたいです。",
        "category": "身バレ"
    },
    {
        "title": "店長からのノルマがきつすぎる...",
        "content": "今月から突然ドリンクのノルマが上がって、達成できるか不安です。ノルマがきつい店での働き方や対処法について教えてください。",
        "category": "店不満"
    },
    {
        "title": "即日で肌をきれいに見せる方法ある？",
        "content": "明日大事なお客様が来るのに、肌の調子が最悪です。即効性のあるスキンケアや、メイクでカバーする方法を教えてください！",
        "category": "美容"
    },
    {
        "title": "常連のお客さんから告白されました",
        "content": "毎週来てくれる常連さんから真剣に付き合いたいと言われました。断ると来なくなりそうだし、でも本当に好きかと言われるとよく分からなくて...。皆さんならどうしますか？",
        "category": "恋愛"
    },
    {
        "title": "誕生日イベントで予算をかけるべき？",
        "content": "来月誕生日なのでお店でイベントをやろうと思っています。装飾やドレスなどどのくらい予算をかけるべきでしょうか？投資以上に売上は上がりましたか？",
        "category": "バースデイ"
    },
    {
        "title": "夜職と昼職の両立、可能ですか？",
        "content": "昼は事務のパートをしていて、夜にキャバクラで働いています。体力的にきついけど、貯金のためにもう少し続けたいです。両立している方、時間管理や体調管理の工夫を教えてください。",
        "category": "プライベート"
    }
]

# ダミー回答データ（質問に対する回答）
dummy_answers = [
    # 初心者質問の回答
    [
        "ドレスは最初は2〜3着あれば十分です！私は最初、古着屋で手頃な値段のものを買いました。メイク用つけまつげは必須です。あとは店によってドレスコードが違うので、先に確認するといいですよ。",
        "私が初めて入った時に役立ったのは、ヘアアレンジの練習！YouTubeで簡単なアップスタイルをマスターしておくと便利です。あと小物は徐々に増やしていけばOKですよ。焦らないでね♪"
    ],
    # 営業質問の回答
    [
        "私はLINE交換は基本的にしないようにしています。どうしても、という場合はサブアカウントを作って、仕事用のみで使い分けています。プライベートとの境界線は大事ですよ。",
        "店のルールがないなら自分でルールを決めるのが大事。私は「月に3回以上来てくれる常連さんだけ」と決めています。あとは断る時も「お店のLINEでいつでも連絡取れるから」と言うと柔らかく断れますよ。"
    ],
    # 出勤質問の回答
    [
        "私も学校と両立してます！週3でも全然やっていけますよ。コツは出勤する曜日を固定することと、いかに効率よく常連さんを作るか。私は週末と、平日は水曜だけ出勤して、常連さんには事前に伝えておくようにしています。",
        "効率よく稼ぐコツは、短時間でも集中して営業すること！私は5時間勤務ですが、入ったら即メイク直しとかせずにすぐ席に着くようにしています。あと、週3なら他の女の子と被らない曜日を選ぶのもポイントですよ。"
    ],
    # メンタル質問の回答
    [
        "すごく分かります...私も同じ経験ありました。結局私は店を変えましたが、その前に試したのは「自分の得意分野を見つけること」。歌が得意とか、トークが得意とか、何か一つ自信を持てる部分があると精神的に楽になりました。",
        "人間関係辛いですよね。私は「割り切る」ことにしました。結局ここは仕事場であって、プライベートでは関わらなくていい。最低限の挨拶と情報共有だけして、あとは自分のお客さんと向き合う時間を大切にしています。"
    ],
    # 身バレ質問の回答
    [
        "私も地元で働いていますが、意外と知り合いに会うことは少ないです。対策としては、SNSの設定を見直す、メイクを普段と変える、名前を本名と離れたものにする、などをしています。",
        "万が一会ってしまった時は、堂々としていることが一番です。向こうも言いづらいはず。私はむしろ先に「ここで会うなんて！」と言って、「内緒にしてね」とお願いしています。意外と理解してくれる人が多いですよ。"
    ],
    # 店不満質問の回答
    [
        "ノルマがきついのは本当に辛いですよね。私の対策は、自分のお客さんにノルマの話を上手に伝えること。「今月このお酒推してるんだ〜」と軽く言うだけで、気にかけてくれる常連さんは多いです。",
        "それはきついですね...。私なら、まずは同僚と協力体制を作ります。「あなたのお客さんにはこのドリンク、私のお客さんにはこのドリンク」みたいに。あとは、達成できなかった時のペナルティがあるなら、それも考慮して店を変えるのも選択肢かも。"
    ],
    # 美容質問の回答
    [
        "即効性があるのは、シートマスクを冷蔵庫で冷やしておいて、朝起きたらすぐにパックすること！むくみも取れるし、肌の調子もかなり良くなりますよ。あとはメイクの下地を念入りに。プライマーを塗って、その上からクッションファンデを薄く何度か重ねると、肌がきれいに見えます。",
        "ベースメイクが命です！私は肌荒れがひどい時、下地の前に色補正下地（緑や紫）を部分的に使ってから、リキッドファンデを重ねています。あとは、目元のメイクを強調すると肌の悩みから目をそらせますよ。"
    ],
    # 恋愛質問の回答
    [
        "これは難しい問題ですね...。私は以前同じ状況になって、一度だけデートしてみました。でも、やっぱり気持ちがついていかなくて、「大切なお客様としての関係を続けたい」と伝えました。意外とその後も来てくれています。正直に自分の気持ちを伝えるのが一番だと思います。",
        "私は恋愛とお仕事は完全に分けています。どんなに誠実な人でも、最初にあなたを知ったのはキャストとしてなので、そのイメージが強いはず。「今はキャリアに集中したい」と優しく断るのがいいと思います。"
    ],
    # バースデイ質問の回答
    [
        "私はバースデーイベント、結構力入れています！装飾は1〜2万円くらいかけて、ドレスは新調しました。結果、いつもの3倍くらい売上がありました！常連さんが「特別な日に呼んでもらえた」と喜んでくれて、むしろ絆が深まった感じです。",
        "バースデーイベントは投資対効果抜群です！私の場合、装飾は100均とネットで5千円くらい、ドレスはレンタルでした。それでも写真映えするセッティングができて、SNSの反応もよかったです。事前にしっかり告知すれば、普段来ない人も来てくれますよ。"
    ],
    # プライベート質問の回答
    [
        "私も昼職と夜職の両立経験あります！一番大事なのは睡眠時間の確保です。私は昼職が終わったら必ず1時間は仮眠を取るようにしていました。あとは、栄養ドリンクに頼りすぎず、ちゃんと食事をとること。特に鉄分とタンパク質は意識的に摂取していました。",
        "両立大変ですよね...。私は「どちらも100％」を目指すのをやめました。夜職の日は昼職でできるだけ体力を温存、逆に昼職で大事な日は夜職を休む、といった優先順位付けも必要です。あとは、ビタミン剤の活用と週に1日は完全休養日を作ることで持ちこたえていました。"
    ]
]

def seed_database():
    with app.app_context():
        # データベースをクリア
        db.drop_all()
        db.create_all()
        
        print("データベースをリセットしました")
        
        # ユーザーを追加
        users = []
        for user_data in dummy_users:
            user = User(
                email=user_data["email"],
                nickname=user_data["nickname"],
                display_name=user_data["display_name"],
                password_hash=user_data["password_hash"],
                status="active",
                trial_end_date=datetime.utcnow() + timedelta(days=10)
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"{len(users)}人のユーザーを追加しました")
        
        # 質問を追加
        questions = []
        now = datetime.utcnow()
        
        for i, question_data in enumerate(dummy_questions):
            # ランダムな時間を割り当て（過去1週間以内）
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            question_time = now - timedelta(days=days_ago, hours=hours_ago)
            
            # ランダムなユーザーを選択
            user = random.choice(users) if random.random() > 0.3 else None  # 約30%は匿名投稿
            
            question = Question(
                title=question_data["title"],
                content=question_data["content"],
                category=question_data["category"],
                created_at=question_time,
                user_id=user.id if user else None
            )
            db.session.add(question)
            questions.append(question)
        
        db.session.commit()
        print(f"{len(questions)}件の質問を追加しました")
        
        # 回答を追加
        answer_count = 0
        
        for i, question in enumerate(questions):
            # この質問に対する回答
            answers_for_question = dummy_answers[i] if i < len(dummy_answers) else []
            
            for j, answer_content in enumerate(answers_for_question):
                # 質問時間より後、現在時刻までのランダムな時間を設定
                question_time = question.created_at
                max_hours_after = int((now - question_time).total_seconds() / 3600)
                if max_hours_after <= 0:
                    max_hours_after = 1
                
                hours_after = random.randint(1, max_hours_after)
                answer_time = question_time + timedelta(hours=hours_after)
                
                # ランダムなユーザーを選択
                user = random.choice(users) if random.random() > 0.4 else None  # 約40%は匿名回答
                
                answer = Answer(
                    content=answer_content,
                    created_at=answer_time,
                    question_id=question.id,
                    user_id=user.id if user else None
                )
                db.session.add(answer)
                answer_count += 1
        
        db.session.commit()
        print(f"{answer_count}件の回答を追加しました")
        
        print("データベースへのシード処理が完了しました")

if __name__ == "__main__":
    seed_database()
