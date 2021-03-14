import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))

from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Api, Resource

from audiofiles import Audio, Song, Podcast, Audiobook
from audiofiles import MetadataValueError, MetadataGenerationError

cluster = MongoClient(os.environ.get('AUDIOSERVERDB'))
collection = cluster["AudioServer"]["audiofiles"]


# noinspection PyMethodMayBeStatic
class Create(Resource):
    """ Resource for creating new audio files on the server """

    def post(self):
        """ RESTful POST Method. """
        data = request.get_json()

        try:
            audiotype: str = data['audioFileType']
            audiometadata: dict = data['audioFileMetadata']

        except KeyError as e:
            return f"Bad Request - {e} is required", 400

        if type(audiometadata) is not dict:
            return "Bad Request - 'audioFileMetadata' must contain a dict", 400

        try:
            if audiotype.lower() == "song":
                file = Song(audiometadata)
            elif audiotype.lower() == "podcast":
                file = Podcast(audiometadata)
            elif audiotype.lower() == "audiobook":
                file = Audiobook(audiometadata)
            else:
                return f"Bad Request - '{audiotype}' is not supported ", 400

        except MetadataValueError as e:
            return f"Bad Request - {e}", 400
        except MetadataGenerationError as e:
            return f"Internal Server Error - metadata generation - {e}", 500
        except Exception as e:
            return f"Internal Server Error - {e}"

        try:
            collection.insert_one(file.metadata)

        except Exception as e:
            return f"Internal Server Error - db write failed - {e}"

        return f"Create Successful. Created a/an {audiotype.capitalize()} file with ID {file.ID}", 200


# noinspection PyMethodMayBeStatic
class Delete(Resource):
    """ Resource for deleting audio files from the server """

    def get(self, audiotype: str, audioID: int):
        """ RESTful GET Method. """
        if audiotype.lower() not in ['song', 'podcast', 'audiobook']:
            return f"Bad Request - '{audiotype}' is not supported ", 400

        try:
            search = {"type": audiotype.capitalize(), "_id": audioID}
            search_result = collection.find_one_and_delete(search)

        except Exception as e:
            return f"Internal Server Error - db query failed - {e}"

        if search_result:
            return f"Delete Successful. Deleted a/an {audiotype.capitalize()} file with ID {search_result['_id']}", 200
        else:
            return f"Delete Successful. No document deleted"


# noinspection PyMethodMayBeStatic
class Update(Resource):
    """docstring"""
    pass


# noinspection PyMethodMayBeStatic
class Get(Resource):
    """ Resource for retrieving audio files from the server """

    def get(self, audiotype: str, audioID: int = None):
        """ RESTful GET Method. """
        if audiotype.lower() not in ['song', 'podcast', 'audiobook']:
            return f"Bad Request - '{audiotype}' is not supported ", 400

        try:
            if audioID:
                search = {"type": audiotype.capitalize(), "_id": audioID}
                result = collection.find_one(search)
            else:
                search = {"type": audiotype.capitalize()}
                search_result = collection.find(search)
                result = [res for res in search_result]

        except Exception as e:
            return f"Internal Server Error - db query failed - {e}", 500

        if result:
            return f"Search Successful. Found {len(result)} result(s). Results: {result}", 200
        else:
            return f"Search Successful. Found 0 result(s)", 200


app = Flask(__name__)
api = Api(app)

api.add_resource(Create, '/create')
api.add_resource(Delete, '/delete/<string:audiotype>/<int:audioID>')
api.add_resource(Get, '/get/<string:audiotype>', '/get/<string:audiotype>/<int:audioID>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
