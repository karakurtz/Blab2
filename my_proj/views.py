from flask import Flask, jsonify, request
from datetime import datetime
import uuid
from my_proj import app


app = Flask(__name__)


@app.route("/")
def hello_page():
    return f"<a href='/healthcheck'>healthcheck page</a>"


@app.route("/healthcheck")
def healthcheck():
    response = jsonify(date=datetime.now(), status="OK")
    response.status_code = 200
    return response


users = {}
categories = {}
records = {}


@app.route('/user/<USER_ID>', methods=['GET', 'DELETE'])
def user_manager(USER_ID):
    if request.method == "GET":
        user = users.get(USER_ID)
        if not user:
            return jsonify({"error": "user with this id does not exist"}), 404
        return jsonify(user)
    elif request.method == "DELETE":
        user = users.pop(USER_ID, None)
        if not user:
            return jsonify({"error": "user with this id does not exist"}), 404
        return jsonify(user)

@app.route('/user', methods=['POST'])
def user_creator():
    user_data_req = request.get_json()
    if "username" not in user_data_req:
        return jsonify({"error": "username need in request"}), 400
    USER_ID = uuid.uuid4().hex
    user = {"id": USER_ID, **user_data_req}
    users[USER_ID] = user
    return jsonify(user)

@app.route('/users', methods=['GET'])
def users_getter():
    return jsonify(list(users.values()))


@app.route('/category', methods=['GET', 'POST', 'DELETE'])
def category_manager():
    if request.method == "GET":
        return jsonify(list(categories.values()))
    elif request.method == "POST":
        category_data_req = request.get_json()
        if "name" not in category_data_req:
            return jsonify({"error": "name need in request"}), 400
        CATEGORY_ID = uuid.uuid4().hex
        category = {"id": CATEGORY_ID, **category_data_req}
        categories[CATEGORY_ID] = category
        return jsonify(category)
    elif request.method == "DELETE":
        CATEGORY_ID = request.args.get('id')
        if CATEGORY_ID:
            category = categories.pop(CATEGORY_ID, None)
            if not category:
                return jsonify({"error": f"CATEGORY ID - {CATEGORY_ID} does not exist"}), 404
            return jsonify(category)
        else:
            categories.clear()
            return jsonify({"message": "categories are deleted"})


@app.route('/record/<RECORD_ID>', methods=['GET', 'DELETE'])
def record_manager(RECORD_ID):
    if request.method == "GET":
        record = records.get(RECORD_ID)
        if not record:
            return jsonify({"error": "this record does not exist"}), 404
        return jsonify(record)
    elif request.method == "DELETE":
        record = records.pop(RECORD_ID, None)
        if not record:
            return jsonify({"error": "this record does not exist"}), 404
        return jsonify(record)


@app.route('/record', methods=['POST', 'GET'])
def record_manager2():
    if request.method == "POST":
        record_data = request.get_json()
        USER_ID = record_data.get('USER_ID')
        CATEGORY_ID = record_data.get('CATEGORY_ID')

        if not USER_ID or not CATEGORY_ID:
            return jsonify({"error": "USER_ID AND CATEGORY_ID both are needed"}), 400
        if USER_ID not in users:
            return jsonify({"error": f"USER ID - {USER_ID} does not exist"}), 404
        if CATEGORY_ID not in categories:
            return jsonify({"error": f"CATEGORY ID - {CATEGORY_ID} does not exist"}), 404

        RECORD_ID = uuid.uuid4().hex
        record = {"id": RECORD_ID, **record_data}
        records[RECORD_ID] = record
        return jsonify(record)
    elif request.method == "GET":
        USER_ID = request.args.get('USER_ID')
        CATEGORY_ID = request.args.get('CATEGORY_ID')
        if not USER_ID and not CATEGORY_ID:
            return jsonify({"ERROR": "USER_ID AND CATEGORY_ID both are needed"}), 400
        filtered_records = [
            r for r in records.values() if (not USER_ID or r['USER_ID'] == USER_ID) or (not CATEGORY_ID or r['CATEGORY_ID'] == CATEGORY_ID)
        ]
        return jsonify(filtered_records)


