# Use Python 3.9 base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Update package list and install necessary packages
RUN apt update && apt upgrade -y \
    && apt install -y git ffmpeg \
    && apt-get clean \
    && apt-get autoremove -y

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the application code
COPY . /app

# Use ENTRYPOINT instead of CMD to easily pass additional arguments
ENTRYPOINT ["python3", "bot.py"]
