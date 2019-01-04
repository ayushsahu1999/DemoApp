import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAY3gBrLA7EBAH7lJkRL4dZAswAfnJndXZCqrxaYaro9WLkKiEt1M6HImAZCybTzD9BZCruLwXG1rlAgaXfP8x7TkKQZBkb9L4r8m9keYBlUlr0m9AbEMJdVuuHHKO23m7P0jA32vL23KsRTggK5LKh9eszcsSc9sTxSlZC6h2MAZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods = ['GET'])
def verify():

    #Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        #verify_token is hello
        if not request.args.get("hub.verify_token") == "hello":
            return "verification token mismatch", 430
        return request.args["hub.challenge"], 200
    return "Hello world", 200

#for processing messeges sent by fb app
@app.route('/', methods = ['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
          for entry in data['entry']:
              for messaging_event in entry['messaging']:

                  #ID's
                  sender_id = messaging_event['sender']['id']
                  recipient_id = messaging_event['recipient']['id']

                  if messaging_event.get('message'):
                      if 'text' in messaging_event['message']:
                          messaging_text = messaging_event['message']['text']
                      else:
                          messaging_text = 'no text'

                      #witbot
                      response = None

                      entity, value = wit_response(messaging_text)

                      if entity == "languageName":
                          response = "Ok, I will teach you {0}".format(str(value))
                      elif entity == "location":
                          response = "Ok, you live in {0}. I will send you top headlines from your location".format(str(value))
                      elif entity == "greetings":
                          response = "Hello, I am Ayush's page" 
                      if response == None:
                          response = "Sorry, I didn't understand"
                      bot.send_text_message(sender_id, response)

    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()



if __name__ == "__main__":
    app.run(debug = True, port = 80)
