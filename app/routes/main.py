@bp.route('/seed-data')
def seed_data_route():
    """開発用：ダミーデータを追加"""
    try:
        # ユーザーモデルのインポート
        from app.models.user import User
        from app.models.question import Question, Answer
        from datetime import datetime, timedelta
        import random
        
        # ダミーユーザーデータ (5人だけにして処理を軽くする)
        dummy_users = [
            {"email": "misaki@example.com", "nickname": "美咲", "display_name": "みなみ", "password_hash": "hashed_password"},
            {"email": "reina@example.com", "nickname": "れいな", "display_name": "れいな", "password_hash": "hashed_password"},
            {"email": "sakura@example.com", "nickname": "さくら", "display_name": "さくら", "password_hash": "hashed_password"},
            {"email": "maria@example.com", "nickname": "まりあ", "display_name": "まりあ", "password_hash": "hashed_password"},
            {"email": "yukina@example.com", "nickname": "ゆきな", "display_name": "ゆきの", "password_hash": "hashed_password"}
        ]
        
        # ダミー質問データ (5件だけにして処理を軽くする)
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
            }
        ]
        
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
        
        return 'ダミーデータが追加されました！ユーザー数: {}、質問数: {}'.format(len(users), len(questions))
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'
