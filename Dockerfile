# Use an official Python runtime as a parent image
FROM python:3.10.2

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Tesseract-OCR, Graphviz, and other system dependencies
RUN apt-get update \
    && apt-get install -y \
       tesseract-ocr \
       graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# Make sure you have a requirements.txt file in your project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Expose the port the app runs on
EXPOSE 8000

# Run the app using Gunicorn. Replace 'myapp:app' with your application's module and variable
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
