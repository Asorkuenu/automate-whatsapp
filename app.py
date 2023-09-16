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
                                    "1️⃣ Guarding Services\n"
                                    "2️⃣ Security Technologies Integration Services\n"
                                    "3️⃣ Private Investigations Services\n"
                                    "4️⃣ Valuables-in-Transit Services")
            users.update_one({"number": number}, {"$set": {"status": "services"}})
        elif option == 2:
            res["reply"] += '\n' + ("Contact Offin Security Services Ltd.\n\n"
                                    "📞 Tel: 020-359-8142\n"
                                    "📧 Email: info@offinsecuritygh.com\n"
                                    "🌐 Website: www.offinsecuritygh.com")
        else:
            res["reply"] += '\n' + ("Please enter a valid response")
    elif user["status"] == "services":
        try:
            option = int(text)
        except:
            res["reply"] += '\n' + ("Please enter a valid response")
            return str(res)

        if option == 1:
            res["reply"] += '\n' + ("**Guarding Services:**\n\n"
                                    "Our Guarding Services have earned the trust of notable clients including BOST, GCB, SSNIT, GRIDCo, KATH, GIPC, and Omni Energy. With a team of highly trained security personnel, we provide top-tier protection and surveillance, ensuring the safety and security of your assets and premises 24/7.")
        elif option == 2:
            res["reply"] += '\n' + ("**Security Technologies Integration Services:**\n\n"
                                    "Our Security Technologies Integration Services offer cutting-edge solutions to enhance your security infrastructure. We seamlessly integrate advanced security technologies to provide real-time monitoring, access control, and threat detection. With our expertise, you can achieve unmatched security and peace of mind.")
        elif option == 3:
            res["reply"] += '\n' + ("**Private Investigations Services:**\n\n"
                                    "Our Private Investigations Services provide discreet and professional solutions to uncover the truth. Whether it's corporate fraud, background checks, or personal matters, our experienced investigators employ industry-leading techniques to deliver accurate and confidential results.")
        elif option == 4:
            res["reply"] += '\n' + ("**Valuables-in-Transit Services:**\n\n"
                                    "Our Valuables-in-Transit Services ensure the safe and secure transport of your valuable assets. With a proven track record, we offer comprehensive logistics solutions, armed escorts, and state-of-the-art security measures to safeguard your valuables throughout their journey. Your assets are in trusted hands with us.")
        else:
            res["reply"] += '\n' + ("Please enter a valid response")

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)

if __name__ == "__main__":
    app.run()
