from flask import Blueprint, jsonify
from app.scripts.insert_test_data import insert_test_data

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/insert-test-data')
def run_insert_test_data():
    """テストデータを投入するエンドポイント"""
    success = insert_test_data()
    if success:
        return jsonify({'message': 'テストデータを投入しました'})
    else:
        return jsonify({'error': 'テストデータの投入に失敗しました'}), 500
