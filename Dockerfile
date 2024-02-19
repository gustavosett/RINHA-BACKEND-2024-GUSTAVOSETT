# Use an official Python runtime as a parent image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Python packages that need compilation
# Update package lists, install build-essential (includes gcc) and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . .

# Crie um ambiente virtual
RUN python3 -m venv myenv

# Activate the virtual environment
SHELL ["bash", "-c"]
RUN source myenv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o script wait-for-it.sh para o diretório atual antes de construir a imagem
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Make port 9999 available to the world outside this container
EXPOSE 9999

# Define environment variable
ENV NAME World

# Use the entrypoint script to start the app
ENTRYPOINT ["entrypoint.sh"]
