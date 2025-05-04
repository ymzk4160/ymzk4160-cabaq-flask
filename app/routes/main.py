import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)
# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ユーザーテーブル
class User(db.Model):
    __tablename__ = 'users'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.Text)
    login_type = db.Column(db.String(20))
    google_id = db.Column(db.String(255))
    line_id = db.Column(db.String(255))
    
    # 表示/プロフィール情報
    nickname = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(50))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    birthday = db.Column(db.Date)
    age = db.Column(db.Integer)
    
    # 業界関連情報
    prefecture = db.Column(db.String(50))
    area = db.Column(db.String(100))
    store_name = db.Column(db.String(100))
    store_type = db.Column(db.String(50))
    years_in_industry = db.Column(db.Integer)
    months_in_industry = db.Column(db.Integer)
    position = db.Column(db.String(50))
    shift_type = db.Column(db.String(50))
    specialties = db.Column(db.Text)
    interests = db.Column(db.Text)
    
    # システム設定/管理情報
    is_paid = db.Column(db.Boolean, default=False)
    trial_end_date = db.Column(db.DateTime)
    role = db.Column(db.String(20), default='user')
    status = db.Column(db.String(20), default='active')
    trust_level = db.Column(db.Integer, default=0)
    contribution_points = db.Column(db.Integer, default=0)
    badge_ids = db.Column(db.Text)
    
    # 通知/コミュニケーション設定
    notification_settings = db.Column(JSON)
    last_notification_read_at = db.Column(db.DateTime)
    communication_preference = db.Column(db.String(50))
    email_verified = db.Column(db.Boolean, default=False)
    allow_direct_messages = db.Column(db.Boolean, default=True)
    blocked_user_ids = db.Column(db.Text)
    
    # 活動/ログ情報
    last_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    question_count = db.Column(db.Integer, default=0)
    answer_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    reaction_received_count = db.Column(db.Integer, default=0)
    last_activity_at = db.Column(db.DateTime)
    
    # 管理/メタ情報
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(255))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

# カテゴリテーブル
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    icon = db.Column(db.String(255))
    color = db.Column(db.String(20))
    display_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_visible = db.Column(db.Boolean, default=True)
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.Text)
    question_count = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # 自己参照リレーション
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

# 質問テーブル
class Question(db.Model):
    __tablename__ = 'questions'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255))
    
    # カテゴリとタグ関連
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sub_category_id = db.Column(db.Integer)
    
    # 状態管理
    status = db.Column(db.String(30), default='published')
    is_solved = db.Column(db.Boolean, default=False)
    best_answer_id = db.Column(db.Integer)
    is_public = db.Column(db.Boolean, default=True)
    visibility = db.Column(db.String(20), default='public')
    is_anonymous = db.Column(db.Boolean, default=False)
    is_sticky = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    
    # 統計情報
    view_count = db.Column(db.Integer, default=0)
    unique_view_count = db.Column(db.Integer, default=0)
    answer_count = db.Column(db.Integer, default=0)
    reaction_count = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    thank_count = db.Column(db.Integer, default=0)
    relate_count = db.Column(db.Integer, default=0)
    edit_count = db.Column(db.Integer, default=0)
    
    # メディア情報
    has_images = db.Column(db.Boolean, default=False)
    images = db.Column(JSON)
    
    # 管理/メタ情報
    last_edited_at = db.Column(db.DateTime)
    last_edited_by = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))

# 回答テーブル
class Answer(db.Model):
    __tablename__ = 'answers'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    
    # 状態管理
    is_best_answer = db.Column(db.Boolean, default=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # 統計情報
    comment_count = db.Column(db.Integer, default=0)
    reaction_count = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    thank_count = db.Column(db.Integer, default=0)
    relate_count = db.Column(db.Integer, default=0)
    edit_count = db.Column(db.Integer, default=0)
    
    # メディア情報
    has_images = db.Column(db.Boolean, default=False)
    images = db.Column(JSON)
    
    # 管理/メタ情報
    last_edited_at = db.Column(db.DateTime)
    last_edited_by = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    user = db.relationship('User', backref=db.backref('answers', lazy=True))

# 回答コメントテーブル
class AnswerComment(db.Model):
    __tablename__ = 'answer_comments'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    
    # ツリー構造管理
    parent_id = db.Column(db.Integer, db.ForeignKey('answer_comments.id'))
    reply_depth = db.Column(db.Integer, default=0)
    original_answer_id = db.Column(db.Integer)
    first_reply_user_id = db.Column(db.Integer)
    
    # 状態/統計情報
    is_anonymous = db.Column(db.Boolean, default=False)
    reaction_count = db.Column(db.Integer, default=0)
    edit_count = db.Column(db.Integer, default=0)
    
    # メディア情報
    has_images = db.Column(db.Boolean, default=False)
    images = db.Column(JSON)
    
    # 管理/メタ情報
    last_edited_at = db.Column(db.DateTime)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    answer = db.relationship('Answer', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('answer_comments', lazy=True))
    replies = db.relationship('AnswerComment', backref=db.backref('parent_comment', remote_side=[id]))

# タグテーブル
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(255))
    color = db.Column(db.String(20))
    question_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_visible = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

# 質問タグテーブル
class QuestionTag(db.Model):
    __tablename__ = 'question_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    question = db.relationship('Question', backref=db.backref('question_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('question_tags', lazy=True))

# リアクションテーブル
class Reaction(db.Model):
    __tablename__ = 'reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    reaction_type = db.Column(db.String(20), nullable=False)
    is_visible = db.Column(db.Boolean, default=True)
    ip_address = db.Column(db.String(45))
    remarks = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('reactions', lazy=True))

# 通知テーブル
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    target_type = db.Column(db.String(20))
    target_id = db.Column(db.Integer)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    is_emailed = db.Column(db.Boolean, default=False)
    is_push_sent = db.Column(db.Boolean, default=False)
    is_line_sent = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('notifications', lazy=True))
    from_user = db.relationship('User', foreign_keys=[from_user_id])

# 決済テーブル
class Payment(db.Model):
    __tablename__ = 'payments'
    
    # 基本情報
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='JPY')
    
    # Stripe連携情報
    stripe_customer_id = db.Column(db.String(255))
    stripe_subscription_id = db.Column(db.String(255))
    stripe_payment_method_id = db.Column(db.String(255))
    stripe_invoice_id = db.Column(db.String(255))
    
    # 支払い状態
    status = db.Column(db.String(50), default='active')
    is_active = db.Column(db.Boolean, default=True)
    payment_method = db.Column(db.String(50))
    
    # 日時情報
    start_date = db.Column(db.DateTime)
    trial_end_date = db.Column(db.DateTime)
    next_billing_date = db.Column(db.DateTime)
    cancel_at = db.Column(db.DateTime)
    canceled_at = db.Column(db.DateTime)
    last_payment_at = db.Column(db.DateTime)
    
    # 通知/管理情報
    trial_reminder_sent = db.Column(db.Boolean, default=False)
    cancel_reason = db.Column(db.Text)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

# 決済履歴テーブル
class PaymentHistory(db.Model):
    __tablename__ = 'payment_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='JPY')
    stripe_invoice_id = db.Column(db.String(255))
    stripe_payment_intent_id = db.Column(db.String(255))
    stripe_charge_id = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(50))
    error_message = db.Column(db.Text)
    receipt_url = db.Column(db.String(255))
    receipt_number = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('payment_histories', lazy=True))
    payment = db.relationship('Payment', backref=db.backref('histories', lazy=True))

# 通報テーブル
class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    reason_type = db.Column(db.String(50))
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    handled_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    action_taken = db.Column(db.String(255))
    internal_notes = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('reports', lazy=True))
    handler = db.relationship('User', foreign_keys=[handled_by])

# 閲覧履歴テーブル
class View(db.Model):
    __tablename__ = 'views'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    session_id = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', backref=db.backref('views', lazy=True))
    question = db.relationship('Question', backref=db.backref('views', lazy=True))

# バッジテーブル
class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))
    level = db.Column(db.String(20))
    requirement = db.Column(db.Text)
    is_hidden = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

# ユーザーバッジテーブル
class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, server_default=db.func.now())
    awarded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_displayed = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # リレーション設定
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('badges', lazy=True))
    badge = db.relationship('Badge', backref=db.backref('users', lazy=True))
    awarder = db.relationship('User', foreign_keys=[awarded_by])

# サイト設定テーブル
class Setting(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text)
    type = db.Column(db.String(20))
    group = db.Column(db.String(50))
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup-db')
def setup_db():
    # データベーステーブル作成（初回のみ）
    db.create_all()
    return 'Database tables created!'

@app.route('/db-check')
def db_check():
    try:
        # テーブルの情報を取得
        users = User.query.all()
        questions = Question.query.all()
        categories = Category.query.all()
        
        # HTML形式で表示
        html = '<h1>データベース内容確認</h1>'
        
        html += '<h2>ユーザーテーブル</h2>'
        html += f'<p>登録ユーザー数: {len(users)}</p>'
        if users:
            html += '<table border="1"><tr><th>ID</th><th>メール</th><th>ニックネーム</th><th>有料会員</th><th>作成日時</th></tr>'
            for user in users:
                html += f'<tr><td>{user.id}</td><td>{user.email}</td><td>{user.nickname}</td><td>{"はい" if user.is_paid else "いいえ"}</td><td>{user.created_at}</td></tr>'
            html += '</table>'
        
        html += '<h2>カテゴリテーブル</h2>'
        html += f'<p>カテゴリ数: {len(categories)}</p>'
        if categories:
            html += '<table border="1"><tr><th>ID</th><th>名前</th><th>スラッグ</th><th>表示順</th></tr>'
            for category in categories:
                html += f'<tr><td>{category.id}</td><td>{category.name}</td><td>{category.slug}</td><td>{category.display_order}</td></tr>'
            html += '</table>'
        
        html += '<h2>質問テーブル</h2>'
        html += f'<p>質問数: {len(questions)}</p>'
        if questions:
            html += '<table border="1"><tr><th>ID</th><th>ユーザーID</th><th>タイトル</th><th>カテゴリ</th><th>作成日時</th></tr>'
            for question in questions:
                html += f'<tr><td>{question.id}</td><td>{question.user_id}</td><td>{question.title}</td><td>{question.category_id}</td><td>{question.created_at}</td></tr>'
            html += '</table>'
        
        return html
    except Exception as e:
        return f'エラー: {str(e)}'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
