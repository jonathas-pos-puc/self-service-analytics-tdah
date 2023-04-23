FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY credentials.json /app/
COPY credentials.json .

# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]
