FROM python:3-alpine as main

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY officeplanner.py officeplanner.py

FROM main as lint
RUN pip3 install pylint
RUN python -m pylint officeplanner.py

FROM main as run

CMD [ "python3", "officeplanner.py" ]
