FROM python:3.12.8-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["./run.sh"]