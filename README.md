### YOLO Object detection API with CI/CD

The main workflow is:
![main.png](main.png)
1. Push code/data → GitHub | using DVC to push new label data to S3
2. GitHub Actions → SSH Training Server
3. Server: dvc pull + train + mlflow log
4. Server: Register model to MLflow
5. Auto-promote a new model if better than production
6. Upload to S3
7. Application rebuild to using the latest model

Feature:
* FastAPI Backend
* YOLO model: YOLO11 for realtime object detection
* Docker
* CICD Pipeline: Complete actions workflow
* Automated Testing: Unit test with pytest
* Health Check: Built-in monitoring endpoint

API Endpoints:
* GET / - Root endpoint with API information
* GET /health - Health check endpoint
* GET /model-info - Get model information and available classes
* POST /predict - Upload image and get object detection results

Project structure:
```
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # CI/CD pipeline
├── data/                    # store in s3 and manage by DVC
│   ├── test/                # test
│       └── images       
│       └── labels       
│   └── train/               # train
│       └── images       
│       └── labels       
│   └── valid/               # val 
│       └── images       
│       └── labels
├── Dockerfile               # Container config
├── docker-compose.yml       # Local deployment
├── requirements.txt         # Python dependencies       
└── README.md
```

#### Prerequisite
* Python 3.12.3+ (I'm using)
* Docker & Docker compose

#### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/CN-LEON-DX/mlops-object-detection
   cd mlops-object-detection
   ```
2. **Install dependencies**
   ```bash
   conda create -n yolo-fastapi python=3.12.3 -y
   conda activate yolo-fastapi
   pip3 install -r requirements.txt
   ```
3. **Test VALID train yolo model**
   ```bash
   yolo detect train data=data/data.yaml model=yolo11n.pt epochs=3 imgsz=640
   ```
