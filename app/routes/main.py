from flask import Blueprint, render_template, current_app
from app.models.question import Question
from app.models.answer import Answer
from app.models.category import Category
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    try:
        # データベースから質問を取得
        db_questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
        
        # テンプレート用に整形
        questions = []
        for q in db_questions:
            category_name = q.category.name if q.category else "未分類"
            answers_list = []
            for a in q.answers:
                if not a.is_deleted:
                    answers_list.append({'content': a.content})
            
            questions.append({
                'id': q.id,
                'title': q.title,
                'content': q.content,
                'category': category_name,
                'answer_count': len(answers_list),
                'answers': answers_list
            })
        
        return render_template('main/index.html', questions=questions)
    except Exception as e:
        # エラーが発生した場合はダミーデータを使用
        dummy_questions = [
            {
                'id': 1,
                'title': '初めてのキャバクラ勤務、何を準備すべき？',
                'content': '来週から初めてキャバクラで働きます。ドレスやメイク道具など、最低限必要なものを教えてください。',
                'category': '初心者',
                'answer_count': 2,
                'answers': [
                    {'content': 'まずは基本的なメイク道具とシンプルな黒のドレス1着があれば大丈夫です。最初は高すぎるものに手を出さず、仕事に慣れてから徐々に増やしていくことをお勧めします。'}
                ]
            },
            {
                'id': 2,
                'title': '大箱と小箱、初心者はどちらがいい？',
                'content': 'これからキャバ嬢デビューしようと思ってます。大きい店と小さい店、どちらから始めるべきでしょうか？',
                'category': '初心者',
                'answer_count': 3,
                'answers': [
                    {'content': '小箱の方が先輩との距離が近く、教えてもらいやすいです。大箱は競争が激しいけど稼げるチャンスは大きいです。'}
                ]
            },
            {
                'id': 3,
                'title': '売上アップのための会話術、おすすめは？',
                'content': '最近売上が伸び悩んでいます。お客様との会話を盛り上げるコツは？',
                'category': '営業',
                'answer_count': 4,
                'answers': [
                    {'content': 'お客様の話をしっかり聞くことが一番です。相手の趣味や仕事の話を掘り下げて、「詳しいですね！」と褒めると喜ばれます。'}
                ]
            },
            {
                'id': 4,
                'title': '同伴のお誘いのタイミングと方法',
                'content': '同伴のお誘いって、どのタイミングでどう切り出すのが効果的ですか？',
                'category': '営業',
                'answer_count': 2,
                'answers': [
                    {'content': '次の来店日を聞いたときに「その日のお仕事終わり、ご一緒できたら嬉しいです」と誘うのがスムーズです。'}
                ]
            },
            {
                'id': 5,
                'title': '効率的なシフトの組み方は？',
                'content': '週4〜5で働いていますが、どういう曜日の組み合わせが効率良いですか？',
                'category': '出勤',
                'answer_count': 3,
                'answers': [
                    {'content': '金土は必須です。あとは水曜も意外と穴場です。私のおすすめは「水・金・土・日または月」の4出勤です。'}
                ]
            },
            {
                'id': 6,
                'title': '体調不良での当日欠勤、皆さんどうしてる？',
                'content': '急な体調不良で欠勤することになった場合、どう連絡するのがマナーですか？',
                'category': '出勤',
                'answer_count': 5,
                'answers': [
                    {'content': 'できるだけ早く連絡することが大事です。遅くとも出勤の3時間前までには。ちゃんと理由も伝えて、次回必ず出勤することを伝えると印象が違います。'}
                ]
            },
            {
                'id': 7,
                'title': '仕事のストレス発散法、みんなどうしてる？',
                'content': '最近、仕事のストレスが溜まっていて、休日も気分転換できません。',
                'category': 'メンタル',
                'answer_count': 8,
                'answers': [
                    {'content': '私はジムに通っています。運動すると気分転換になるし、仕事にも活かせます。あとは趣味に没頭する時間を作ることも大事ですよ。'}
                ]
            },
            {
                'id': 8,
                'title': '夜職と昼職の両立、精神的にきつい',
                'content': '昼は事務職、夜はキャバクラで働いています。最近、睡眠不足で精神的にも辛いです。',
                'category': 'メンタル',
                'answer_count': 4,
                'answers': [
                    {'content': '私も経験ありますが、長期的には難しいです。無理せず夜職は週末だけにするなど調整した方がいいです。体調崩すと両方できなくなります。'}
                ]
            },
            {
                'id': 9,
                'title': 'ノルマがきつい店、移籍すべき？',
                'content': '今の店はノルマが厳しすぎて毎月赤字になることも…。でも常連さんもいるので移籍に踏み切れません。',
                'category': '店不満',
                'answer_count': 3,
                'answers': [
                    {'content': '常連さんが多いなら、移籍前に連絡先を交換しておくことをお勧めします。私は移籍時に7割の常連さんに新しい店に来てもらえました。'}
                ]
            },
            {
                'id': 10,
                'title': '地元でのお仕事、身バレリスク対策は？',
                'content': '実家から近いエリアで働いています。知り合いに会う可能性があり心配です。',
                'category': '身バレ',
                'answer_count': 6,
                'answers': [
                    {'content': 'メイクを普段と大きく変える、カラコンやウィッグを使うなど外見を変えるのが基本です。あとはSNSの設定を見直して、位置情報をオフにするのも忘れずに。'}
                ]
            }
        ]
        return render_template('main/index.html', questions=dummy_questions)

@bp.route('/debug')
def debug():
    """詳細なデバッグ情報を表示"""
    info = {}
    
    # アプリケーション情報
    info['app'] = {
        'name': current_app.name,
        'debug': current_app.debug,
        'testing': current_app.testing,
        'config_keys': list(current_app.config.keys())
    }
    
    # データベース情報
    try:
        info['db'] = {
            'uri': current_app.config.get('SQLALC
