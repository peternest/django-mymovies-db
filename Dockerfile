ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
COPY --chmod=755 wait-for-it.sh ./
COPY ./src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

ENV PYTHONPATH=/app/src:$PYTHONPATH

# Services are run from docker-compose.yaml
# EXPOSE 8000
# CMD ["python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]
