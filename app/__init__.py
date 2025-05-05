from flask import Flask, request, redirect
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # HTTPSリダイレクト（Renderなどのプロキシ環境向け）
    @app.before_request
    def before_request():
        if request.headers.get("X-Forwarded-Proto", "http") == "http":
            return redirect(request.url.replace("http://", "https://", 1), code=301)

    # データベースの初期化
    db.init_app(app)

    # ブループリントの登録
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    # データ管理用ブループリント登録
    from app.routes.data import bp as data_bp
    app.register_blueprint(data_bp)

    return app
