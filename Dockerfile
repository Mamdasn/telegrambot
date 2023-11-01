# syntax=docker/dockerfile:1
FROM python:3.11-alpine

# Install nginx
RUN apk --no-cache add nginx

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Copy the Nginx configuration file
COPY portforwarding.conf /etc/nginx/nginx.conf

# Copy configuration files
COPY SSLFILES/YOURPUBLIC.pem /etc/nginx/cert.pem
COPY SSLFILES/YOURPRIVATE.key /etc/nginx/cert.key

EXPOSE 443

# Create a directory in the container to log the output of the code
RUN mkdir -p /app/output

# Specify the command to run on container start
CMD ["sh", "-c", "nginx && python3 telegram-bot-run.py >> /app/output/telegram.logs 2>&1"]
