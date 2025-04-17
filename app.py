from flask import render_template
from flask import Flask, request, jsonify
from models import db, PaymentLog
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Automatically create tables before first use
with app.app_context():
    db.create_all()

@app.route('/webhook/telebirr', methods=['POST'])
def telebirr_webhook():
    data = request.json
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

