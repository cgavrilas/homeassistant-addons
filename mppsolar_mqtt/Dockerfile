FROM python:3.11-slim
WORKDIR /app
COPY run.py .
RUN pip install paho-mqtt pyserial
CMD ["python", "run.py"]
