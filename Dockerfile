# Use a lightweight official Python image
FROM python:3.11-slim
# Set the working directory inside the container
WORKDIR /app
# Copy dependency list and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of your application code
COPY main.py .
# Run the single-pass script when the container launches
CMD ["python", "main.py"]