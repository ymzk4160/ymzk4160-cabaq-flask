from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random
from app.models import User, Question, Answer

# Blueprintを作成（url_prefixを削除）
bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/')
def index():
    """トップページ"""
    # データベースから最新の質問を取得
    try:
        recent_questions = Question.query.filter_by(is_deleted=False).order_by(Question.created_at.desc()).limit(10).all()
    except Exception as e:
        print(f"エラー発生: {str(e)}")
        recent_questions = []
    
    return render_template('main/index.html', questions=recent_questions)

@bp.route('/about')
def about():
    """サイト紹介ページ"""
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    """データベーステーブルの作成"""
    try:
        db.create_all()
        return 'データベーステーブルが作成されました！'
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'

@bp.route('/seed-data')
def seed_data_route():
    try:
        # データベースをクリア
        db.session.query(Answer).delete()
        db.session.query(Question).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # ユーザーの追加（20名）
        users = []
        user_names = [
            'れいな', 'まお', 'さくら', 'ゆきな', 'みう', 
            'えれな', 'あやか', 'りょう', 'みれい', 'かれん',
            'るか', 'あいり', 'ゆめ', 'まりあ', 'ななみ',
            'ありさ', 'りな', 'ここ', 'じゅり', 'まりな'
        ]
        
        for i, name in enumerate(user_names):
            user = User(
                email=f"user{i+1}@odaiba.info",
                nickname=name,
                display_name=name,
                password_hash="hashed_password",
                status="active"
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        # 質問データ
        questions_data = [
            # 初心者カテゴリ
            {
                'title': '初めてのキャバクラ勤務、何を準備すべき？',
                'content': '来週から初めてキャバクラで働きます。ドレスやメイク道具など、最低限必要なものを教えてください。何から揃えるべきでしょうか？',
                'category': '初心者',
                'user_index': 0,
                'answers': [
                    {'content': 'まずは基本的なメイク道具とシンプルな黒のドレス1着があれば大丈夫です。最初は高すぎるものに手を出さず、仕事に慣れてから徐々に増やしていくことをお勧めします。', 'user_index': 4},
                    {'content': '化粧ポーチに入れておくと便利なのは、リップ、コンシーラー、つけまつ毛の接着剤です。お直しで必須ですよ。あとは店によってはヘアセットがあるので、そこは確認してみてください。', 'user_index': 14}
                ]
            },
            {
                'title': '大箱と小箱、初心者はどちらがいい？',
                'content': 'これからキャバ嬢デビューしようと思ってます。大きい店と小さい店、どちらから始めるべきでしょうか？それぞれのメリット・デメリットを教えてください。',
                'category': '初心者',
                'user_index': 1,
                'answers': [
                    {'content': '小箱の方が先輩との距離が近く、教えてもらいやすいです。大箱は競争が激しいけど稼げるチャンスは大きいです。私は最初小箱で経験積んでから大箱に移りました。', 'user_index': 8},
                    {'content': '自分の性格も大事です。人見知りなら小箱から、社交的で積極的なら大箱もアリです。小箱は常連さんが多いので、安定した収入が得やすいというメリットもあります。', 'user_index': 16}
                ]
            },
            
            # 営業カテゴリ
            {
                'title': '売上アップのための会話術、おすすめは？',
                'content': '最近売上が伸び悩んでいます。お客様との会話を盛り上げるコツや、ドリンクを注文してもらうきっかけづくりについてアドバイスください。',
                'category': '営業',
                'user_index': 2,
                'answers': [
                    {'content': 'お客様の話をしっかり聞くことが一番です。相手の趣味や仕事の話を掘り下げて、「詳しいですね！」と褒めると喜ばれます。そこから「乾杯しましょう」と自然に注文に繋げられます。', 'user_index': 11},
                    {'content': '私はお酒のストーリーを話すようにしています。「このカクテルは○○な思い出があって」とか「このワイン、先日知ったんですけど〜」という感じで興味を持ってもらえると注文につながります。', 'user_index': 9}
                ]
            },
            {
                'title': '同伴のお誘いのタイミングと方法',
                'content': '同伴のお誘いって、どのタイミングでどう切り出すのが効果的ですか？強引すぎず自然に誘える方法を知りたいです。',
                'category': '営業',
                'user_index': 3,
                'answers': [
                    {'content': '次の来店日を聞いたときに「その日のお仕事終わり、ご一緒できたら嬉しいです」と誘うのがスムーズです。強引さがなく、お客様も考える時間があります。', 'user_index': 18},
                    {'content': 'お客様の好きな食べ物や行きたいお店の話から「今度ご一緒しませんか？」と繋げるのも自然です。あとは「〇〇さんと一緒にディナーしたいなぁ」と願望を伝えておくと、向こうから誘ってくれることも。', 'user_index': 13}
                ]
            }
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
                user_id=users[q_data['user_index']].id
            )
            db.session.add(question)
            db.session.flush()  # IDを取得するためにフラッシュ
            
            # 回答を追加
            for ans_data in q_data['answers']:
                answer = Answer(
                    content=ans_data['content'],
                    question_id=question.id,
                    user_id=users[ans_data['user_index']].id,
                    created_at=question.created_at + timedelta(hours=random.randint(1, 48))
                )
                db.session.add(answer)
        
        db.session.commit()
        return '質問と回答をデータベースに追加しました！詳細なダミーデータが反映されました。'
    except Exception as e:
        db.session.rollback()
        return f'エラーが発生しました: {str(e)}'
