FROM python:3.9-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
COPY screenshot_rename.py .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "screenshot_rename.py"]
