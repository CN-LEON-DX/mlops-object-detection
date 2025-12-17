import os
from pathlib import Path

import boto3
from ultralytics import YOLO


def download_from_s3(bucket: str, key: str, local_path: Path) -> Path:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, str(local_path))
    return local_path

def load_production_model() -> YOLO:
    bucket = os.getenv("S3_BUCKET")
    key = os.getenv("S3_MODEL_KEY")
    local = Path(os.getenv("MODEL_PATH", "models/production.pt"))

    if bucket and key:
        download_from_s3(bucket=bucket, key=key, local_path=local)

    if not local.exists():
        raise FileNotFoundError(
            "Model file not found. :(( "
        )
    return YOLO(str(local))