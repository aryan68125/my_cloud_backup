FROM python:3.12-slim

WORKDIR /app

COPY configs/requirements.txt ./configs/requirements.txt
RUN pip install --no-cache-dir -r configs/requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", \
     "alembic upgrade head && \
      python back_end_initialization/seed_data.py && \
      uvicorn main:app --host 0.0.0.0 --port 8000"]
