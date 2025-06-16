from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import bcrypt

from models import db, User, ResetCode
from utils import send_email_code

app = Flask(_name_)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/send-reset-code', methods=['POST'])
def send_reset_code():
    data = request.json
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'هذا الإيميل غير مسجل'}), 404

    code = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    reset = ResetCode(email=email, code=code, expiry=expiry)
    db.session.add(reset)
    db.session.commit()

    if send_email_code(email, code):
        return jsonify({'message': 'تم إرسال الكود إلى بريدك الإلكتروني'})
    else:
        return jsonify({'message': 'فشل في إرسال الإيميل'}), 500

@app.route('/verify-reset-code', methods=['POST'])
def verify_code():
    data = request.json
    email = data.get('email')
    code = data.get('code')

    reset = ResetCode.query.filter_by(email=email, code=code).order_by(ResetCode.expiry.desc()).first()

    if reset and reset.expiry > datetime.utcnow():
        return jsonify({'message': 'الكود صحيح'})
    else:
        return jsonify({'message': 'الكود غير صحيح أو منتهي'}), 400

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'الإيميل غير مسجل'}), 404

    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed.decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'تم تغيير كلمة المرور بنجاح'})

if __name__ == '__main__':
    app.run(debug=True)
