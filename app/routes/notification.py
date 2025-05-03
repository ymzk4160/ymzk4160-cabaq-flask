from flask import Blueprint, render_template
from datetime import datetime

# Blueprintを作成
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """トップページ"""
    # HTMLを直接返す（テンプレートを使わない）
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>キャバ嬢Q&A</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-3">
            <h1>キャバ嬢Q&A</h1>
            <p>ダミーデータが表示されています</p>
            <div class="list-group">
                <div class="list-group-item">
                    <h5>初めてのキャバクラ勤務、何から準備すれば？</h5>
                    <span class="badge bg-primary">初心者</span>
                    <p>回答: ドレスは最初は2〜3着あれば十分です！</p>
                </div>
                <div class="list-group-item">
                    <h5>お客さんとのLINE交換、みんなどうしてる？</h5>
                    <span class="badge bg-primary">営業</span>
                    <p>回答: 私はLINE交換は基本的にしないようにしています。</p>
                </div>
                <div class="list-group-item">
                    <h5>出勤日数の調整について悩んでいます</h5>
                    <span class="badge bg-primary">出勤</span>
                    <p>回答: 私も学校と両立してます！週3でも全然やっていけますよ。</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
