from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId  
from config import DATABASE_URL, DB_NAME, COLLECTION_NAME
from fastapi.staticfiles import StaticFiles
import uuid
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
payments = db[COLLECTION_NAME]


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/pay")
async def show_payment_page(
    request: Request,
    order_id: str = Form(...),
    amount: float = Form(...)
):
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
    payment_id = str(uuid.uuid4())
    
    payment_data = {
        "_id": payment_id,
        "order_id": order_id,
        "amount": amount,
        "status": True  
    }
    payments.insert_one(payment_data)
    
    return RedirectResponse(url=f"/success/{payment_id}", status_code=303)

@app.get("/success/{payment_id}")
def payment_success(request: Request, payment_id: str):
    
    payment = payments.find_one({"_id": payment_id})

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

from fastapi.responses import RedirectResponse

@app.get("/")
def redirect_to_main_site():
    main_site_url = "localhost:9078" 
    return RedirectResponse(url=main_site_url)
