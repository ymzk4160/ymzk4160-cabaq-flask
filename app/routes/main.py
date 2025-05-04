from flask import Blueprint, render_template, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
import random
# モデルをインポートする方法を変更
from app.models import User, Question, Answer

# Blueprintを作成
bp = Blueprint('main', __name__)
