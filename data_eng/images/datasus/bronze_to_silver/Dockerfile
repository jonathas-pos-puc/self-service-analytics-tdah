FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY credentials.json /app/
COPY credentials.json .

CMD ["python", "app.py"]
