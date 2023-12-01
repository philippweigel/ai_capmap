# Use an official Python runtime as a parent image
FROM python:3.10.2

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Tesseract-OCR
RUN apt-get update \
    && apt-get install -y tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# Make sure you have a requirements.txt file in your project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run the app. Replace "app.py" with your application script
CMD ["python", "./app.py"]
