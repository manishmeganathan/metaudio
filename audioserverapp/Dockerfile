# Building custom base image based on Python 3.8
FROM python:3.8-slim

# Setting an environment variables APPDIR and APPNAME
ENV APPDIR /app
ENV APPNAME audioserver

# Change working directory to APPDIR
WORKDIR $APPDIR

# Move the package and server script into the APPDIR
COPY ./audiofiles  $APPDIR/audiofiles
COPY ./audioserver $APPDIR

# Update pip and install dependancies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run a GUnicorn WSGI Server. Timeout is set to 60s
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class gthread --threads 4 --timeout 60 $APPNAME:app