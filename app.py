import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    #verify webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    
    return "Hello world", 200

#@app.route('/', methods=['POST'])
#def webhook():
    #processing incoming messaging events

 #   data = requests.get_json()
  #  log(data) #may not want to log for production but its great ffor testing

   # if data["object"] == "page":