FROM --platform=linux/amd64 python:3.12-slim as build

WORKDIR /src

COPY requirements/requirements.txt .

RUN pip install --no-cache-dir uvicorn fastapi

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]