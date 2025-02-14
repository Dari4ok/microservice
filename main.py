from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId  
from config import DATABASE_URL, DB_NAME, COLLECTION_NAME, MAIN_SERVER_URL
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
payments = db[COLLECTION_NAME]

@app.post("/pay")
async def show_payment_page(request: Request, data: dict = Body(...)):
    order_id = data.get("order_id")
    amount = data.get("amount", 0.0)
    return templates.TemplateResponse(
        "payment_form.html",
        {"request": request, "order_id": order_id, "amount": amount}
    )

@app.post("/process_payment")
def process_payment(
    order_id: str = Form(...),
    amount: float = Form(...),
    card_number: str = Form(...),
    expiry: str = Form(...),
    cvv: str = Form(...)
):
    
    payment_data = {
        "order_id": order_id,
        "amount": amount,
        "status": True  
    }
    payments.insert_one(payment_data)
    
    requests.post(MAIN_SERVER_URL, json={   
        "order_id": order_id,
        "status": True
    })
    
    return RedirectResponse(url=f"/success/{order_id}", status_code=303)

@app.get("/success/{payment_id}")
def payment_success(request: Request, payment_id: str):
    try:
        payment = payments.find_one({"_id": ObjectId(payment_id)})
    except Exception:
        return templates.TemplateResponse("payment_failed.html", {"request": request})
    
    if not payment:
        return templates.TemplateResponse("payment_failed.html", {"request": request})
    
    return templates.TemplateResponse(
        "payment_success.html",
        {
            "request": request,
            "order_id": payment["order_id"],
            "amount": payment.get("amount", "Unknown"),
            "status": payment["status"],
        }
    )
