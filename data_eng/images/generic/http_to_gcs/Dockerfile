# The file Dockerfile defines the image's environment
FROM python:3.6-slim

# Install any necessary dependencies
RUN pip install google-cloud-storage
RUN pip install requests

COPY . .

# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]
