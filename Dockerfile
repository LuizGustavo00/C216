FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY test_api.py .
COPY entrypoint.sh .
COPY sistema_faculdade.py .
COPY funcoes/ ./funcoes/

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]