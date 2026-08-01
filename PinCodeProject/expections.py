from fastapi.responses import JSONResponse
from fastapi import Request

class PincodeNotFoundError(Exception):
    def __init__(self,pincode:str):
        self.pincode=pincode

class InvalidPinCodeError(Exception):
    def __init__(self,pincode:str,reason:str="Invalid Pincode Format"):
        self.pincode=pincode
        self.reason=reason


##Custom handlers
async def pincode_not_found(request:Request,exp:PincodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error":"pincode_not_found",
            "message":f"Pincode not found:{exp.pincode}",
            "pincode":exp.pincode
            
            }
    )

async def invalid_pincode(request:Request,exp:InvalidPinCodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error":"invalid_pincode",
            "message":exp.reason,
            "pincode":exp.pincode
            
            }
    )    