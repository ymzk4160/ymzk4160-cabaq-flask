from flask import Flask, render_template
from app.routes import main  # Blueprint をインポート


def create_app():
    app = Flask(__name__)

    # Blueprint を登録
    app.register_blueprint(main.bp)

    # 404 エラーハンドラー
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app
