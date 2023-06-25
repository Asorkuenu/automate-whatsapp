from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["get","post"])
def reply():
    response = MessagingResponse()
    response.message("Hello")
    return str(response)

if __name__ =="__main__":
    app.run()
    
