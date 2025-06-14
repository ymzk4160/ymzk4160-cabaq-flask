import os

class Config:
    # ホスト名を完全な形式で指定
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_ueQ9V4yPMnU0@ep-late-sky-a1w66gtw-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
