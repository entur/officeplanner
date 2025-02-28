FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN python3 -m venv venv \
  && chown -R appuser:appgroup venv
USER appuser
COPY requirements.txt \
  officeplanner.py \
  pyproject.toml \
  requirements.in \
  ./
RUN source venv/bin/activate && pip install --upgrade --no-cache-dir pip pip-tools && pip-sync

CMD [ "venv/bin/python", "officeplanner.py" ]