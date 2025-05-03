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
        # データベースをクリア
        db.session.query(Answer).delete()
        db.session.query(Question).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # ユーザーの追加（20名）
        users = []
        user_names = [
            'はじめまして嬢', '迷い中', '伸び悩み中', '同伴苦手嬢', 'シフト迷子', 
            '風邪気味', '疲れ気味', 'ダブルワーク嬢', 'ノルマ苦戦中', 'ヘルプ嬢',
            '地元嬢', 'SNS好き', '7月生まれ', '予算組み中', 'メイク崩れ悩み中',
            '髪質悩み中', '最近恋人できた', '対応に困り中', '将来考え中', 'オフの日迷子'
        ]
        
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
            {
                'title': '指名やアフターの断り方に悩んでいます',
                'content': '指名は嬉しいけど、アフターや連絡先交換を断りたい場合のスマートな対応方法を教えてください。お客様を怒らせずに上手く断る方法はありますか？',
                'category': '初心者',
                'user_index': 17,
                'answers': [
                    {'content': '「お店のルールでアフターや連絡先交換は禁止されています」と店のルールにするのが一番穏便です。それでも強引な場合は、必ず店長や先輩に相談してください。', 'user_index': 19},
                    {'content': '「今はお仕事に集中したい時期なので…」と丁寧に断るのも効果的です。断る時は必ず代替案（「また店内でお会いできるのを楽しみにしています」など）を出すと印象が良いです。', 'user_index': 5}
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
            },
            
            # 出勤カテゴリ
            {
                'title': '効率的なシフトの組み方は？',
                'content': '週4〜5で働いていますが、どういう曜日の組み合わせが効率良いですか？売上と体力のバランスを考えた理想的な出勤パターンを教えてください。',
                'category': '出勤',
                'user_index': 4,
                'answers': [
                    {'content': '金土は必須です。あとは水曜も意外と穴場です。私のおすすめは「水・金・土・日または月」の4出勤です。連休明けの月曜も意外といいですよ。', 'user_index': 7},
                    {'content': '体力的には連続2日以上の出勤は避けた方がいいです。間に休みを入れると長く続けられます。あと月初と月末は給料日前後なので忙しいです。', 'user_index': 15}
                ]
            },
            {
                'title': '体調不良での当日欠勤、皆さんどうしてる？',
                'content': '急な体調不良で欠勤することになった場合、どう連絡するのがマナーですか？罰金などある店舗が多いと思いますが、どう対処してますか？',
                'category': '出勤',
                'user_index': 5,
                'answers': [
                    {'content': 'できるだけ早く連絡することが大事です。遅くとも出勤の3時間前までには。ちゃんと理由も伝えて、次回必ず出勤することを伝えると印象が違います。', 'user_index': 1},
                    {'content': '本当に体調が悪いときは仕方ないです。でも頻繁に休むとお店からの信用も客層も下がります。私は年に1〜2回しか休まないようにしています。', 'user_index': 8}
                ]
            },
            
            # メンタルカテゴリ
            {
                'title': '仕事のストレス発散法、みんなどうしてる？',
                'content': '最近、仕事のストレスが溜まっていて、休日も気分転換できません。皆さんはどんな方法でリフレッシュしていますか？',
                'category': 'メンタル',
                'user_index': 6,
                'answers': [
                    {'content': '私はジムに通っています。運動すると気分転換になるし、仕事にも活かせます。あとは趣味に没頭する時間を作ることも大事ですよ。', 'user_index': 18},
                    {'content': '完全に仕事から離れる日を作ることが大事です。電話も見ない、SNSも見ない。私は月に2日は「デジタルデトックスデー」を作っています。温泉旅行もおすすめです。', 'user_index': 16}
                ]
            },
            {
                'title': '夜職と昼職の両立、精神的にきつい',
                'content': '昼は事務職、夜はキャバクラで働いています。最近、睡眠不足で精神的にも辛いです。両立している方、どうやって乗り切っていますか？',
                'category': 'メンタル',
                'user_index': 7,
                'answers': [
                    {'content': '私も経験ありますが、長期的には難しいです。無理せず夜職は週末だけにするなど調整した方がいいです。体調崩すと両方できなくなります。', 'user_index': 2},
                    {'content': '栄養ドリンクやサプリに頼りすぎずに、質の良い睡眠を取ることを最優先にしてください。私は週3夜職にして、その分単価を上げる努力をしました。', 'user_index': 19}
                ]
            },
            
            # 店への不満カテゴリ
            {
                'title': 'ノルマがきつい店、移籍すべき？',
                'content': '今の店はノルマが厳しすぎて毎月赤字になることも…。でも常連さんもいるので移籍に踏み切れません。同じような経験のある方、アドバイスください。',
                'category': '店への不満',
                'user_index': 8,
                'answers': [
                    {'content': '常連さんが多いなら、移籍前に連絡先を交換しておくことをお勧めします。私は移籍時に7割の常連さんに新しい店に来てもらえました。ノルマのない店の方が長く続けられます。', 'user_index': 3},
                    {'content': '赤字続きはメンタル的にも辛いです。まずは同じエリアでノルマの緩い店を探してみては？面接の段階でしっかりノルマについて確認することが大事です。', 'user_index': 10}
                ]
            },
            {
                'title': 'ヘルプに行ったら環境最悪だった…',
                'content': 'ヘルプで行った店でスタッフの態度が最悪でした。こういう時どう対応するのがベスト？二度と行きたくないけど、断り方も難しいです。',
                'category': '店への不満',
                'user_index': 9,
                'answers': [
                    {'content': '正直に「体調不良でヘルプが難しい」と伝えるのがシンプルです。あまり嘘をつくと後々面倒なので、丁寧に断るのがベストです。', 'user_index': 4},
                    {'content': '所属店の担当者に相談してみるのも手です。「あちらの店舗とは相性が合わなかった」と伝えれば、次からは別の店を紹介してもらえるかもしれません。', 'user_index': 8}
                ]
            },
            
            # 身バレカテゴリ
            {
                'title': '地元でのお仕事、身バレリスク対策は？',
                'content': '実家から近いエリアで働いています。知り合いに会う可能性があり心配です。身バレ対策として効果的な方法はありますか？',
                'category': '身バレ',
                'user_index': 10,
                'answers': [
                    {'content': 'メイクを普段と大きく変える、カラコンやウィッグを使うなど外見を変えるのが基本です。あとはSNSの設定を見直して、位置情報をオフにするのも忘れずに。', 'user_index': 6},
                    {'content': '私は源氏名と普段の名前を全く別のイメージにしています。また、お店の写真はなるべく顔がわかりにくいアングルを選んでもらうようにお願いしています。', 'user_index': 11}
                ]
            },
            {
                'title': 'SNSでの身バレ防止策について',
                'content': 'インスタやTikTokをやっていますが、お店のSNSと完全に分けるにはどうすればいいですか？アカウントを複数持つコツなども教えてください。',
                'category': '身バレ',
                'user_index': 11,
                'answers': [
                    {'content': '仕事用と私用で完全に別のスマホを持つのがベストです。面倒でも一番安全です。どうしても1台なら、アプリの切り替え忘れに注意してください。', 'user_index': 0},
                    {'content': '私はプライベート用は完全非公開設定にし、フォロワーは厳選しています。また、投稿内容も仕事の内容を匂わせるものは絶対に避けています。', 'user_index': 12}
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
