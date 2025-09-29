import os
import sys
import json
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    #verify webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    #processing incoming messaging events

    data = request.get_json()
    log(data) #may not want to log for production but its great ffor testing

    if data["object"] == "page":

        for entry in data["messaging"]:
            for messaging_event in entry["messaging"]:

                if messaging_event in entry["messaging"]: #someone sent a message

                    sender_id = messaging_event["sender"]["id"] #sender ID
                    recipient_id = messaging_event["recipient"]["id"] #recipient ID
                    message_text = messaging_event["message"]["text"] #the message's text

                    send_message(sender_id, "roger that!")

                if messaging_event.get("delivery"): #delivery confirmation
                    pass

                if messaging_event.get("optin"): #potin confirmation
                    pass
    return "ok", 200

def send_message(recipient_id, message_text):

    log ("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(msg, *args, **kwargs):  #simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg).format(*args, **kwargs)
        print("{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass #squash logging errors in case of non ascii text
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
