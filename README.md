# AudioServer
## A Flask-RESTful App Server that serves audio file metadata from a MongoDB server.
 
**Platform: Google Cloud Platform Cloud Run**  
**Language: Python 3.8**

This repository contains a python package **audiofiles** which contains the classes *Song*, *Podcast* and 
*Audiobook* all of which derive from *Audio*. These classes are simple dataclasses which abstract the 
validation and generation of metadata values for these Audio classes. 

The directory **audioserverapp** contains a flask server script and a Dockerfile to containerise the server.

### Dependencies
- PyMongo
- Flask
- Flask-RESTful


