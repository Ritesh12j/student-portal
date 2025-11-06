FROM python:3.13-slim

WORKDIR /app

# copy dependency info and install first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# ensure instance folder exists and has correct permissions
RUN mkdir -p /app/instance

EXPOSE 5000

# use gunicorn for production in container
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app", "--workers=4", "--timeout=120"]
