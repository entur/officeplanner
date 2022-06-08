FROM python:3-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY officeplanner.py officeplanner.py

CMD [ "python3", "officeplanner.py" ]
