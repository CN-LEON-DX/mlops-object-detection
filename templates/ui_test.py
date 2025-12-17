import base64
import os
from pathlib import Path
from typing import Any

import requests
import uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

app = FastAPI(title="YOLO Web UI", description="Basic UI for upload & visualize detections")
TEMPLATES_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "api_base": API_BASE})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    img_bytes = await file.read()

    # Call YOLO API (8000)
    resp = requests.post(
        f"{API_BASE}/predict",
        files={"file": (file.filename, img_bytes, file.content_type or "image/jpeg")},
        timeout=120,
    )
    resp.raise_for_status()
    payload: dict[str, Any] = resp.json()

    # Embed image for display
    mime = file.content_type or "image/jpeg"
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    image_data_url = f"data:{mime};base64,{img_b64}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "api_base": API_BASE,
            "filename": payload.get("filename", file.filename),
            "count": payload.get("count", 0),
            "detections": payload.get("detections", []),
            "image_data_url": image_data_url,
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)