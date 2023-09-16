from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://savior:savior@cluster0.9y1vsjs.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
db = cluster["security"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("message")
    number = request.form.get("sender")
    res = {"reply": ""}
    user = users.find_one({"number": number})
    
    if not user:
        res["reply"] += '\n' + ("Hi, thanks for contacting *Offin Security Services Ltd.*\n"
                                "How can we assist you today? Choose an option:\n"
                                "1️⃣ Services\n2️⃣ Contact Information")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res["reply"] += '\n' + ("Please enter a valid response")
            return str(res)

        if option == 1:
            res["reply"] += '\n' + ("Our Services:\n\n"
                                    "1️⃣ Guarding\n"
                                    "2️⃣ Security Technologies Integration\n"
                                    "3️⃣ Private Investigations\n"
                                    "4️⃣ Valuables-in-Transit\n"
                                    "Price for our services depends on assessment. 🕵️‍♂️")
        elif option == 2:
            res["reply"] += '\n' + ("Contact Offin Security Services Ltd.\n\n"
                                    "📞 Tel: 020-359-8142\n"
                                    "📧 Email: info@offinsecuritygh.com\n"
                                    "🌐 Website: www.offinsecuritygh.com")
        else:
            res["reply"] += '\n' + ("Please enter a valid response")
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)

if __name__ == "__main__":
    app.run()
