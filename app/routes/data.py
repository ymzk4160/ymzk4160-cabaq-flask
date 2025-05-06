from flask import Blueprint, jsonify

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/insert-mass-data')
def run_insert_mass_data():
    """大量のテストデータを投入するエンドポイント"""
    return jsonify({'message': 'このエンドポイントは現在無効化されています。'})
