from my_proj import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=35), nullable=False, unique=False)
    records = db.relationship("Record", back_populates="user", lazy="dynamic")
    currency_id_df = db.Column(db.Integer, db.ForeignKey("currency.id"))
    currency_df = db.relationship("Currency", foreign_keys=[currency_id_df])

class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=35), nullable=False, unique=False)
    symbol = db.Column(db.String(length=10), nullable=False, unique=False)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=35), nullable=False, unique=False)
    record = db.relationship("Record", back_populates="category", lazy="dynamic")

class Record(db.Model):
    __tablename__ = "record"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float(precision=3), unique=False, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"), unique=False, nullable=False)
    user = db.relationship("User", back_populates="records")
    category = db.relationship("Category", back_populates="record")

