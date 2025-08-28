import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vapi import Vapi
from dotenv import load_dotenv
load_dotenv(override=True)
# Load from ENV
VAPI_KEY = os.getenv("key")
ASSISTANT_ID = os.getenv("assistant_id")
PHONE_NUMBER_ID = os.getenv("phone_number_id")


print("VAPI_KEY",VAPI_KEY)
print("ASSISTANT_ID",ASSISTANT_ID)
print("PHONE_NUMBER_ID",PHONE_NUMBER_ID)


client = Vapi(token=VAPI_KEY)

print("client:",client)

app = FastAPI()

# Allow CORS (for frontend use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CallRequest(BaseModel):
    phone: str

@app.post("/start-call")
async def start_call(req: CallRequest):
    """
    Starts a call to the provided phone number.
    """
    try:
        print("phno : req.phone",req.phone)
        call = client.calls.create(
            assistant_id=ASSISTANT_ID,
            phone_number_id=PHONE_NUMBER_ID,
            customer={"number": req.phone},
        )

        print("Call initiated with ID:", call.id)
        return {"status": "success", "call_id": call.id}
    except Exception as e:
        print("error:", str(e))
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)