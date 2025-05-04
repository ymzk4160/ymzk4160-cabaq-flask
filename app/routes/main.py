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
