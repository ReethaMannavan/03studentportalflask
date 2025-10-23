import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///students.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
