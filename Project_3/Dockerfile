# Use the official Python 3.10 image with Alpine Linux
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app/

# Copy the current directory contents into the container at /app
COPY hw3.py /app/

# Copy specific files from host into the container at /home/data
COPY IF.txt Limerick-1.txt /home/data/

# Start Almquist Shell
CMD ["python", "hw3.py"]
