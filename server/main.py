from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, events, tickets, verify

app = FastAPI(title="NFT Ticketing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(verify.router)

@app.get("/")
async def root():
    return {
        "message": "AI-Verified NFT Ticketing System API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/wallet",
            "events": "/events",
            "tickets": "/tickets",
            "verify": "/verify"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
