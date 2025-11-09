import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from .routers import ping_router, auth_router, project_router
base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "static"

static_dir.mkdir(parents=True, exist_ok=True)

load_dotenv()

app = FastAPI(title="DevMetrics API", version="1.0.0", description="API for DevMetrics application")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(ping_router.router, prefix="/api/v1", tags=["ping"])
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(project_router.router, prefix="/api/v1/projects", tags=["projects"])


@app.get("/", tags=["root"])
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

    app_str = "app.main:app"

    if env == "production":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app_str, host="0.0.0.0", port=port)

    else:
        uvicorn.run(app_str, host="0.0.0.0", port=8000, reload=True)
