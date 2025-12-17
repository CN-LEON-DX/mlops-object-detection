from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api import router

# docs: https://fastapi.tiangolo.com/advanced/events/#lifespan

@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.model_loader import load_production_model
    from src.state import ml_models
    ml_models["my_yolo11"] = load_production_model()
    print("[OK] load model successfully !")
    yield
    ml_models.clear()

app = FastAPI(
    title="API object detection",
    description="API for object detection with CICD",
    lifespan=lifespan
)

app.include_router(router)