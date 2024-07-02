# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434

# Run main.py when the container launches
CMD ["python", "agents.py"]
