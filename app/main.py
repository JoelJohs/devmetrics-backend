import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DevMetrics API", version="1.0.0")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DevMetrics API", "version": app.version, "ok": True}

if __name__ == "__main__":
    env = os.getenv("ENV", "development")

    if env == "production":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run("main:app", host="0.0.0.0", port=port)

    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
