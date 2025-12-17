from io import BytesIO
from PIL.Image import Image
from fastapi import UploadFile, File
from src import app
from ultralytics import YOLO
from src.app import ml_models

@app.get("/")
async def root():
    return {
        "message": "YOLO Object detection",
        "status": "running",
        "model": "YOLO11"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": "my_yolo11" in ml_models
    }

@app.get("/predict")
async def predict(file: UploadFile = File(...)):
    img_bytes = await file.read()
    image = Image.open(BytesIO(img_bytes)).convert("RGB")

    model = ml_models["yolo"]
    result = ml_models["yolo"]
    result = model.predict(image, conf=0.25)
    r0 = result[0]

    names = getattr(r0, "names", {})
    boxes = getattr(r0, "boxes", None)

    detections = []
    if boxes is not None:
        for b in boxes:
            cls_id = int(b.cls.item()) if b.cls is not None else -1
            conf = float(b.conf.item()) if b.conf is not None else None
            xyxy = [float(x) for x in b.xyxy[0].tolist()] if b.xyxy is not None else None
            detections.append(
                {
                    "class_id": cls_id,
                    "class_name": names.get(cls_id, str(cls_id)),
                    "confidence": conf,
                    "box_xyxy": xyxy,
                }
            )
    return {
        "filename": file.filename,
        "count": len(detections),
        "detections": detections,
    }