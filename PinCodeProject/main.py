from fastapi import FastAPI
import uvicorn
from expections import (
    PincodeNotFoundError,pincode_not_found,InvalidPinCodeError,invalid_pincode
)
from data import pincode_db
from models import BulkRequest,BulkResponse,LocationResponse

app = FastAPI(
    title = "Pin code Project",
    description=" This fetches pin code of places"

)

#registering custom exception handler
app.add_exception_handler(PincodeNotFoundError,pincode_not_found)
app.add_exception_handler(InvalidPinCodeError,invalid_pincode)


@app.get("/")
def root():
    return {"message":"Pincode api lookup running"}

@app.get("/pincode/{code}",response_model=LocationResponse)
def get_pincode(code:str):
    if len(code)!=6 or not code.isdigit():
        raise InvalidPinCodeError(code,"Must be of 6 digits")
    if code not in pincode_db:
        raise PincodeNotFoundError(code,"Pincode not found")
    return pincode_db[code]    

@app.post("/pincode/bulk",response_model=BulkResponse) 
def get_bulk_pincode(request:BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
    return BulkResponse(
        found = len(results),
        not_found = len(missing),
        results = results,
        missing = missing



    )              

        

