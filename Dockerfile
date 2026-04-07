FROM python:3.10-slim

WORKDIR /app

COPY sistema_faculdade.py .

COPY funcoes/ ./funcoes/

CMD ["python", "sistema_faculdade.py"]