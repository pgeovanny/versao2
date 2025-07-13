# Use imagem oficial Python 3.11
FROM python:3.11-slim

# Instala dependências básicas do sistema para buildar PyMuPDF e outras libs
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho
WORKDIR /app

# Copia todos os arquivos para o container
COPY . .

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponha a porta padrão (altere para 10000 se preferir)
EXPOSE 10000

# Comando para iniciar o servidor FastAPI (Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
