from .common import Notification
import json

def push(data):
    Notification.create(data=json.dumps(data))

def pop():
    try:
        notification_row = Notification.select().order_by(Notification.added_at).get()
        notification_row.delete_instance()
        return json.loads(notification_row.data)
    except Notification.DoesNotExist: return None
