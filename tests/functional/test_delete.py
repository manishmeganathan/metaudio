"""
Functional Test Module for the /delete endpoint of the AudioServer
Test Framework: pyTest
"""
import json
import random


def test_Delete_Song(client):
    """
    **GIVEN** a Flask application configured for testing and a Song file has been created\n
    **WHEN** the delete endpoint is hit with a GET request for deleting the Song\n
    **THEN** check that the response is valid for a 200 response (OK), perform a delete
    on the file again and check the null delete response.
    """
    # Create a Song file
    name = f"test-song-{random.randint(100, 999)}"
    request = {"audioFileType": "Song", "audioFileMetadata": {"name": f"{name}", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Delete the file
    response = client.get(f"/delete/song/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"Song file with ID {docID} has been deleted"
    assert data['document'] == docID

    # Attempt to delete the file again
    response = client.get(f"/delete/song/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert 'document' not in data

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"No document deleted"


def test_Delete_Podcast(client):
    """
    **GIVEN** a Flask application configured for testing and a Podcast file has been created\n
    **WHEN** the delete endpoint is hit with a GET request for deleting the Podcast\n
    **THEN** check that the response is valid for a 200 response (OK), perform a delete
    on the file again and check the null delete response.
    """
    # Create a Podcast file
    name = f"test-podcast-{random.randint(100, 999)}"
    request = {"audioFileType": "Podcast",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "host": "host1", "participants": ["cast1"]}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Delete the file
    response = client.get(f"/delete/podcast/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"Podcast file with ID {docID} has been deleted"
    assert data['document'] == docID

    # Attempt to delete the file again
    response = client.get(f"/delete/podcast/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert 'document' not in data

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"No document deleted"


def test_Delete_Audiobook(client):
    """
    **GIVEN** a Flask application configured for testing and an Audiobook file has been created\n
    **WHEN** the delete endpoint is hit with a GET request for deleting the Audiobook\n
    **THEN** check that the response is valid for a 200 response (OK), perform a delete
    on the file again and check the null delete response.
    """
    # Create an Audiobook file
    name = f"test-book-{random.randint(100, 999)}"
    request = {"audioFileType": "Audiobook",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "author": "author1", "narrator": "narrator1"}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Delete the file
    response = client.get(f"/delete/audiobook/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"Audiobook file with ID {docID} has been deleted"
    assert data['document'] == docID

    # Attempt to delete the file again
    response = client.get(f"/delete/audiobook/{docID}")

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert 'document' not in data

    assert data['status'] == 200
    assert data['message'] == f"Delete Complete"
    assert data['result'] == f"No document deleted"


def test_Delete_invalid_type(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the create endpoint is hit with a GET request with an invalid 'type' parameter\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    response = client.get(f"/delete/pod/1010101010")

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'Pod' is not supported"


def test_Delete_POST(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the delete endpoint is hit with a POST request\n
    **THEN** check that the response is valid for a 405 response (Method not Allowed)
    """
    response = client.post(f"/delete/pod/1010100")

    assert response.status_code == 405
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['message'], str)
    assert data['message'] == f"The method is not allowed for the requested URL."
