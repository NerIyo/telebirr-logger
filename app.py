from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask import render_template
from flask import Flask, request, jsonify
from models import db, PaymentLog
from datetime import datetime

app = Flask(__name__)
app.secret_key = "telebirr-secret-key-123"  # You can change this to anything random
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Automatically create tables before first use
with app.app_context():
    db.create_all()

@app.route('/webhook/telebirr', methods=['POST'])
def telebirr_webhook():
    data = request.json
    # Check for existing transaction
    if PaymentLog.query.filter_by(transaction_id=data.get('transaction_id')).first():
        return jsonify({"error": "Duplicate transaction ID"}), 400

    log = PaymentLog(
        phone_number=data.get('phone_number'),
        amount=data.get('amount'),
        transaction_id=data.get('transaction_id'),
        status=data.get('status'),
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Logged successfully"}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "pass123":
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    logs = PaymentLog.query.order_by(PaymentLog.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)

@app.route('/logs', methods=['GET'])
def get_logs():
    query = PaymentLog.query

@app.route('/dashboard')
def dashboard():
    logs = PaymentLog.query.order_by(PaymentLog.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)


    # Filter by phone number
    phone = request.args.get('phone')
    if phone:
        query = query.filter(PaymentLog.phone_number == phone)

    # Filter by status
    status = request.args.get('status')
    if status:
        query = query.filter(PaymentLog.status == status)

    # Filter by date range
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(PaymentLog.timestamp >= start)
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(PaymentLog.timestamp <= end)

    logs = query.all()
    return jsonify([log.to_dict() for log in logs])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

