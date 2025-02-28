FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
COPY requirements.txt \
  officeplanner.py \
  ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "venv/bin/python", "officeplanner.py" ]