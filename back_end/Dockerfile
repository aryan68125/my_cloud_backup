FROM python:3.12-slim

WORKDIR /app

COPY configs/requirements.txt ./configs/requirements.txt
RUN pip install --no-cache-dir -r configs/requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
