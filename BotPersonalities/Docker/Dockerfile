# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /botpersonalities

# Copy the application files
COPY . /botpersonalities

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the network port
EXPOSE 8000

# Specify the command to run the application
CMD ["python", "eventHandler_newMsg.py"]
