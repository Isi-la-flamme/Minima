FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .
CMD ["minima", "run", "--config", "config/config.yaml"]
