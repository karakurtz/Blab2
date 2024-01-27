from my_proj import app, db
from flask import Flask, request, jsonify, abort
from datetime import datetime
from my_proj.schemas import userSc, categorySc, recordSc, currencySc
from my_proj.model import User, Category, Record, Currency
import uuid
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError



with app.app_context():
    db.create_all()
    db.session.commit()



@app.route("/")
def hello_page():
    return f"<a href='/healthcheck'>healthcheck page</a>"


@app.route("/healthcheck")
def healthcheck():
    response = jsonify(date=datetime.now(), status="OK")
    response.status_code = 200
    return response



@app.route('/user/<int:USER_ID>', methods=['GET', 'DELETE'])
def user_manager(USER_ID):
    with app.app_context():
        user_data_qu = User.query.get(USER_ID)

        if not user_data_qu:
            return jsonify({'error': f'user - {USER_ID} does not exist'}), 404

        if request.method == "GET":
            user_dt = {
                'id': user_data_qu.id,
                'username': user_data_qu.username,
                'currency': user_data_qu.currency_id_df
            }
            return jsonify(user_dt), 200

        elif request.method == "DELETE":
            db.session.delete(user_data_qu)
            db.session.commit()
            return jsonify({'message': f'user - {USER_ID} was deleted'}), 200


@app.route('/users', methods=['GET'])
def users_getter():
    with app.app_context():
        response = [
            {"id": user.id,
              "username": user.username,
              "currency": user.currency_id_df} for user in User.query.all()
        ]
        return jsonify(response)

@app.route('/user', methods=['POST'])
def user_creator():
    user_data_req = request.get_json()

    userSchema = userSc()
    try:
        user_data_example = userSchema.load(user_data_req)
    except ValidationError as err:
        return jsonify({'ERROR': err.messages}), 400

    currency_id_df = user_data_req.get("currency_id_df")
    currency_df = Currency.query.filter_by(id=currency_id_df).first()

    if currency_id_df is None:
        currency_df = Currency.query.filter_by(name="default currency").first()
        if not currency_df:
            currency_df = Currency(name="default currency", symbol="defsymb")
            db.session.add(currency_df)
            db.session.commit()
            currency_df = Currency.query.filter_by(name="default currency").first()

    post_user = User(
        username=user_data_example["username"],
        currency_id_df=currency_df.id
    )
    with app.app_context():
        db.session.add(post_user)
        db.session.commit()

        response = {
            'id': post_user.id,
            'username': post_user.username,
            'currency': post_user.currency_df.symbol if post_user.currency_df else None
        }

        return jsonify(response), 200



@app.route('/category', methods=['POST', 'GET'])
def category_manager():
    if request.method == 'GET':
        with app.app_context():
            category_data_qu = {
                category.id: {"name": category.name} for category in Category.query.all()
            }
            return jsonify(category_data_qu)

    elif request.method == 'POST':
        category_data_req = request.get_json()
        category_schema_example = categorySc()
        try:
            category_data_qu = category_schema_example.load(category_data_req)
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

        post_category = Category(name=category_data_qu["name"])
        with app.app_context():
            db.session.add(post_category)
            db.session.commit()

            response = {
                "id": post_category.id,
                "name": post_category.name
            }

            return jsonify(response), 200





@app.route('/category/<int:CATEGORY_ID>', methods=['DELETE'])
def category_deleter(CATEGORY_ID):
    with app.app_context():
        category_data_req = Category.query.get(CATEGORY_ID)

        if not category_data_req:
            return jsonify({'error': f'category with id {CATEGORY_ID} does not exist'}), 404

        db.session.delete(category_data_req)
        db.session.commit()
        return jsonify({'message': f'category with id - {CATEGORY_ID} was deleted'}), 200





@app.route('/records', methods=['GET'])
def records_getter():
    with app.app_context():
        response = [
                 {
                    "record id": record.id,
                    "user id": record.user_id,
                    "category id": record.category_id,
                    "currency id": record.currency_id,
                    "amount": record.amount,
                    "created": record.created
                } for record in Record.query.all()
            ]
        return jsonify(response)


@app.route('/record', methods=['GET', 'POST'])
def record_manager():
    if request.method == 'GET':
        user_id_req = request.args.get('user_id')
        category_id_req = request.args.get('category_id')
        if not user_id_req and not category_id_req:
            return jsonify({'error': 'both user id and category id are required'}), 400

        query = Record.query
        if user_id_req:
            query = query.filter_by(user_id=user_id_req)
        if category_id_req:
            query = query.filter_by(category_id=category_id_req)

        record_query = query.all()
        print(record_query)
        response = [{"record id": record.id,
                "user id": record.user_id,
                "category id": record.category_id,
                "currency id": record.currency_id,
                "amount": record.amount,
                "created": record.created
            } for record in record_query
        ]
        return jsonify(response)

    elif request.method == 'POST':
        record_data_req = request.get_json()
        recordSchema = recordSc()
        try:
            record_data_example = recordSchema.load(record_data_req)
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

        user_id = record_data_example['user_id']
        user_select = User.query.get(user_id)

        if not user_select:
            return jsonify({'error': 'user does not exist'}), 404
        currency_id = user_select.currency_id_df
        new_record = Record(
            user_id=user_id,
            category_id=record_data_example['category_id'],
            amount=record_data_example['amount'],
            currency_id=currency_id
        )
        with app.app_context():
            db.session.add(new_record)
            db.session.commit()

            response = {
                "record id": new_record.id,
                "user id": new_record.user_id,
                "category id": new_record.category_id,
                "currency id": new_record.currency_id,
                "amount": new_record.amount
            }

            return jsonify(response), 200

@app.route('/record/<int:RECORD_ID>', methods=['GET', 'DELETE'])
def record_manager2(RECORD_ID):
    with app.app_context():
        record_data_req = Record.query.get(RECORD_ID)

        if not record_data_req:
            return jsonify({"error": f"record with id - {RECORD_ID} does not exist"}), 404

        if request.method == "GET":
            response = {
                "record id": record_data_req.id,
                "user id": record_data_req.user_id,
                "category id": record_data_req.category_id,
                "currency id": record_data_req.currency_id,
                "amount": record_data_req.amount,
                "created": record_data_req.created
            }
            return jsonify(response), 200

        elif request.method == "DELETE":
            db.session.delete(record_data_req)
            db.session.commit()
            return jsonify({'message': f'record with id - {RECORD_ID} was deleted'}), 200

@app.route('/currency', methods=['POST', 'GET'])
def currency_manager():
    if request.method == 'GET':
        with app.app_context():
            response = [
                             {"currency id": currency.id,
                              "name": currency.name,
                              "symbol": currency.symbol} for currency in Currency.query.all()
            ]
            return jsonify(response)

    elif request.method == 'POST':
        currency_data_req = request.get_json()
        currencySchema = currencySc()
        try:
            currency_example = currencySchema.load(currency_data_req)
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400

        new_currency = Currency(name=currency_example["name"], symbol=currency_example["symbol"])
        with app.app_context():
            db.session.add(new_currency)
            db.session.commit()

            response = {
                "id": new_currency.id,
                "name": new_currency.name,
                "symbol": new_currency.symbol
            }

            return jsonify(response), 200

@app.route('/currency/<int:CURRENCY_ID>', methods=['DELETE'])
def currency_deleter(CURRENCY_ID):
    with app.app_context():
        currency_data_req = Currency.query.filter_by(id=CURRENCY_ID).first()
        if currency_data_req:
            db.session.delete(currency_data_req)
            db.session.commit()
            return jsonify({'message': f'currency with id - {CURRENCY_ID} was deleted'}), 200
        else:
            return jsonify({'error': f'currency with id - {CURRENCY_ID} does not exist'}), 404
