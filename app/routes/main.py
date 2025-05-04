@bp.route('/check-db')
def check_db():
    try:
        users = User.query.all()
        questions = Question.query.all()
        answers = Answer.query.all()
        
        result = f"DB内容: ユーザー {len(users)}件、質問 {len(questions)}件、回答 {len(answers)}件"
        return result
    except Exception as e:
        return f'エラー: {str(e)}'
