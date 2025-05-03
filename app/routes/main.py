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
    # データベースから最新の質問を取得（ダミーデータではなく）
    recent_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
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
        # データベースをクリア（オプション）
        db.session.query(Answer).delete()
        db.session.query(Question).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # ユーザーの追加
        users = []
        user_names = ['はじめまして嬢', '迷い中', '伸び悩み中', '同伴苦手嬢', 'シフト迷子', 
                      '風邪気味', '疲れ気味', 'ダブルワーク嬢', 'ノルマ苦戦中', 'ヘルプ嬢',
                      '地元嬢', 'SNS好き', '7月生まれ', '予算組み中', 'メイク崩れ悩み中',
                      '髪質悩み中', '最近恋人できた', '対応に困り中', '将来考え中', 'オフの日迷子']
        
        for i, name in enumerate(user_names):
            user = User(
                email=f"user{i+1}@example.com",
                nickname=name,
                display_name=name,
                password_hash="hashed_password",
                status="active"
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # カテゴリリスト
        categories = ['初心者', '営業', '出勤', 'メンタル', '店への不満', 
                      '身バレ', 'バースデイ', '美容', '恋愛', 'プライベート']
        
        # 質問データ
        questions_data = [
            # 初心者カテゴリ
            {
                'title': '初めてのキャバクラ勤務、何を準備すべき？',
                'content': '来週から初めてキャバクラで働きます。ドレスやメイク道具など、最低限必要なものを教えてください。何から揃えるべきでしょうか？',
                'category': '初心者',
                'user_index': 0,
                'answers': [
                    {'content': 'まずは基本的なメイク道具とシンプルな黒のドレス1着があれば大丈夫です。最初は高すぎるものに手を出さず、仕事に慣れてから徐々に増やしていくことをお勧めします。', 'user_name': '5年選手'},
                    {'content': '化粧ポーチに入れておくと便利なのは、リップ、コンシーラー、つけまつ毛の接着剤です。お直しで必須ですよ。あとは店によってはヘアセットがあるので、そこは確認してみてください。', 'user_name': 'メイク好き'}
                ]
            },
            {
                'title': '大箱と小箱、初心者はどちらがいい？',
                'content': 'これからキャバ嬢デビューしようと思ってます。大きい店と小さい店、どちらから始めるべきでしょうか？それぞれのメリット・デメリットを教えてください。',
                'category': '初心者',
                'user_index': 1,
                'answers': [
                    {'content': '小箱の方が先輩との距離が近く、教えてもらいやすいです。大箱は競争が激しいけど稼げるチャンスは大きいです。私は最初小箱で経験積んでから大箱に移りました。', 'user_name': '元小箱嬢'},
                    {'content': '自分の性格も大事です。人見知りなら小箱から、社交的で積極的なら大箱もアリです。小箱は常連さんが多いので、安定した収入が得やすいというメリットもあります。', 'user_name': '箱転々嬢'}
                ]
            },
            
            # 営業カテゴリ
            {
                'title': '売上アップのための会話術、おすすめは？',
                'content': '最近売上が伸び悩んでいます。お客様との会話を盛り上げるコツや、ドリンクを注文してもらうきっかけづくりについてアドバイスください。',
                'category': '営業',
                'user_index': 2,
                'answers': [
                    {'content': 'お客様の話をしっかり聞くことが一番です。相手の趣味や仕事の話を掘り下げて、「詳しいですね！」と褒めると喜ばれます。そこから「乾杯しましょう」と自然に注文に繋げられます。', 'user_name': '月間MVP'},
                    {'content': '私はお酒のストーリーを話すようにしています。「このカクテルは○○な思い出があって」とか「このワイン、先日知ったんですけど〜」という感じで興味を持ってもらえると注文につながります。', 'user_name': 'カクテル検定持ち'}
                ]
            },
            {
                'title': '同伴のお誘いのタイミングと方法',
                'content': '同伴のお誘いって、どのタイミングでどう切り出すのが効果的ですか？強引すぎず自然に誘える方法を知りたいです。',
                'category': '営業',
                'user_index': 3,
                'answers': [
                    {'content': '次の来店日を聞いたときに「その日のお仕事終わり、ご一緒できたら嬉しいです」と誘うのがスムーズです。強引さがなく、お客様も考える時間があります。', 'user_name': '同伴上手'},
                    {'content': 'お客様の好きな食べ物や行きたいお店の話から「今度ご一緒しませんか？」と繋げるのも自然です。あとは「〇〇さんと一緒にディナーしたいなぁ」と願望を伝えておくと、向こうから誘ってくれることも。', 'user_name': '月20本同伴'}
                ]
            },
            
            # 出勤カテゴリ
            {
                'title': '効率的なシフトの組み方は？',
                'content': '週4〜5で働いていますが、どういう曜日の組み合わせが効率良いですか？売上と体力のバランスを考えた理想的な出勤パターンを教えてください。',
                'category': '出勤',
                'user_index': 4,
                'answers': [
                    {'content': '金土は必須です。あとは水曜も意外と穴場です。私のおすすめは「水・金・土・日または月」の4出勤です。連休明けの月曜も意外といいですよ。', 'user_name': '8年目ベテラン'},
                    {'content': '体力的には連続2日以上の出勤は避けた方がいいです。間に休みを入れると長く続けられます。あと月初と月末は給料日前後なので忙しいです。', 'user_name': '健康第一嬢'}
                ]
            },
            # 残りの質問データも同様に...
        ]
        
        # 質問と回答を追加
        for i, q_data in enumerate(questions_data):
            # 質問を作成
            question = Question(
                title=q_data['title'],
                content=q_data['content'],
                category=q_data['category'],
                is_deleted=False,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                user_id=users[q_data['user_index']].id if 'user_index' in q_data else None
            )
            db.session.add(question)
            db.session.flush()  # IDを取得するためにフラッシュ
            
            # 回答を追加
            for ans_data in q_data['answers']:
                # ランダムなユーザーを選ぶ（回答者用）
                random_user = random.choice(users)
                
                answer = Answer(
                    content=ans_data['content'],
                    question_id=question.id,
                    user_id=random_user.id,
                    created_at=question.created_at + timedelta(hours=random.randint(1, 48))
                )
                db.session.add(answer)
        
        db.session.commit()
        return '20件の質問と約40件の回答をデータベースに追加しました！'
    except Exception as e:
        db.session.rollback()
        return f'エラーが発生しました: {str(e)}'
