FROM python:3.12-slim

WORKDIR /app

# Sistemske knjižnice, ki jih pogosto rabijo Pillow / OpenCV / torch dependencyji
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Najprej kopiramo requirements, da Docker bolje uporablja cache
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Kopiramo aplikacijsko kodo
COPY server /app/server
COPY inteligent_component /app/inteligent_component

EXPOSE 12000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "12000"]
