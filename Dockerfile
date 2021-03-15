# Building custom base image based on Python 3.8
FROM python:3.8-slim

# Setting the environment variables
ENV PORT 8080
ENV APPDIR /app
ENV APPNAME audioserver

# Change working directory to APPDIR
WORKDIR $APPDIR

# Move contents into the APPDIR
COPY . $APPDIR

# Update pip and install dependancies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run a GUnicorn WSGI Server. Timeout is set to 60s
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class gthread --threads 4 --timeout 60 $APPNAME:app