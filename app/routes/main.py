@app.route('/db-info')
def db_info():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    html = '<h1>データベーステーブル一覧</h1>'
    html += f'<p>テーブル数: {len(tables)}</p>'
    html += '<ul>'
    
    for table in tables:
        html += f'<li><h3>{table}</h3>'
        html += '<table border="1"><tr><th>カラム名</th><th>タイプ</th><th>NULL可</th></tr>'
        
        for column in inspector.get_columns(table):
            html += f'<tr><td>{column["name"]}</td><td>{column["type"]}</td><td>{"はい" if column.get("nullable") else "いいえ"}</td></tr>'
        
        html += '</table></li>'
    
    html += '</ul>'
    return html
