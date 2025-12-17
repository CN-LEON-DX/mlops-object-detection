from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile

# docs: https://fastapi.tiangolo.com/advanced/events/#lifespan
ml_models = {}


def fake_answer():
    return 1 + 1

@asynccontextmanager
async def lifespan(app: FastAPI):

    # load ml model
    ml_models["answer"] = fake_answer
    yield

    ml_models.clear()



app = FastAPI(
    title="API object detection",
    description="API for object detection with CICD",
    lifespan=lifespan
)