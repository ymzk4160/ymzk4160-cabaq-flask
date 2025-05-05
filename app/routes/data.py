from flask import Blueprint, jsonify

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/insert-mass-data')
def run_insert_mass_data():
    """大量のテストデータを投入するエンドポイント"""
    from app.scripts.insert_mass_data import insert_mass_data
    success = insert_mass_data()
    if success:
        return jsonify({'message': '大量のテストデータを投入しました'})
    else:
        return jsonify({'error': '大量のテストデータの投入に失敗しました'}), 500
