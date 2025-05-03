from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random

# 単純なBlueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # データベース接続なしでシンプルに表示
    return render_template('main/index.html', questions=[])

@bp.route('/about')
def about():
    """サイト紹介ページ"""
    return render_template('main/about.html')

@bp.route('/setup-db')
def setup_db():
    """データベーステーブルの作成"""
    try:
        db.create_all()
        return 'データベーステーブルが作成されました！'
    except Exception as e:
        return f'エラーが発生しました: {str(e)}'

@bp.route('/seed-data')
def seed_data_route():
    return '一時的に無効化されています'
