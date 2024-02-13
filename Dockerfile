FROM python:3-alpine

WORKDIR /app
RUN pip3 install --no-cache-dir slack_sdk pylint

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY officeplanner.py officeplanner.py
RUN python -m pylint officeplanner.py

ENTRYPOINT [ "python3", "officeplanner.py" ]
