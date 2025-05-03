from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # ルーティング等の設定…

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app
