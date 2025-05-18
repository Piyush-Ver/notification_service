from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
import random
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class NotificationType(enum.Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    INAPP = "INAPP"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def process_notification(notification):
    try:
        if notification.type == NotificationType.EMAIL:
            send_email(notification)
        elif notification.type == NotificationType.SMS:
            send_sms(notification)
        elif notification.type == NotificationType.INAPP:
            send_inapp(notification)
        notification.status = "SENT"
    except Exception as exc:
        notification.status = "FAILED"
    db.session.commit()

def send_email(notification):
    if random.random() < 0.1:
        raise Exception("Email sending failed")
    print("Email sent to user", notification.user_id, "with subject:", notification.subject)

def send_sms(notification):
    if random.random() < 0.1:
        raise Exception("SMS sending failed")
    print("SMS sent to user", notification.user_id)

def send_inapp(notification):
    if random.random() < 0.1:
        raise Exception("In-app notification sending failed")
    print("In-app notification processed for user", notification.user_id)

@app.route('/notifications', methods=['POST'])
def send_notification_endpoint():
    data = request.get_json()
    if not data.get('userId') or not data.get('type') or not data.get('message'):
        return jsonify({"error": "Missing field"}), 400
    try:
        notif_type = NotificationType[data['type']]
    except KeyError:
        return jsonify({"error": "Invalid type. Allowed values: EMAIL, SMS, INAPP."}), 400
    notification = Notification(
        user_id=data['userId'],
        type=notif_type,
        subject=data.get('subject'),
        message=data['message'],
        status="PENDING"
    )
    db.session.add(notification)
    db.session.commit()
    process_notification(notification)
    return jsonify({
        "id": notification.id,
        "userId": notification.user_id,
        "type": notification.type.name,
        "subject": notification.subject,
        "message": notification.message,
        "status": notification.status,
        "createdAt": notification.created_at.isoformat()
    }), 201

@app.route('/users/<int:user_id>/notifications', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    result = []
    for notif in notifications:
        result.append({
            "id": notif.id,
            "userId": notif.user_id,
            "type": notif.type.name,
            "subject": notif.subject,
            "message": notif.message,
            "status": notif.status,
            "createdAt": notif.created_at.isoformat()
        })
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
