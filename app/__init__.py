from flask import Flask, render_template
from app.routes import main  # ← ルート登録を忘れずに！

def create_app():
    app = Flask(__name__)
    
    # ルーティング（Blueprint）を登録
    app.register_blueprint(main.bp)

    # 404エラー処理
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app
