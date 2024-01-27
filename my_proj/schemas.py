# schemas.py
from marshmallow import Schema, fields, validate, ValidationError

class userSc(Schema):
    id = fields.Int()
    username = fields.String(required=True)
    currency_id_df = fields.Int(required=False)
    password = fields.String(required=True)
class categorySc(Schema):
    name = fields.String(required=True)

class recordSc(Schema):
    category_id = fields.Integer(required=True, validate=validate.Range(min=0))
    user_id = fields.Integer(required=True, validate=validate.Range(min=0))
    amount = fields.Float(required=True, validate=validate.Range(min=0.0))
    currency_id = fields.Int(required=False)
class currencySc(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    symbol = fields.Str(required=True)


