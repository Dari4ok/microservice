from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId  
from config import DATABASE_URL, DB_NAME, COLLECTION_NAME, MAIN_SERVER_URL
import requests
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Connect to MongoDB
client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
payments = db[COLLECTION_NAME]

@app.get("/pay/{order_id}")
def show_payment_page(request: Request, order_id: str):
    response = requests.get(f"{MAIN_SERVER_URL}/get_order/{order_id}")
    amount = response.json().get("amount", 0.0) if response.status_code == 200 else 0.0  

    return templates.TemplateResponse(
        "payment_form.html",
        {"request": request, "order_id": order_id, "amount": amount}
    )

@app.post("/process_payment")
def process_payment(order_id: str = Form(...), card_number: str = Form(...), expiry: str = Form(...), cvv: str = Form(...)):
    payment_id = str(ObjectId())  

    payment_data = {
        "_id": ObjectId(payment_id), 
        "order_id": order_id,
        "status": "successful"
    }
    payments.insert_one(payment_data)  

    requests.post(MAIN_SERVER_URL, json={"payment_id": payment_id, "order_id": order_id, "status": "successful"})
    
    return RedirectResponse(url=f"/success/{payment_id}", status_code=303)

@app.get("/success/{payment_id}")
def payment_success(request: Request, payment_id: str):
    try:
        payment = payments.find_one({"_id": ObjectId(payment_id)}) 
    except:
        return templates.TemplateResponse("payment_failed.html", {"request": request})

    if not payment:
        return templates.TemplateResponse("payment_failed.html", {"request": request})

    return templates.TemplateResponse(
        "payment_success.html",
        {
            "request": request,
            "order_id": payment["order_id"],
            "payment_id": payment_id,
            "amount": payment.get("amount", "Unknown"),
            "status": payment["status"],
        }
    )
