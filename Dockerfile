FROM python:3.9.19-alpine3.20

WORKDIR ./

COPY . .

RUN pip install requirements.txt

CMD ["./run.sh"]