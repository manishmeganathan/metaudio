"""
A Flask-RESTful App Server that serves audio file metadata from a MongoDB server

Author: Manish Meganathan
License: MIT License
"""
import os

from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Api, Resource

from audiofiles import Song, Podcast, Audiobook
from audiofiles import MetadataValueError, MetadataGenerationError

cluster = MongoClient(os.environ.get('AUDIOSERVERDB'))
collection = cluster["AudioServer"]["audiofiles"]


def generate400response(error: str) -> dict:
    """ A function that generates a '400-Bad Request' message and returns it as a dict """
    return {
        "status": 400,
        "message": "Bad Request",
        "error": error
    }


def generate500response(error: str) -> dict:
    """ A function that generates a '500-Internal Server Error' message and returns it as a dict """
    return {
        "status": 500,
        "message": "Internal Server Error",
        "error": error
    }


def generateAudio(audiotype: str, audiometadata: dict):
    """ A function that generates an Audio object, one of Song, Podcast and Audiobook
    and returns it. Returns None if the 'audiotype' is invalid. """
    try:
        audiotype = audiotype.lower()

        if audiotype == "song":
            file = Song(audiometadata)
        elif audiotype == "podcast":
            file = Podcast(audiometadata)
        elif audiotype == "audiobook":
            file = Audiobook(audiometadata)
        else:
            return None

        return file

    except MetadataValueError as error:
        raise MetadataValueError(error)

    except MetadataGenerationError as error:
        raise MetadataGenerationError(error)


# noinspection PyMethodMayBeStatic
class Create(Resource):
    """ Resource for creating new audio files on the server """
    def post(self):
        """ RESTful POST Method. """
        data = request.get_json()

        try:
            audiotype: str = data['audioFileType']
            audiometadata: dict = data['audioFileMetadata']
            audiotype = audiotype.capitalize()

        except KeyError as key:
            response = generate400response(f"{key} is required")
            return response, 400

        if not isinstance(audiometadata, dict):
            response = generate400response("'audioFileMetadata' must be a dict")
            return response, 400

        try:
            audiofile = generateAudio(audiotype, audiometadata)

            if not audiofile:
                response = generate400response(f"'{audiotype}' is not supported")
                return response, 400

        except MetadataValueError as error:
            response = generate400response(f"{error}")
            return response, 400

        except MetadataGenerationError as error:
            response = generate500response(f"metadata generation for {audiotype} - {error}")
            return response, 500

        insert_result = collection.insert_one(audiofile.metadata)

        if not insert_result.acknowledged:
            response = generate500response("database insertion failed")
            return response, 500

        return {
            "status": 200,
            "message": "Create Complete",
            "result": f"{audiotype} file with ID {insert_result.inserted_id} has been created",
            "document": insert_result.inserted_id
        }, 200


# noinspection PyMethodMayBeStatic
class Delete(Resource):
    """ Resource for deleting audio files from the server """
    def get(self, audiotype: str, audioID: int):
        """ RESTful GET Method. """
        audiotype = audiotype.capitalize()

        if audiotype.lower() not in ['song', 'podcast', 'audiobook']:
            response = generate400response(f"'{audiotype}' is not supported")
            return response, 400

        try:
            search_filter = {"type": audiotype, "_id": audioID}
            delete_result = collection.find_one_and_delete(search_filter)

        except Exception as error:
            response = generate500response(f"database query and delete failed - {error}")
            return response, 500

        if not delete_result:
            return {
                "status": 200,
                "message": "Delete Complete",
                "result": f"No document deleted"
            }, 200

        return {
            "status": 200,
            "message": "Delete Complete",
            "result": f"{audiotype} file with ID {delete_result['_id']} has been deleted",
            "document": delete_result['_id']
        }, 200


# noinspection PyMethodMayBeStatic
class Update(Resource):
    """ Resource for updating audio files on the server """
    def post(self, audiotype: str, audioID: int):
        """ RESTful POST Method. """
        audiotype = audiotype.capitalize()

        if audiotype.lower() not in ['song', 'podcast', 'audiobook']:
            response = generate400response(f"'{audiotype}' is not supported")
            return response, 400

        data = request.get_json()

        try:
            param_audiotype: str = data['audioFileType']
            audiometadata: dict = data['audioFileMetadata']

        except KeyError as key:
            response = generate400response(f"{key} is required")
            return response, 400

        if param_audiotype.capitalize() != audiotype:
            response = generate400response("'audioFileType' field must match the endpoint")
            return response, 400

        if not isinstance(audiometadata, dict):
            response = generate400response("'audioFileMetadata' must be a dict")
            return response, 400

        try:
            search_filter = {"type": audiotype, "_id": audioID}
            old_document = collection.find_one(search_filter)

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        if not old_document:
            response = generate400response(f"No document found for ID - {audioID}")
            return response, 400

        try:
            new_audiofile = generateAudio(audiotype, audiometadata)

            if not new_audiofile:
                response = generate400response(f"'{audiotype}' is not supported")
                return response, 400

            new_document = new_audiofile.metadata
            new_document['_id'] = old_document['_id']

        except MetadataValueError as error:
            response = generate400response(f"{error}")
            return response, 400

        except MetadataGenerationError as error:
            response = generate500response(f"metadata generation for {audiotype} - {error}")
            return response, 500

        except Exception as error:
            response = generate500response(f"document update failed - {error}")
            return response, 500

        try:
            pre_update_doc = collection.find_one_and_replace(search_filter, new_document)

        except Exception as error:
            response = generate500response(f"database query and replace failed - {error}")
            return response, 500

        return {
            "status": 200,
            "message": "Update Complete",
            "result": f"{audiotype} file with ID {audioID} has been updated",
            "pre-update": pre_update_doc,
            "post-update": new_document,
            "document": audioID
        }, 200


# noinspection PyMethodMayBeStatic
class Get(Resource):
    """ Resource for retrieving audio files from the server """
    def get(self, audiotype: str, audioID: int = None):
        """ RESTful GET Method. """
        audiotype = audiotype.capitalize()

        if audiotype.lower() not in ['song', 'podcast', 'audiobook']:
            response = generate400response(f"'{audiotype}' is not supported")
            return response, 400

        try:
            if audioID:
                search = {"type": audiotype, "_id": audioID}
                result = collection.find_one(search)
                result = [result] if result else []
            else:
                search = {"type": audiotype}
                search_result = collection.find(search)
                result = [res for res in search_result]

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        if not result:
            return {
                "status": 200,
                "message": "Get Complete",
                "result": f"No result(s) found"
            }, 200

        return {
            "status": 200,
            "message": "Get Complete",
            "result": f"{len(result)} result(s) found",
            "documents": result
        }, 200


app = Flask(__name__)
api = Api(app)

api.add_resource(Create, '/create')
api.add_resource(Delete, '/delete/<string:audiotype>/<int:audioID>')
api.add_resource(Update, '/update/<string:audiotype>/<int:audioID>')
api.add_resource(Get, '/get/<string:audiotype>', '/get/<string:audiotype>/<int:audioID>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
