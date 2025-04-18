from fastapi import FastAPI

from ai_nutritionist.interfaces.whatsapp.whatsapp import whatsapp_router

app = FastAPI()
app.include_router(whatsapp_router)
