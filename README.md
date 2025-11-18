# ArcGIS Token Service (FastAPI)


## Run locally


1. Build & run with Docker (recommended):


```bash
docker build -t arcgis-token-service .
docker run -p 8000:8000 arcgis-token-service


2. Build & run without Docker :


```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000