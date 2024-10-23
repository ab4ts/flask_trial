# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the uploads directory and set appropriate permissions
RUN mkdir -p /app/uploads && chmod -R 775 /app/uploads

RUN chmod -R 775 /app/uploads

# Expose the port that Flask will run on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Run the command to start the Flask app
CMD ["python", "app.py"]
