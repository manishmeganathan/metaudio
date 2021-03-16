"""
Functional Test Module for the /update endpoint of the AudioServer
Test Framework: pyTest
"""
import json
import random


def test_Update_Song(client):
    """
    **GIVEN** a Flask application configured for testing and a Song file has been created\n
    **WHEN** the update endpoint is hit with a POST request for updating the Song\n
    **THEN** check that the response is valid for a 200 response (OK), check if the document
    was updated correctly and delete the created file.
    """
    # Create a Song file
    name = f"test-song-{random.randint(100, 999)}"
    request = {"audioFileType": "Song", "audioFileMetadata": {"name": f"{name}", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Update the file
    new_name = f"test-song-{random.randint(100, 999)}"
    request = {"audioFileType": "Song", "audioFileMetadata": {"name": f"{new_name}", "duration": 2}}
    response = client.post(f"/update/song/{docID}", json=request)

    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Update Complete"
    assert data['result'] == f"Song file with ID {docID} has been updated"
    assert data['document'] == docID
    assert data['pre-update']['_id'] == docID
    assert data['pre-update']['name'] == name
    assert data['pre-update']['duration'] == 45
    assert data['post-update']['_id'] == docID
    assert data['post-update']['name'] == new_name
    assert data['post-update']['duration'] == 2

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/song/{docID}")
    assert response.status_code == 200


def test_Update_Podcast(client):
    """
    **GIVEN** a Flask application configured for testing and a Podcast file has been created\n
    **WHEN** the update endpoint is hit with a POST request for updating the Podcast\n
    **THEN** check that the response is valid for a 200 response (OK), check if the document
    was updated correctly and delete the created file.
    """
    # Create a Song file
    name = f"test-podcast-{random.randint(100, 999)}"
    request = {"audioFileType": "Podcast",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "host": "host1", "participants": ["cast1"]}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Update the file
    new_name = f"test-podcast-{random.randint(100, 999)}"
    request = {"audioFileType": "Podcast",
               "audioFileMetadata": {"name": f"{new_name}", "duration": 4345,
                                     "host": "host2", "participants": ["cast3"]}}
    response = client.post(f"/update/podcast/{docID}", json=request)

    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Update Complete"
    assert data['result'] == f"Podcast file with ID {docID} has been updated"
    assert data['document'] == docID
    assert data['pre-update']['_id'] == docID
    assert data['pre-update']['name'] == name
    assert data['pre-update']['host'] == "host1"
    assert data['pre-update']['participants'] == ["cast1"]
    assert data['pre-update']['duration'] == 45
    assert data['post-update']['_id'] == docID
    assert data['post-update']['name'] == new_name
    assert data['post-update']['host'] == "host2"
    assert data['post-update']['participants'] == ["cast3"]
    assert data['post-update']['duration'] == 4345

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/podcast/{docID}")
    assert response.status_code == 200


def test_Update_Audiobook(client):
    """
    **GIVEN** a Flask application configured for testing and an Audiobook file has been created\n
    **WHEN** the update endpoint is hit with a POST request for updating the Audiobook\n
    **THEN** check that the response is valid for a 200 response (OK), check if the document
    was updated correctly and delete the created file.
    """
    # Create a Song file
    name = f"test-book-{random.randint(100, 999)}"
    request = {"audioFileType": "Audiobook",
               "audioFileMetadata": {"name": f"{name}", "duration": 45,
                                     "author": "author1", "narrator": "narrator1"}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Update the file
    new_name = f"test-book-{random.randint(100, 999)}"
    request = {"audioFileType": "Audiobook",
               "audioFileMetadata": {"name": f"{new_name}", "duration": 4535,
                                     "author": "author2", "narrator": "narrator2"}}
    response = client.post(f"/update/audiobook/{docID}", json=request)

    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    assert isinstance(data['status'], int)
    assert isinstance(data['message'], str)
    assert isinstance(data['result'], str)
    assert isinstance(data['document'], int)

    assert data['status'] == 200
    assert data['message'] == f"Update Complete"
    assert data['result'] == f"Audiobook file with ID {docID} has been updated"
    assert data['document'] == docID
    assert data['pre-update']['_id'] == docID
    assert data['pre-update']['name'] == name
    assert data['pre-update']['author'] == "author1"
    assert data['pre-update']['narrator'] == "narrator1"
    assert data['pre-update']['duration'] == 45
    assert data['post-update']['_id'] == docID
    assert data['post-update']['name'] == new_name
    assert data['post-update']['author'] == "author2"
    assert data['post-update']['narrator'] == "narrator2"
    assert data['post-update']['duration'] == 4535

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/audiobook/{docID}")
    assert response.status_code == 200


def test_Update_invalid_metadata(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request with an invalid 'audioFileMetadata'\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    request = {"audioFileType": "song", "audioFileMetadata": "23442353"}
    response = client.post(f"/update/song/1010101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileMetadata' must be a dict"


def test_Update_invalid_type_url(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request with an invalid type in the URL\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    response = client.post(f"/update/pod/1010101010")

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'Pod' is not supported"


def test_Update_invalid_type_request(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request with an invalid 'audioFileType'\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for 'audioFileType' not an str
    request = {"audioFileType": 34, "audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/update/song/101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileType' must be an str"

    # Test for 'audioFileType' not matching endpoint
    request = {"audioFileType": "son", "audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/update/song/101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileType' field must match the endpoint"


def test_Update_missing_key(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request with missing keys\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Test for missing 'audioFileMetadata'
    request = {"audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/update/song/101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileType' is required"

    # Test for missing 'audioFileMetadata'
    request = {"audioFileType": "Song"}
    response = client.post(f"/update/song/101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"'audioFileMetadata' is required"


def test_Update_no_document(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request for a document that doesn't exist\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    request = {"audioFileType": "song", "audioFileMetadata": {"name": "test-song", "duration": 45}}
    response = client.post(f"/update/song/101010", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"No document found for ID - 101010"


def test_Update_invalid_metadata_values(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a POST request with invalid metadata values\n
    **THEN** check that the response is valid for a 400 response (OK)
    """
    # Create a Song file
    name = f"test-song-{random.randint(100, 999)}"
    request = {"audioFileType": "Song", "audioFileMetadata": {"name": f"{name}", "duration": 45}}
    response = client.post(f"/create", json=request)

    assert response.status_code == 200
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)
    docID = data['document']

    # Test for invalid field in 'audioFileMetadata'
    request = {"audioFileType": "song", "audioFileMetadata": {"name": 33, "duration": 45}}
    response = client.post(f"/update/song/{docID}", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"metadata value is invalid for 'name' - not an str"

    # Test for missing field in 'audioFileMetadata'
    request = {"audioFileType": "song", "audioFileMetadata": {"duration": 45}}
    response = client.post(f"/update/song/{docID}", json=request)

    assert response.status_code == 400
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert data['status'] == 400
    assert data['message'] == f"Bad Request"
    assert data['error'] == f"metadata value is missing for 'name'"

    # Cleanup - Delete the added test file
    response = client.get(f"/delete/song/{docID}")
    assert response.status_code == 200


def test_Update_GET(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** the update endpoint is hit with a GET request\n
    **THEN** check that the response is valid for a 405 response (Method not Allowed)
    """
    response = client.get(f"/update/song/101010")

    assert response.status_code == 405
    assert isinstance(response.data, bytes)

    data = json.loads(response.data)

    assert isinstance(data['message'], str)
    assert data['message'] == f"The method is not allowed for the requested URL."


def test_Update_badURL(client):
    """
    **GIVEN** a Flask application configured for testing\n
    **WHEN** an invalid URL for the update endpoint is hit with a POST request\n
    **THEN** check that the response is valid for a 404 response (Not Found)
    """
    response = client.post(f"/update")
    assert response.status_code == 404

    response = client.post(f"/update/")
    assert response.status_code == 404

    response = client.post(f"/update/234234")
    assert response.status_code == 404

    response = client.post(f"/update/song")
    assert response.status_code == 404

    response = client.post(f"/update/song/something")
    assert response.status_code == 404
