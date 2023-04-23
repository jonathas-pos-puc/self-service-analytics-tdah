FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY credentials.json /app/
COPY credentials.json .

# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]

