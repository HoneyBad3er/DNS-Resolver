FROM python:3.10-slim

WORKDIR /app

COPY data ./
COPY dns_resolver ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 53/tcp
EXPOSE 53/udp

ENTRYPOINT ["python", "manage.py", "run"]
