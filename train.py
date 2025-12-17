import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO
from dotenv import load_dotenv
load_dotenv()
from src.model_loader import download_from_s3

def chose_start_weights(pretrained_fallback: str) -> str:
    bucket = os.getenv("S3_BUCKET")
    key = os.getenv("S3_MODEL_KEY")
    local_model_path = Path(os.getenv("MODEL_PATH", "models/production.pt"))

    if bucket and key:
        try:
            download_from_s3(bucket=bucket, key=key, local_path=local_model_path)
            print(f"[OK] Fine-tune from production: s3://{bucket}/{key} -> {local_model_path}")
            return str(local_model_path)
        except Exception as e:
            print(f"[WARN] Could not download production model from S3, fallback to pretrained. Error: {e}")

    print(f"[INFO] Using pretrained fallback weights: {pretrained_fallback}")
    return pretrained_fallback


def main():
    parser = argparse.ArgumentParser(
        description="train YOLO"
    )
    parser.add_argument("--data", default=os.getenv("YOLO_DATA", "data/data.yaml"))
    parser.add_argument("--epochs", type=int, default=int(os.getenv("YOLO_EPOCHS", "10")))
    parser.add_argument("--imgsz", type=int, default=int(os.getenv("YOLO_IMGSZ", "640")))
    parser.add_argument("--batch", type=int, default=int(os.getenv("YOLO_BATCH", "16")))
    parser.add_argument("--device", default=os.getenv("YOLO_DEVICE", "cpu"))  # GPU example: "0"
    parser.add_argument("--patience", type=int, default=int(os.getenv("YOLO_PATIENCE", "20")))
    parser.add_argument("--project", default=os.getenv("YOLO_PROJECT", "runs/detect"))
    parser.add_argument("--name", default=os.getenv("YOLO_RUN_NAME", ""))
    parser.add_argument("--pretrained", default=os.getenv("YOLO_PRETRAINED", "yolo11n.pt"))
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {data_path.resolve()}")

    run_name = args.name.strip() or f"finetune_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    start_weights = chose_start_weights(pretrained_fallback=args.pretrained)

    # Train
    model = YOLO(start_weights)
    results = model.train(
        data=str(data_path),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        patience=args.patience,
        project=args.project,
        name=run_name,
        save=True,
        plots=True,
    )

    # Record outputs for next pipeline steps
    save_dir = Path(str(results.save_dir))
    best_pt = save_dir / "weights" / "best.pt"
    last_pt = save_dir / "weights" / "last.pt"

    payload = {
        "data_yaml": str(data_path),
        "start_weights": start_weights,
        "run_name": run_name,
        "save_dir": str(save_dir),
        "best_pt": str(best_pt) if best_pt.exists() else None,
        "last_pt": str(last_pt) if last_pt.exists() else None,
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "patience": args.patience,
    }

    Path("artifacts").mkdir(parents=True, exist_ok=True)
    out_path = Path("artifacts/train_out.json")
    out_path.write_text(json.dumps(payload, indent=2))

    print("[OK] Training completed.")
    print(f"[OK] Summary saved to: {out_path.resolve()}")
    if payload["best_pt"]:
        print(f"[OK] Best weights: {payload['best_pt']}")
    else:
        print("[WARN] best.pt not found. Check training logs/output directory.")


if __name__ == "__main__":
    print("Training ...")
    main()