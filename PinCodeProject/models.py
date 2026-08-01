from pydantic import BaseModel,field_validator

class PinCodeRequest(BaseModel):
    pincode:str

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value):
        if len(value)!=6 or not value.isdigit():
            raise ValueError("Pincode must be of 6 digits")
        return value  



class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str

class BulkRequest(BaseModel):
    pincodes:list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincode(cls,values):
        if len(values)==0:
            raise ValueError("At least one pincode is required")
        if len(values)>20:
            raise ValueError("Maximum 20 pincode is allowed, limit crossed")      
        for code in values:
            if len(code)!=6 or not code.isdigit():
                raise ValueError("Each Pincode must be of 6 digits")   
        return values   

class BulkResponse(BaseModel):
    status:str = "success"
    found:int
    not_found:int
    results:list[LocationResponse]
    missing:list[str]                      
