from flask import Flask, render_template
from app.routes import main

def create_app():
    app = Flask(__name__)
    
    # ここでBlueprint登録が必要
    app.register_blueprint(main.bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    return app
