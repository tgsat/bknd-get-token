# ArcGIS Token Service (FastAPI)


## Run locally

arcgis-fastapi/
├── 📁 app/
│   ├── 📁 api/
│   │   ├── 📁 v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── token.py
│   │   │   │   └── users.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── 📁 core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── __init__.py
│   ├── 📁 models/
│   │   ├── schemas.py
│   │   └── __init__.py
│   ├── 📁 services/
│   │   ├── arcgis_service.py
│   │   ├── cache_service.py
│   │   └── __init__.py
│   ├── 📁 utils/
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── __init__.py
│   └── __init__.py
├── 📁 tests/
│   ├── test_auth.py
│   ├── test_token.py
│   └── __init__.py
├── 📁 docs/
├── 📁 logs/
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── railway.json
├── main.py
└── README.md


1. Build & run with Docker (recommended):


```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Push ke GitHub, lalu deploy otomatis di Railway
git add .
git commit -m "Deploy ArcGIS API"
git push origin main