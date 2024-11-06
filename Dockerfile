# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3-slim

# Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# Install pip requirements
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt

# WORKDIR /app
# COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "function_app.py"]
FROM mcr.microsoft.com/azure-functions/python:4.0-python3.11

# RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev poppler-utils
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/site/wwwroot

# Set environment variables
# ENV AzureWebJobsStorage="UseDevelopmentStorage=true"
# ENV AzureFunctionsJobHost__Logging__Console__IsEnabled="true"
# ENV MY_CUSTOM_ENV_VAR="my_value"

# ENV AzureWebJobsScriptRoot=/home/site/wwwroot
# ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command to run the function host
# CMD ["python", "-m", "azure.functions"]
# Start the Azure Functions host
# CMD ["func", "host", "start", "--verbose"]