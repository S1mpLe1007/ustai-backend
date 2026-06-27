from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import hisob, smeta, ai_dizayn

app = FastAPI(
    title="Remont Kalkulyator API",
    description="Qurilish materiallari hisob-kitob API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],


)

app.include_router(hisob.router, prefix="/hisob", tags=["Hisob-kitob"])
app.include_router(smeta.router, prefix="/smeta", tags=["Smeta"])
app.include_router(ai_dizayn.router, prefix="/ai", tags=["AI Dizayn"])

@app.get("/")
def root():
    return {"xabar": "Remont Kalkulyator API ishlamoqda!"}
