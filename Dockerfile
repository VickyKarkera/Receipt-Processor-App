# syntax=docker/dockerfile:1

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /receipt-app

# Copy the current directory contents into the container
RUN pip install flask 

COPY . .

# Run the application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]



