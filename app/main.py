import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "static"

static_dir.mkdir(parents=True, exist_ok=True)

load_dotenv()

app = FastAPI(title="DevMetrics API", version="1.0.0")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DevMetrics API", "version": app.version, "ok": True}


@app.get("/favicon.ico")
async def favicon():
    f = static_dir / "favicon.ico"

    if f.exists():
        return FileResponse(f)

    return Response(status_code=404)

if __name__ == "__main__":
    env = os.getenv("ENV", "development")

    if env == "production":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run("main:app", host="0.0.0.0", port=port)

    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
