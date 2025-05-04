@bp.route('/debug-all-tables')
def debug_all_tables():
    from app.extensions import db
    tables = db.metadata.tables
    result = ["<h2>全テーブル構造</h2><ul>"]
    for table_name, table in tables.items():
        result.append(f"<li><strong>{table_name}</strong><ul>")
        for col in table.columns:
            result.append(f"<li>{col.name}: {col.type}</li>")
        result.append("</ul></li>")
    result.append("</ul>")
    return "<html><body>" + "\n".join(result) + "</body></html>"
