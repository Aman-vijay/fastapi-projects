from fastapi import HTTPException, Header

API_KEY = "1234567890"

def verify_api_key(x_api_key: str = Header()):
    """Verify the API key is valid"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key