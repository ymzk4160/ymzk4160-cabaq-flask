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
                'category': category_name,  # ここで category.name を取得
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
