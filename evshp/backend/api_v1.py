from datetime import datetime
from flask import request, session, jsonify
from evshp import db, app
from evshp.backend.utils import type_validation
import bcrypt

@app.route('/api/v1/register', methods=['POST'])
def api_register():
    try:
        if not type_validation(request.json, {"login":str, "password":str, "email":str}):
            return jsonify({"status":"error", "description":"Wrong type of values"}), 400
    except KeyError:
        return jsonify({"status":"error", "description":"Invalid body"}), 400
    
    if db.users.find_one({"details.email":request.json['email']}) or db.users.find_one({"username":request.json['login']}):
        return jsonify({"status":"error", "description":"Username or email is allready in use"})

    db.users.insert_one({
        "username":request.json['login'],
        "password":bcrypt.hashpw(bytes(request.json['password'], encoding="UTF8"), bcrypt.gensalt()), #hashing password
        "details":{
            "email":request.json['email'],
            "joined":datetime.now(),
            "group":"user"
        }
    })

    return jsonify({"status":"success", "description":"Account registered successfuly"})

@app.route('/api/v1/login', methods=['POST'])
def api_login():
    try:
        if not type_validation(request.json, {"email":str, "password":str}):
            return jsonify({"status":"error", "description":"Wrong type of values"}), 400
    except KeyError:
        return jsonify({"status":"error", "description":"Invalid body"}), 400
    
    user = db.users.find_one({"details.email":request.json['email']})
    if not user:
        return jsonify({"status": "error", "description":"Wrong username or password"}), 403

    if bcrypt.checkpw(bytes(request.json['password'], encoding="UTF8"), user['password']):
        session['username'] = user['username']
        return jsonify({"status": "success", "account_details":user['details']})
    else:
        return jsonify({"status": "error", "description":"Wrong username or password"}), 403