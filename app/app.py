from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile

# docs: https://fastapi.tiangolo.com/advanced/events/#lifespan
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    from ml.model_loader import load_production_model
    ml_models["yolo"] = load_production_model()
    yield
    ml_models.clear()

app = FastAPI(
    title="API object detection",
    description="API for object detection with CICD",
    lifespan=lifespan
)