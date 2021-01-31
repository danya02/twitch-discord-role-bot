from flask import Flask, request, abort
import database
import hmac
import functools

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Twitch!'

def validate_request():
    raw_data = request.get_data()
    json_data = request.get_json(force=True)
    signature = request.headers['Twitch-Eventsub-Message-Signature']
    timestamp = request.headers['Twitch-Eventsub-Message-Timestamp']
    msg_id = request.headers['Twitch-Eventsub-Message-Id']

    subscription = json_data['subscription']['id']
    secret = database.subscription_secrets[subscription]
    print(secret)
    message = bytes(msg_id, 'ascii') + bytes(timestamp, 'ascii') + raw_data
    hmac_obj = hmac.new(secret, message, 'sha256')
    hmac_str = 'sha256=' + hmac_obj.hexdigest()
    print(hmac_str, signature)
    if not hmac.compare_digest(hmac_str, signature):
        abort(403)
    
def requires_validation(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        validate_request()
        return func(*args, **kwargs)
    return inner


@app.route('/twitch/callback', methods=['POST'])
@database.is_used
@requires_validation
def twitch_callback():
    data = request.get_json(force=True)
    msg_type = request.headers['Twitch-Eventsub-Message-Type']
    if msg_type == 'webhook_callback_verification':
        challenge = data['challenge']
        print('Callback verification: challenge is', challenge)
        return challenge
    elif msg_type == 'notification':
        database.notifications.push(data)
        return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
