from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
)
from models import db, User, Scholarship, Application
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'dev-secret')

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    db.create_all()

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    if not (name and email and password):
        return jsonify({'msg':'missing fields'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'msg':'email exists'}), 400
    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'registered'}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg':'bad credentials'}), 401
    # store minimal identity and put user info into additional claims to avoid "Subject must be a string" errors
    token = create_access_token(identity=str(user.id), additional_claims={'user': {'id': user.id, 'role': user.role, 'email': user.email}})
    return jsonify({'access_token': token, 'user': {'id':user.id,'name':user.name,'role':user.role}})

@app.route('/scholarships', methods=['GET','POST'])
@jwt_required(optional=True)
def scholarships():
    if request.method == 'GET':
        items = Scholarship.query.all()
        out = []
        for s in items:
            out.append({'id':s.id,'title':s.title,'description':s.description,'eligibility':s.eligibility,'amount':s.amount,'status':s.status})
        return jsonify(out)
    # POST: create scholarship (admin)
    jwt_claims = get_jwt() or {}
    identity = jwt_claims.get('user') or {}
    if not identity or identity.get('role') != 'admin':
        return jsonify({'msg':'admin only'}), 403
    data = request.json or {}
    s = Scholarship(title=data.get('title'), description=data.get('description'), eligibility=data.get('eligibility'), amount=data.get('amount'))
    db.session.add(s)
    db.session.commit()
    return jsonify({'msg':'created','id':s.id}), 201

@app.route('/applications', methods=['GET','POST'])
@jwt_required()
def applications():
    jwt_claims = get_jwt() or {}
    identity = jwt_claims.get('user') or {}
    user_id = identity.get('id')
    role = identity.get('role')
    if request.method == 'POST':
        data = request.json or {}
        scholarship_id = data.get('scholarship_id')
        appn = Application(student_id=user_id, scholarship_id=scholarship_id, documents=data.get('documents'))
        db.session.add(appn)
        db.session.commit()
        return jsonify({'msg':'submitted','id':appn.id}), 201
    # GET: students see their apps, institutions/admin see all
    if role == 'student':
        apps = Application.query.filter_by(student_id=user_id).all()
    else:
        apps = Application.query.all()
    out = []
    for a in apps:
        out.append({'id':a.id,'student_id':a.student_id,'scholarship_id':a.scholarship_id,'status':a.status,'submitted_at':a.submitted_at.isoformat()})
    return jsonify(out)

@app.route('/applications/verify', methods=['POST'])
@jwt_required()
def verify_application():
    jwt_claims = get_jwt() or {}
    identity = jwt_claims.get('user') or {}
    if identity.get('role') not in ('institution','admin'):
        return jsonify({'msg':'forbidden'}), 403
    data = request.json or {}
    app_id = data.get('application_id')
    status = data.get('status')
    appn = Application.query.get(app_id)
    if not appn:
        return jsonify({'msg':'not found'}), 404
    appn.status = status
    db.session.commit()
    return jsonify({'msg':'updated'})


@app.route('/applications/<int:app_id>', methods=['DELETE'])
@jwt_required()
def withdraw_application(app_id):
    jwt_claims = get_jwt() or {}
    identity = jwt_claims.get('user') or {}
    user_id = identity.get('id')
    role = identity.get('role')
    appn = Application.query.get(app_id)
    if not appn:
        return jsonify({'msg':'not found'}), 404
    # students can withdraw their own application; admins/institutions can also change status
    if role == 'student' and appn.student_id != user_id:
        return jsonify({'msg':'forbidden'}), 403
    appn.status = 'withdrawn'
    db.session.commit()
    return jsonify({'msg':'withdrawn'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
