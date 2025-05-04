@bp.route('/check-db')
def check_db():
    """データベースの内容を確認"""
    try:
        users = User.query.all()
        questions = Question.query.all()
        answers = Answer.query.all()
        
        result = f"データベース内容:<br>"
        result += f"ユーザー数: {len(users)}<br>"
        result += f"質問数: {len(questions)}<br>"
        result += f"回答数: {len(answers)}<br>"
        
        if users:
            result += f"<br>ユーザーサンプル: {users[0].nickname}<br>"
        if questions:
            result += f"<br>質問サンプル: {questions[0].title}<br>"
        if answers:
            result += f"<br>回答サンプル: {answers[0].content[:30]}...<br>"
        
        return result
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'
